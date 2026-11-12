#!/usr/bin/env python3
"""Check required project files, agent entry points, JSON, and Python syntax."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "README.zh.md", "AGENTS.md",
    "skills/positioning-strategy/SKILL.md",
    "skills/positioning-strategy/references/book-chapter-map.md",
    "skills/positioning-strategy/references/evidence-and-causal-attribution.md",
    "schemas/positioning-case.schema.json",
    "examples/industrial-compressor-case.json",
]
AGENTS = [".codex", ".claude", ".opencode", ".pi"]


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing required file: {relative}")
    for agent in AGENTS:
        entry = ROOT / agent / "skills/positioning-strategy/SKILL.md"
        if not entry.is_file():
            errors.append(f"Missing agent entry point: {entry.relative_to(ROOT)}")
        elif "skills/positioning-strategy/SKILL.md" not in entry.read_text(encoding="utf-8"):
            errors.append(f"Agent entry point does not reference canonical skill: {entry.relative_to(ROOT)}")
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
    for path in ROOT.rglob("*.py"):
        if any(part in {".venv", "__pycache__"} for part in path.parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            errors.append(f"Invalid Python {path.relative_to(ROOT)}: {exc}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK: repository structure, JSON, Python syntax, and agent entry points")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
