---
name: positioning-strategy
description: Entry point for the Positioning Strategy Framework. Load the canonical skill and its references from the repository.
---

# Positioning Strategy — Claude Code entry point

This repository-local entry point points to the canonical skill:

- ../../../skills/positioning-strategy/SKILL.md
- ../../../skills/positioning-strategy/references/

Do not independently redefine the framework here. The canonical skill is the source of truth.

Install the full portable skill into a project-local Claude Code directory with:

~~~bash
python scripts/install_skill.py --agent claude
~~~
