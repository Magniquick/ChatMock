#!/usr/bin/env python3
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSTANTS_PATH = ROOT / "chatmock" / "constants.py"
AUTH_RS_URL = "https://raw.githubusercontent.com/openai/codex/refs/heads/main/codex-rs/core/src/auth.rs"
CLIENT_ID_REGEX = re.compile(r'CLIENT_ID\s*:\s*&str\s*=\s*"([^"]+)"')


def fetch_client_id() -> str:
    with urllib.request.urlopen(AUTH_RS_URL, timeout=30) as resp:
        data = resp.read().decode("utf-8", errors="replace")
    match = CLIENT_ID_REGEX.search(data)
    if not match:
        raise RuntimeError("Failed to locate CLIENT_ID in upstream auth.rs")
    return match.group(1)


assert fetch_client_id() == "app_EMoamEEZ73f0CkXaXp7hrann"
