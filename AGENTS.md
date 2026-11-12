# Repository Agent Instructions

## Mission
Maintain this repository as a portable, evidence-led positioning strategy Agent Skill.

## Source of truth
- Canonical skill: skills/positioning-strategy/SKILL.md
- Canonical references: skills/positioning-strategy/references/
- Agent-specific directories are entry points; keep them aligned with the canonical skill.
- Schemas define contracts for structured cases and examples.

## Required behavior
1. Read the canonical skill before changing workflow or reference materials.
2. Distinguish book-derived concepts from modern operational extensions.
3. Never invent customer research, market share, sales, source URLs, case outcomes, or causal effects.
4. Label every synthetic example as synthetic.
5. Separate source/evidence quality from causal-attribution confidence.
6. Preserve counter-evidence and limitations in every substantive case.
7. Do not treat an unoccupied space as an opportunity without demand, economics, and capability checks.
8. Do not conflate positioning statement, value proposition, slogan, campaign, and product specification.
9. Avoid copying copyrighted book passages or proprietary consulting reports.
10. Do not package unlicensed advertising assets.

## Engineering
- Python standard library only unless a dependency is justified.
- UTF-8 and LF line endings.
- Every JSON file must parse.
- Schema/example changes require tests or validation.
- Do not weaken validation to make invalid examples pass.
- Update both README files when public interfaces change.
- Keep agent entry points concise and point to the canonical skill.

## Validation
~~~bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/validate_case.py examples/industrial-compressor-case.json
~~~

## Commit style
Use conventional commits: docs:, feat:, fix:, test:, chore:.
