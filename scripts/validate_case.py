#!/usr/bin/env python3
"""Validate a positioning case JSON file using only the Python standard library."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCORES = ("relevance", "differentiation", "credibility", "strategic_fit", "economics", "defensibility", "execution")
GRADES = {"A", "B", "C", "D"}
REQUIRED = ("case_id", "brand", "category", "target_audience", "competitive_frame", "current_position", "desired_position", "point_of_difference", "reasons_to_believe", "opportunity_score", "sources", "claims", "counter_evidence")


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Root JSON value must be an object."]
    for key in REQUIRED:
        if key not in data:
            errors.append(f"Missing required field: {key}")
    if errors:
        return errors

    for key in ("case_id", "brand", "category", "target_audience", "competitive_frame"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key} must be a non-empty string.")
    if not isinstance(data.get("reasons_to_believe"), list):
        errors.append("reasons_to_believe must be an array.")
    if not isinstance(data.get("counter_evidence"), list):
        errors.append("counter_evidence must be an array.")

    score = data.get("opportunity_score")
    if not isinstance(score, dict):
        errors.append("opportunity_score must be an object.")
    else:
        for key in SCORES:
            value = score.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                errors.append(f"opportunity_score.{key} must be an integer from 1 to 5.")

    sources = data.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list):
        errors.append("sources must be an array.")
        sources = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"sources[{index}] must be an object.")
            continue
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            errors.append(f"sources[{index}].source_id must be a non-empty string.")
        elif source_id in source_ids:
            errors.append(f"Duplicate source_id: {source_id}")
        else:
            source_ids.add(source_id)
        if source.get("grade") not in GRADES:
            errors.append(f"sources[{index}].grade must be A, B, C, or D.")
        if source.get("synthetic") is True and source.get("grade") != "D":
            errors.append(f"Synthetic source {source_id} must use grade D.")

    claims = data.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be an array.")
        claims = []
    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{index}] must be an object.")
            continue
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"claims[{index}].claim_id must be a non-empty string.")
        elif claim_id in claim_ids:
            errors.append(f"Duplicate claim_id: {claim_id}")
        else:
            claim_ids.add(claim_id)
        if claim.get("evidence_grade") not in GRADES:
            errors.append(f"claims[{index}].evidence_grade must be A, B, C, or D.")
        if claim.get("attribution_grade") not in GRADES:
            errors.append(f"claims[{index}].attribution_grade must be A, B, C, or D.")
        refs = claim.get("source_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"claims[{index}].source_ids must be a non-empty array.")
        else:
            for ref in refs:
                if ref not in source_ids:
                    errors.append(f"claims[{index}] references unknown source_id: {ref}")

    if not claims:
        errors.append("At least one claim is required.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_file", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.case_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.case_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
