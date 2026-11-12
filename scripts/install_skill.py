#!/usr/bin/env python3
"""Install the canonical skill into project-local agent directories."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

TARGETS = {
    "codex": Path(".codex/skills/positioning-strategy"),
    "claude": Path(".claude/skills/positioning-strategy"),
    "opencode": Path(".opencode/skills/positioning-strategy"),
    "pi": Path(".pi/skills/positioning-strategy"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["all", *TARGETS], default="all")
    parser.add_argument("--target-root", type=Path, default=Path.cwd())
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    source = args.source_root.resolve() / "skills/positioning-strategy"
    if not (source / "SKILL.md").is_file():
        parser.error(f"Canonical skill not found at {source}")
    selected = TARGETS if args.agent == "all" else {args.agent: TARGETS[args.agent]}
    target_root = args.target_root.resolve()
    for name, relative in selected.items():
        destination = target_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        print(f"Installed {name}: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
