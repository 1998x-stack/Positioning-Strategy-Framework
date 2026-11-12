#!/usr/bin/env python3
"""Build a concise Markdown positioning case report from a JSON case file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from score_opportunity import calculate, band


def build(data: dict) -> str:
    score = calculate(data["opportunity_score"])
    lines = [
        f"# Positioning Case — {data['brand']}", "",
        "> Evidence quality and causal attribution are separate. Do not infer causality from a score or a before/after change.", "",
        "## Decision context",
        f"- Case: {data['case_id']}",
        f"- Category: {data['category']}",
        f"- Target: {data['target_audience']}",
        f"- Competitive frame: {data['competitive_frame']}", "",
        "## Current and desired position",
        f"- Current: {data['current_position']}",
        f"- Desired: {data['desired_position']}",
        f"- Difference: {data['point_of_difference']}", "",
        "## Reasons to believe",
    ]
    lines.extend(f"- {item}" for item in data.get("reasons_to_believe", []))
    lines.extend(["", "## Opportunity score", f"- Weighted score: **{score:.2f}/5.00**", f"- Band: {band(score)}", "", "| Dimension | Score |", "|---|---:|"])
    for key, value in data["opportunity_score"].items():
        lines.append(f"| {key} | {value}/5 |")
    lines.extend(["", "## Hard gates"])
    lines.extend(f"- {item}" for item in data.get("hard_gates", []))
    lines.extend(["", "## Claims and evidence", "| Claim ID | Claim | Evidence | Attribution | Sources |", "|---|---|---:|---:|---|"])
    for claim in data.get("claims", []):
        safe_claim = claim.get("claim", "").replace("|", "\\|")
        lines.append(f"| {claim.get('claim_id', '')} | {safe_claim} | {claim.get('evidence_grade', '')} | {claim.get('attribution_grade', '')} | {', '.join(claim.get('source_ids', []))} |")
    lines.extend(["", "## Counter-evidence"])
    lines.extend(f"- {item}" for item in data.get("counter_evidence", []))
    lines.extend(["", "## Unknowns"])
    lines.extend(f"- {item}" for item in data.get("unknowns", []))
    lines.extend(["", "## Sources"])
    for source in data.get("sources", []):
        url = source.get("url") or "No public URL"
        marker = " — SYNTHETIC" if source.get("synthetic") else ""
        lines.append(f"- {source.get('source_id')}: {source.get('title')} [{source.get('grade')}]{marker} — {url}")
    lines.extend(["", "---", "Generated from structured case data. Verify every source and claim before external publication.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_file", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.case_file.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build(data), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
