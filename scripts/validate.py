#!/usr/bin/env python3
"""
Validate the company-finance-buddy skill source tree before packaging.

Checks structural rules that break the skill silently if violated:
  1. Required files exist and are non-empty.
  2. SKILL.md frontmatter is well-formed, has name + description, and the
     name matches the directory.
  3. The description stays inside the trigger-budget (a description that is
     too short under-triggers, too long crowds the system prompt).
  4. Every `references/...` or `assets/...` path mentioned in any markdown
     file actually resolves on disk. A dead reference means the model is
     told to read a file that isn't there and improvises instead.
  5. Progressive-disclosure budget: SKILL.md stays small enough to load on
     every trigger; reference files stay small enough to load one at a time.
  6. Domain guard: no hardcoded statutory dates, rates or thresholds. The
     skill's own design rule is that it holds the sequence, not the calendar.

Exit code 0 = pass, 1 = fail. Warnings never fail the build.

Usage:
    python3 scripts/validate.py [skill_dir]
"""

from __future__ import annotations

import pathlib
import re
import sys

SKILL_DIR_DEFAULT = "company-finance-buddy"

REQUIRED_FILES = [
    "SKILL.md",
    "references/boundaries.md",
    "references/close-checklist.md",
    "references/gst-reconciliation.md",
    "references/tds-reconciliation.md",
    "references/anomaly-detection.md",
    "references/reporting.md",
    "references/zoho-books.md",
    "assets/templates.md",
]

# Trigger budget. Claude sees every skill description at once; the
# description is the only thing that decides whether this skill fires.
DESCRIPTION_MIN_CHARS = 200
DESCRIPTION_MAX_CHARS = 1024

# Progressive-disclosure budget, in lines.
SKILL_MD_MAX_LINES = 250
REFERENCE_MAX_LINES = 400

# Statutory values that move. Matching any of these in prose is a warning,
# not an error — some appear as worked examples, which is legitimate.
VOLATILE_PATTERNS = [
    (r"\b(?:due|filed?|deadline)\s+(?:by|on)\s+(?:the\s+)?\d{1,2}(?:st|nd|rd|th)?\b",
     "hardcoded statutory due date"),
    (r"\bGSTR-?[13][AB]?\s+(?:is\s+)?due\s+\d{1,2}\b",
     "hardcoded return due date"),
    (r"\bTDS\s+rate\s+(?:is|of)\s+\d+(?:\.\d+)?%",
     "hardcoded TDS rate"),
    (r"\be-?invoic\w*\s+threshold\s+(?:is|of)\s+(?:₹|Rs\.?)\s?\d",
     "hardcoded e-invoicing threshold"),
]

errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Minimal YAML frontmatter reader — key: value pairs only, no deps."""
    if not text.startswith("---"):
        fail("SKILL.md does not open with a `---` frontmatter block.")
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        fail("SKILL.md frontmatter block is not closed with `---`.")
        return {}
    block = text[3:end]
    data: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2).strip()
        elif key:
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else SKILL_DIR_DEFAULT).resolve()

    if not root.is_dir():
        print(f"FAIL  skill directory not found: {root}")
        return 1

    # 1. Required files present and non-empty.
    for rel in REQUIRED_FILES:
        p = root / rel
        if not p.is_file():
            fail(f"missing required file: {rel}")
        elif p.stat().st_size == 0:
            fail(f"required file is empty: {rel}")

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        print("FAIL  SKILL.md missing — cannot continue.")
        return 1

    text = skill_md.read_text(encoding="utf-8")

    # 2. Frontmatter.
    fm = parse_frontmatter(text)
    name = fm.get("name", "")
    description = fm.get("description", "")

    if not name:
        fail("frontmatter is missing `name`.")
    elif name != root.name:
        fail(f"frontmatter name `{name}` does not match directory `{root.name}`.")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(f"frontmatter name `{name}` must be lowercase kebab-case.")

    # 3. Description budget.
    if not description:
        fail("frontmatter is missing `description` — the skill will never trigger.")
    else:
        n = len(description)
        if n < DESCRIPTION_MIN_CHARS:
            fail(f"description is {n} chars — under {DESCRIPTION_MIN_CHARS}, it will under-trigger.")
        if n > DESCRIPTION_MAX_CHARS:
            fail(f"description is {n} chars — over the {DESCRIPTION_MAX_CHARS} budget.")
        if "Use this skill" not in description and "Use it" not in description:
            warn("description does not state when to use the skill; triggering will be vague.")

    # 4. Every referenced path resolves.
    md_files = sorted(root.rglob("*.md"))
    ref_pattern = re.compile(r"`((?:references|assets)/[A-Za-z0-9._-]+\.md)`")
    for md in md_files:
        body = md.read_text(encoding="utf-8")
        for target in set(ref_pattern.findall(body)):
            if not (root / target).is_file():
                fail(f"{md.relative_to(root)} references `{target}` which does not exist.")

    # Reverse check: a reference file nobody points at will never be read.
    linked: set[str] = set()
    for md in md_files:
        linked |= set(ref_pattern.findall(md.read_text(encoding="utf-8")))
    for md in md_files:
        rel = md.relative_to(root).as_posix()
        if rel != "SKILL.md" and rel not in linked:
            warn(f"{rel} is not referenced from any other file — it will never be loaded.")

    # 5. Progressive-disclosure budget.
    skill_lines = len(text.splitlines())
    if skill_lines > SKILL_MD_MAX_LINES:
        fail(f"SKILL.md is {skill_lines} lines — over the {SKILL_MD_MAX_LINES}-line always-loaded budget.")
    for md in md_files:
        rel = md.relative_to(root).as_posix()
        if rel == "SKILL.md":
            continue
        n = len(md.read_text(encoding="utf-8").splitlines())
        if n > REFERENCE_MAX_LINES:
            fail(f"{rel} is {n} lines — over the {REFERENCE_MAX_LINES}-line per-reference budget.")

    # 6. Volatile statutory values.
    for md in md_files:
        body = md.read_text(encoding="utf-8")
        for pattern, label in VOLATILE_PATTERNS:
            for m in re.finditer(pattern, body, flags=re.IGNORECASE):
                line_no = body[: m.start()].count("\n") + 1
                warn(f"{md.relative_to(root)}:{line_no} possible {label}: \"{m.group(0).strip()}\"")

    # Report.
    total_lines = sum(len(m.read_text(encoding='utf-8').splitlines()) for m in md_files)
    print(f"skill      {root.name}")
    print(f"files      {len(md_files)} markdown")
    print(f"lines      {total_lines}")
    print(f"SKILL.md   {skill_lines} lines / {SKILL_MD_MAX_LINES} budget")
    print(f"desc       {len(description)} chars / {DESCRIPTION_MAX_CHARS} budget")
    print()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")

    if errors:
        print(f"\n{len(errors)} error(s). Not packageable.")
        return 1

    print(f"PASS  {len(warnings)} warning(s), 0 errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
