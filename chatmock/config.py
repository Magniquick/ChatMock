from __future__ import annotations

import os
import sys
from pathlib import Path

from .constants import (
    DEFAULT_CHATGPT_RESPONSES_URL,
    DEFAULT_CLIENT_ID,
    DEFAULT_OAUTH_ISSUER,
)

CLIENT_ID_DEFAULT = os.getenv("CHATGPT_LOCAL_CLIENT_ID") or DEFAULT_CLIENT_ID
OAUTH_ISSUER_DEFAULT = os.getenv("CHATGPT_LOCAL_ISSUER") or DEFAULT_OAUTH_ISSUER
OAUTH_TOKEN_URL = f"{OAUTH_ISSUER_DEFAULT}/oauth/token"

CHATGPT_RESPONSES_URL = DEFAULT_CHATGPT_RESPONSES_URL


def _read_prompt_text(filename: str) -> str | None:
    candidates = [
        Path(__file__).parent.parent / filename,
        Path(__file__).parent / filename,
        (
            Path(getattr(sys, "_MEIPASS", "")) / filename
            if getattr(sys, "_MEIPASS", None)
            else None
        ),
        Path.cwd() / filename,
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            if candidate.exists():
                content = candidate.read_text(encoding="utf-8")
                if isinstance(content, str) and content.strip():
                    return content
        except Exception:
            continue
    return None


def read_base_instructions() -> str:
    content = _read_prompt_text("prompt.md")
    if content is None:
        raise FileNotFoundError(
            "Failed to read prompt.md; expected adjacent to package or CWD."
        )
    return content


def read_gpt5_codex_instructions(fallback: str) -> str:
    content = _read_prompt_text("prompt_gpt5_codex.md")
    return content if isinstance(content, str) and content.strip() else fallback


BASE_INSTRUCTIONS = read_base_instructions()
GPT5_CODEX_INSTRUCTIONS = read_gpt5_codex_instructions(BASE_INSTRUCTIONS)
