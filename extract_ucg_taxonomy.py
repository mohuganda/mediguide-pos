#!/usr/bin/env python3
"""Collect disease/condition candidates from the Uganda Clinical Guidelines corpus.

Primary source: the per-chapter `chapters_split/NN/index.md` files, which carry
the complete chapter text with clean numbered headings. The split per-topic
files and `generated-manifest.json` are a lossy derivative of those (82+ numbered
entries missing, ~39 corrupted titles), so they are used only to attach the
public route of an entry that was split out.

Output is a review artefact shaped like the platform's `diseases` /
`disease_aliases` / `disease_codes` tables. Names and ICD-10 codes are copied
from the guideline text, never inferred. Nothing is seeded or committed here.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

CONTENT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/home/josh/mohUganda/mediguide-pos/guidelines-platform/src/content"
)
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")

CHAPTER_HEADING = re.compile(r"^#\s+Chapter\s+(\d+)\s*:\s*(.+?)\s*$")
NUMBERED_HEADING = re.compile(r"^(#{2,6})\s+\**\s*(\d+(?:\.\d+)+)\s*\**\s*(.+?)\s*$")
ANY_HEADING = re.compile(r"^#{1,6}\s+")
ICD_MARKER = re.compile(r"^\*{0,2}ICD[-‑ ]?10\s*CODES?\s*:?\*{0,2}\s*(.*)", re.IGNORECASE)
ICD_IN_TITLE = re.compile(r"\s*ICD[-‑ ]?10\s*CODES?\s*:?\s*(.*)$", re.IGNORECASE)
# The trailing lookahead tolerates glued source text such as "K85Acute".
CODE_TOKEN = re.compile(r"\b([A-TV-Z][0-9]{2}(?:\.[0-9A-Z]{1,4})?)(?![0-9.])")
PARENTHETICAL = re.compile(r"\s*\(([^)]{2,60})\)")

ACRONYMS = {
    "hiv", "aids", "tb", "art", "fp", "pid", "pph", "iv", "ent", "ors", "uti",
    "urti", "copd", "cmm", "lam", "gud", "sti", "stis", "dm", "htn", "imci",
    "who", "bcg", "dpt", "hpv", "rti", "arv", "arvs", "ncd", "ncds", "crp",
    "gi", "cns", "pcp", "rhd", "ckd", "aki", "sam", "mam", "anc", "pmtct",
    "ipt", "dka", "hhs", "pud", "ebv", "cmv", "orf", "bph", "csf", "ecg",
}
MIXED_CASE = {
    "hbsag": "HBsAg", "hbeag": "HBeAg", "covid": "COVID", "prep": "PrEP",
    "pep": "PEP", "ph": "pH",
}
SMALL_WORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or",
    "the", "to", "with", "without", "during", "after", "before",
}
# Entries whose title describes a procedure, schedule or service rather than a
# clinical subject. Flagged for review, never silently dropped.
NON_DISEASE_HINTS = (
    "guidelines", "guideline", "management of", "schedules", "schedule",
    "prophylaxis", "therapy", "counselling", "counseling", "technique",
    "procedure", "principles", "assessment of", "assess ", "prevention of",
    "care of", "use of", "administration", "method", "referral", "definition",
    "classification", "monitoring", "follow up", "follow-up", "planning",
    "requirements", "supplementation", "transfusion", "vaccine", "vaccination",
    "immunisation", "immunization", "screening", "diet", "feeding", "check ",
    "recommended", "provide ", "manage client", "introduction",
)


def normalize_term(value: str) -> str:
    """Mirror of services.normalizeDiseaseTerm in the Go backend."""
    out: list[str] = []
    space = True
    for ch in value.strip().lower():
        if unicodedata.category(ch)[0] in ("L", "N"):
            out.append(ch)
            space = False
        elif not space:
            out.append(" ")
            space = True
    return "".join(out).strip()


def slugify(value: str) -> str:
    """Produce a slug matching the platform check ^[a-z0-9]+(?:-[a-z0-9]+)*$."""
    return "-".join(normalize_term(value).split())


def title_case(value: str) -> str:
    words = value.split()
    out: list[str] = []
    for index, word in enumerate(words):
        bare = word.strip("()/,.’'")
        lowered = bare.lower()
        if lowered in MIXED_CASE:
            out.append(word.replace(bare, MIXED_CASE[lowered]))
        elif lowered in ACRONYMS:
            out.append(word.replace(bare, bare.upper()))
        elif index and lowered in SMALL_WORDS:
            out.append(word.lower())
        elif word.isupper() and len(bare) > 3:
            out.append(word.capitalize())
        else:
            out.append(word[:1].upper() + word[1:])
    return " ".join(out)


def clean_title(raw: str) -> str:
    text = ICD_IN_TITLE.sub("", raw).replace("**", "").strip()
    text = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", text)
    return re.sub(r"\s+", " ", text).strip(" :.-–")


def split_aliases(name: str) -> tuple[str, str | None, list[str]]:
    """Split 'Onchocerciasis (River Blindness)' into name, short name, aliases."""
    aliases: list[str] = []
    short_name: str | None = None
    for match in PARENTHETICAL.finditer(name):
        inner = match.group(1).strip().strip("“”‘’\"'")
        letters = [c for c in inner if c.isalpha()]
        if letters and all(c.isupper() for c in letters) and len(inner) <= 12:
            if short_name:
                aliases.append(inner)
            else:
                short_name = inner
        elif inner.lower() not in ("acute", "chronic"):
            aliases.append(inner if any(c.isupper() for c in inner) else title_case(inner))
    base = PARENTHETICAL.sub("", name).strip(" -/,")
    # 'Appendicitis (Acute)' reads as 'Acute Appendicitis'.
    for match in PARENTHETICAL.finditer(name):
        if match.group(1).strip().lower() in ("acute", "chronic"):
            base = f"{match.group(1).strip().capitalize()} {base}"
    return re.sub(r"\s+", " ", base).strip(), short_name, aliases


def parse_codes(raw: str | None) -> list[str]:
    if not raw:
        return []
    cleaned = raw.replace("–", "-").replace("—", "-").replace("‑", "-")
    cleaned = re.split(r"(?<=[a-z])\.\s", cleaned)[0]
    codes: list[str] = []
    for chunk in re.split(r"[,;]| and ", cleaned):
        found = CODE_TOKEN.findall(chunk)
        if not found:
            continue
        if len(found) == 2 and re.search(r"[0-9]\s*-\s*[A-TV-Z]", chunk):
            codes.append(f"{found[0]}-{found[1]}")
        else:
            codes.extend(found)
    seen: set[str] = set()
    unique: list[str] = []
    for code in codes:
        if code not in seen:
            seen.add(code)
            unique.append(code)
    return unique


def code_for_body(heading_line: str, body: list[str]) -> str:
    inline = ICD_IN_TITLE.search(heading_line)
    if inline and inline.group(1).strip():
        return inline.group(1).strip()
    for line in body[:25]:
        stripped = line.strip()
        if not stripped:
            continue
        found = ICD_MARKER.match(stripped)
        if found:
            return found.group(1).replace("**", "").strip()
    return ""


def routes_by_section(content: Path) -> dict[str, str]:
    manifest_path = content / "generated-manifest.json"
    if not manifest_path.exists():
        return {}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return {
        item["sectionNumber"]: item["route"]
        for item in manifest
        if item.get("sectionNumber")
    }


def main() -> int:
    routes = routes_by_section(CONTENT)
    records: list[dict] = []
    sections: list[dict] = []

    for index_file in sorted((CONTENT / "chapters_split").glob("*/index.md")):
        lines = index_file.read_text(encoding="utf-8").splitlines()
        chapter_number, chapter_title = 0, ""
        pending: dict | None = None
        body: list[str] = []

        def flush(entry: dict | None, text: list[str]) -> None:
            if entry is None:
                return
            entry["icd10_raw"] = code_for_body(entry.pop("heading_line"), text)
            entry["icd10_codes"] = parse_codes(entry["icd10_raw"])
            (sections if entry["depth"] == 2 else records).append(entry)

        for line in lines:
            chapter = CHAPTER_HEADING.match(line)
            if chapter:
                chapter_number, chapter_title = int(chapter.group(1)), chapter.group(2).strip()
                continue
            heading = NUMBERED_HEADING.match(line)
            if heading:
                flush(pending, body)
                body = []
                section_number = heading.group(2)
                depth = len(section_number.split("."))
                display = clean_title(heading.group(3))
                if display.isupper():
                    display = title_case(display)
                name, short_name, aliases = split_aliases(display)
                pending = {
                    "chapter": chapter_number,
                    "chapter_title": chapter_title,
                    "section_number": section_number,
                    "depth": depth,
                    "parent_section_number": section_number.rsplit(".", 1)[0] if depth >= 4 else "",
                    "name": name,
                    "short_name": short_name or "",
                    "aliases": aliases,
                    "normalized_name": normalize_term(name),
                    "slug": slugify(name),
                    "route": routes.get(section_number, ""),
                    "source_path": str(index_file.relative_to(CONTENT)),
                    "heading_line": heading.group(3),
                    "review_flag": "",
                }
                continue
            if pending is not None and not ANY_HEADING.match(line):
                body.append(line)
        flush(pending, body)

    index = {record["section_number"]: record for record in records}
    for record in records:
        parent = index.get(record["parent_section_number"])
        record["parent_name"] = parent["name"] if parent else ""
        record["parent_slug"] = parent["slug"] if parent else ""
        if record["depth"] >= 4 and not parent:
            record["review_flag"] = "orphan-child"

    names: dict[str, list[str]] = {}
    slugs: dict[str, list[str]] = {}
    for record in records:
        names.setdefault(record["normalized_name"], []).append(record["section_number"])
        slugs.setdefault(record["slug"], []).append(record["section_number"])

    for record in records:
        flags = [record["review_flag"]] if record["review_flag"] else []
        if any(hint in record["name"].lower() for hint in NON_DISEASE_HINTS):
            flags.append("non-clinical-subject?")
        if len(names[record["normalized_name"]]) > 1:
            flags.append("duplicate-name:" + ",".join(names[record["normalized_name"]]))
        elif len(slugs[record["slug"]]) > 1:
            flags.append("duplicate-slug")
        if not record["slug"]:
            flags.append("empty-slug")
        if record["icd10_raw"] and not record["icd10_codes"]:
            flags.append("code-text-unparsed")
        if not record["icd10_raw"]:
            flags.append("no-code-in-source")
        record["review_flag"] = " ".join(flags)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ucg-disease-candidates.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUT / "ucg-sections.json").write_text(
        json.dumps(sections, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    columns = [
        "chapter", "chapter_title", "section_number", "depth", "name", "short_name",
        "aliases", "slug", "parent_name", "icd10_codes", "icd10_raw", "review_flag",
        "route",
    ]
    with (OUT / "ucg-disease-candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["icd10_codes"] = " ".join(record["icd10_codes"])
            row["aliases"] = "; ".join(record["aliases"])
            writer.writerow(row)

    print(f"chapters          : {len({r['chapter'] for r in records})}")
    print(f"sections (d2)     : {len(sections)}")
    print(f"candidates        : {len(records)}")
    print(f"  parents (d3)    : {sum(1 for r in records if r['depth'] == 3)}")
    print(f"  children (d4)   : {sum(1 for r in records if r['depth'] == 4)}")
    print(f"  deeper (d5+)    : {sum(1 for r in records if r['depth'] >= 5)}")
    print(f"  with ICD-10     : {sum(1 for r in records if r['icd10_codes'])}")
    print(f"  with short name : {sum(1 for r in records if r['short_name'])}")
    print(f"  with aliases    : {sum(1 for r in records if r['aliases'])}")
    print(f"  with a route    : {sum(1 for r in records if r['route'])}")
    print(f"  flagged         : {sum(1 for r in records if r['review_flag'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
