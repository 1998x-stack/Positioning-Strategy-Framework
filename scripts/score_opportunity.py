#!/usr/bin/env python3
"""Calculate the documented weighted positioning-opportunity score."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

WEIGHTS = {
    "relevance": 0.20,
    "differentiation": 0.15,
    "credibility": 0.15,
    "strategic_fit": 0.15,
    "economics": 0.15,
    "defensibility": 0.10,
    "execution": 0.10,
}


def calculate(scores: dict[str, int]) -> float:
    missing = set(WEIGHTS) - set(scores)
    if missing:
        raise ValueError("Missing dimensions: " + ", ".join(sorted(missing)))
    for key, value in scores.items():
        if key not in WEIGHTS:
            raise ValueError(f"Unknown score dimension: {key}")
        if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
            raise ValueError(f"{key} must be an integer from 1 to 5")
    return round(sum(scores[key] * weight for key, weight in WEIGHTS.items()), 2)


def band(value: float) -> str:
    if value >= 4.2:
        return "Priority for validation; hard gates still apply"
    if value >= 3.5:
        return "Promising; validate missing evidence"
    if value >= 2.8:
        return "Rework the option or narrow the target"
    return "Do not prioritize at this stage"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_file", type=Path)
    args = parser.parse_args()
    data = json.loads(args.case_file.read_text(encoding="utf-8"))
    result = calculate(data["opportunity_score"])
    print(f"Weighted score: {result:.2f} / 5.00")
    print(f"Decision band: {band(result)}")
    for gate in data.get("hard_gates", []):
        print(f"HARD GATE: {gate}")
    print("Reminder: score is structured judgment, not objective measurement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
