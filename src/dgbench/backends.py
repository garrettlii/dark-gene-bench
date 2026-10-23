"""Model backends for no-data (prior-only) questions, plus response parsing.

``api`` backends call the providers' SDKs and give the cleanest comparison
(same plain prompt, no agent scaffold). ``cli`` backends shell out to an
installed agent CLI; they work with workspace sign-ins instead of API keys,
but each CLI adds its own system prompt, so record which backend produced
which numbers.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Sequence

_JSON_OBJECT = re.compile(r"\{[^{}]*\}")


def parse_probs(text: str, labels: Sequence[str]) -> dict[str, float] | None:
    """Last JSON object in the text that has all labels with non-negative numbers, normalized to sum 1."""
    if not text:
        return None
    for candidate in reversed(_JSON_OBJECT.findall(text)):
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        try:
            vals = {lab: float(obj[lab]) for lab in labels}
        except (KeyError, TypeError, ValueError):
            continue
        if any(v < 0 for v in vals.values()):
            continue
        total = sum(vals.values())
        if total <= 0:
            continue
        return {k: v / total for k, v in vals.items()}
    return None


class Backend:
    name = "base"

    def complete(self, prompt: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError

    def describe(self) -> dict:
        return {"backend": self.name}


class AnthropicBackend(Backend):
    name = "anthropic"

    def __init__(self, model: str, max_tokens: int = 1024):
        import anthropic

        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens

    def complete(self, prompt: str) -> str:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(getattr(block, "text", "") for block in resp.content)

    def describe(self) -> dict:
        return {"backend": self.name, "model": self.model, "max_tokens": self.max_tokens}


class OpenAIBackend(Backend):
    name = "openai"

    def __init__(self, model: str, reasoning_effort: str | None = None):
        import openai

        self.client = openai.OpenAI()
        self.model = model
        self.reasoning_effort = reasoning_effort

    def complete(self, prompt: str) -> str:
        kwargs = {"model": self.model, "input": prompt}
        if self.reasoning_effort:
            kwargs["reasoning"] = {"effort": self.reasoning_effort}
        resp = self.client.responses.create(**kwargs)
        return resp.output_text

    def describe(self) -> dict:
        return {"backend": self.name, "model": self.model, "reasoning_effort": self.reasoning_effort}


class CLIBackend(Backend):
    """Runs a command template such as ["claude", "-p", "{prompt}"] in an empty directory outside the repo."""

    name = "cli"

    def __init__(self, command: list[str], workdir: str, env: dict[str, str] | None = None, timeout_s: int = 600):
        if not any("{prompt}" in part for part in command):
            raise ValueError("CLI command template must contain {prompt}")
        self.command = command
        self.workdir = Path(os.path.expanduser(workdir))
        self.workdir.mkdir(parents=True, exist_ok=True)
        if any(self.workdir.iterdir()):
            raise RuntimeError(f"CLI workdir {self.workdir} must be empty")
        self.env = {k: os.path.expanduser(v) for k, v in (env or {}).items()}
        self.timeout_s = timeout_s

    def complete(self, prompt: str) -> str:
        cmd = [part.replace("{prompt}", prompt) for part in self.command]
        env = {**os.environ, **self.env}
        # empty stdin: some CLIs (codex exec) otherwise wait for extra prompt input on an open stdin
        proc = subprocess.run(cmd, cwd=self.workdir, env=env, capture_output=True, text=True,
                              timeout=self.timeout_s, stdin=subprocess.DEVNULL)
        if proc.returncode != 0:
            raise RuntimeError(f"exit {proc.returncode}: {proc.stderr[-500:]}")
        return proc.stdout

    def describe(self) -> dict:
        return {"backend": self.name, "command": self.command, "env_vars": sorted(self.env)}


def make_backend(model_cfg: dict, backends_cfg: dict) -> Backend:
    kind = model_cfg["backend"]
    if kind == "anthropic":
        opts = backends_cfg.get("anthropic", {})
        return AnthropicBackend(model_cfg["model"], max_tokens=opts.get("max_tokens", 1024))
    if kind == "openai":
        return OpenAIBackend(model_cfg["model"], reasoning_effort=model_cfg.get("reasoning_effort"))
    if kind == "cli":
        cli = backends_cfg["cli"]
        workdir = str(Path(os.path.expanduser(cli["workdir"])) / model_cfg["name"])
        return CLIBackend(model_cfg["command"], workdir=workdir, env=model_cfg.get("env"),
                          timeout_s=cli.get("timeout_s", 600))
    raise ValueError(f"unknown backend {kind!r}")


def call_with_retries(backend: Backend, prompt: str, retries: int = 2, wait_s: float = 5.0) -> tuple[str | None, str | None, float]:
    """Returns (text, error, seconds)."""
    start = time.time()
    last_error = None
    for attempt in range(retries + 1):
        try:
            return backend.complete(prompt), None, time.time() - start
        except Exception as exc:  # noqa: BLE001 - record and retry any provider error
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < retries:
                time.sleep(wait_s * (2 ** attempt))
    return None, last_error, time.time() - start
