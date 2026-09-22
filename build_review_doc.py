#!/usr/bin/env python3
"""Render the candidate disease taxonomy as a review document."""

from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).parent
rows = json.loads((HERE / "ucg-disease-candidates.json").read_text(encoding="utf-8"))

# A missing code is normal in the source and needs no decision; keep the
# review column for things a reviewer must actually rule on.
for row in rows:
    row["decision_flag"] = " ".join(
        flag for flag in row["review_flag"].split() if flag != "no-code-in-source"
    )

by_chapter: "OrderedDict[tuple[int, str], list[dict]]" = OrderedDict()
for row in rows:
    by_chapter.setdefault((row["chapter"], row["chapter_title"]), []).append(row)

lines: list[str] = []
add = lines.append
add("# Candidate disease and condition taxonomy — for review")
add("")
add("Source: the 24 chapter files at `guidelines-platform/src/content/chapters_split/NN/index.md`")
add("(Uganda Clinical Guidelines). Extracted, not authored: every name is the guideline's")
add("own heading and every ICD-10 code is copied from the guideline text. Where the source")
add("states no code, the cell is empty rather than guessed. Nothing has been seeded or committed.")
add("")
add("Proposed mapping onto the existing schema:")
add("")
add("| UCG level | Example | Proposed platform record |")
add("|---|---|---|")
add("| Chapter (24) | `Infectious Diseases` | `guideline_categories` row |")
add("| Section (75) | `2.5 PROTOZOAL PARASITES` | not seeded (grouping only) |")
add(f"| Numbered condition ({sum(1 for r in rows if r['depth'] == 3)}) | `2.5.2 Malaria` | `diseases` row, `parent_id` NULL |")
add(f"| Sub-condition ({sum(1 for r in rows if r['depth'] == 4)}) | `2.5.2.2 Complicated/Severe Malaria` | `diseases` row, `parent_id` = its parent |")
add("")
add(f"Totals: **{len(rows)} candidates** — {sum(1 for r in rows if r['depth'] == 3)} parents, "
    f"{sum(1 for r in rows if r['depth'] == 4)} children, "
    f"{sum(1 for r in rows if r['icd10_codes'])} with an ICD-10 code, "
    f"{sum(1 for r in rows if r['decision_flag'])} needing a decision.")
add("")
add("Review actions: strike anything that is not a clinical subject, merge the")
add("duplicates, and confirm the two unparsed codes. Legend: `**!**` = needs a decision.")
add("")

for (number, title), items in by_chapter.items():
    add(f"## {number}. {title}")
    add("")
    add("| # | Name | Short | Aliases | ICD-10 | Flag |")
    add("|---|---|---|---|---|---|")
    for row in items:
        indent = "&nbsp;&nbsp;↳ " if row["depth"] >= 4 else ""
        flag = row["decision_flag"].replace("|", "/")
        mark = "**!** " if flag else ""
        add(
            f"| {row['section_number']} | {indent}{mark}{row['name']} | "
            f"{row['short_name'] or ''} | {'; '.join(row['aliases'])} | "
            f"{' '.join(row['icd10_codes'])} | {flag} |"
        )
    add("")

flagged = [r for r in rows if r["decision_flag"]]
add("## Needing a decision")
add("")
add("| # | Chapter | Name | Reason |")
add("|---|---|---|---|")
for row in flagged:
    add(
        f"| {row['section_number']} | {row['chapter']} | {row['name']} | "
        f"{row['decision_flag'].replace('|', '/')} |"
    )
add("")
add("## Entries with no ICD-10 code in the source")
add("")
add(f"{sum(1 for r in rows if not r['icd10_raw'])} of {len(rows)} candidates. The guideline")
add("simply does not state a code for these; none has been inferred.")
add("")

(HERE / "ucg-disease-candidates-review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote ucg-disease-candidates-review.md ({len(lines)} lines, {len(flagged)} flagged)")
