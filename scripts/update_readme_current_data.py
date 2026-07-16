#!/usr/bin/env python3
"""
Regenerate the "Current Data" section of README.md from
data/jurisdiction_reference_table.csv.

This script only touches the content between the two marker comments:

    <!-- CURRENT_DATA_TABLE_START -->
    ...
    <!-- CURRENT_DATA_TABLE_END -->

It lists jurisdictions that submit data directly to USDT (data_source ==
"USDT" in the reference table), the conditions each submits, and a link to
the jurisdiction's public dashboard/website, if one is on file.

Usage:
    python scripts/update_readme_current_data.py
        [--csv data/jurisdiction_reference_table.csv]
        [--readme README.md]

Exits non-zero if the markers are missing from the README, or if the CSV
cannot be read, so CI fails loudly instead of silently skipping the update.
"""

import argparse
import csv
import sys
from pathlib import Path

START_MARKER = "<!-- CURRENT_DATA_TABLE_START -->"
END_MARKER = "<!-- CURRENT_DATA_TABLE_END -->"

NNDSS_SOURCE_URL = "https://www.cdc.gov/nndss/"

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "data" / "jurisdiction_reference_table.csv"
DEFAULT_README = REPO_ROOT / "README.md"


def format_conditions(raw: str) -> str:
    """Turn 'measles; meningococcus; pertussis' into 'Measles, Meningococcus, Pertussis'."""
    conditions = [c.strip() for c in raw.split(";") if c.strip()]
    return ", ".join(c.title() for c in conditions)


def format_website(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return "—"
    return f"[Link]({url})"


def load_usdt_jurisdictions(csv_path: Path):
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row.get("data_source", "").strip() == "USDT"]
    rows.sort(key=lambda r: r.get("jurisdiction_name", ""))
    return rows


def build_table(rows) -> str:
    header = "| State | Jurisdiction ID | Conditions Submitted to USDT | Jurisdiction Website |"
    sep = "|---|---|---|---|"
    lines = [header, sep]
    for row in rows:
        name = row.get("jurisdiction_name", "").strip()
        jid = row.get("jurisdiction_id", "").strip()
        conditions = format_conditions(row.get("conditions_included", ""))
        website = format_website(row.get("website_dashboard_link", ""))
        lines.append(f"| {name} | {jid} | {conditions} | {website} |")
    return "\n".join(lines)


def build_section_body(rows) -> str:
    table = build_table(rows)
    n = len(rows)
    return (
        f"{n} jurisdictions currently submit data directly to USDT:\n"
        f"\n"
        f"{table}\n"
        f"\n"
        f"**Note:** For jurisdictions not yet submitting directly to USDT (and for "
        f"conditions not listed above), USDT supplements coverage using "
        f"state/territory-level data from the CDC's National Notifiable Diseases "
        f"Surveillance System (NNDSS). Source: [{NNDSS_SOURCE_URL}]({NNDSS_SOURCE_URL})\n"
        f"\n"
        f"For more info, see [`data/jurisdiction_reference_table.csv`](data/jurisdiction_reference_table.csv)."
    )


def update_readme(readme_path: Path, section_body: str) -> str:
    text = readme_path.read_text(encoding="utf-8")

    if START_MARKER not in text or END_MARKER not in text:
        raise SystemExit(
            f"Could not find {START_MARKER} / {END_MARKER} markers in {readme_path}. "
            "Add the 'Current Data' section with these markers before running this script."
        )

    before, rest = text.split(START_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)

    new_text = f"{before}{START_MARKER}\n{section_body}\n{END_MARKER}{after}"
    return new_text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--readme", type=Path, default=DEFAULT_README)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with status 1 if the README would change, without writing (for CI checks).",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"ERROR: CSV not found at {args.csv}", file=sys.stderr)
        return 1
    if not args.readme.exists():
        print(f"ERROR: README not found at {args.readme}", file=sys.stderr)
        return 1

    rows = load_usdt_jurisdictions(args.csv)
    section_body = build_section_body(rows)
    new_text = update_readme(args.readme, section_body)
    old_text = args.readme.read_text(encoding="utf-8")

    if new_text == old_text:
        print("README.md 'Current Data' section already up to date.")
        return 0

    if args.check:
        print("README.md 'Current Data' section is out of date.", file=sys.stderr)
        return 1

    args.readme.write_text(new_text, encoding="utf-8")
    print(f"Updated 'Current Data' section in {args.readme} ({len(rows)} USDT-submitting jurisdictions).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
