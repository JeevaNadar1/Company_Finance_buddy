# Contributing

The whole skill is markdown. There is no runtime, no dependency tree and
nothing to install beyond Python 3 for the validator.

## Repository layout

```
company-finance-buddy/      the skill source — edit here
company-finance-buddy.skill the packaged bundle — generated, but committed
scripts/                    validate.py, build.sh
docs/                       architecture and usage notes
examples/                   synthetic fixtures, safe to publish
```

The `.skill` bundle is a build artifact that is committed anyway, so anyone
can install without cloning. CI fails if it drifts from the source. Never
hand-edit the bundle.

## Workflow

```bash
git clone https://github.com/JeevaNadar1/Company_Finance_buddy.git
cd Company_Finance_buddy

# edit company-finance-buddy/...

make validate     # structural checks
make build        # validate, then repackage the bundle
```

Commit both the source change and the rebuilt bundle in the same commit.

## What the validator enforces

1. Required files exist and are non-empty.
2. Frontmatter has a `name` matching the directory and a `description`
   between 200 and 1024 characters.
3. Every `references/...` path mentioned anywhere resolves on disk.
4. `SKILL.md` stays under 250 lines; each reference file under 400.
5. No hardcoded statutory dates, rates or thresholds (warning only).

Rules 3 and 4 exist for the same reason: `SKILL.md` loads on every trigger,
reference files load on demand. A bloated `SKILL.md` costs tokens on every
invocation. A dead reference means the model is told to read a file that
isn't there and improvises the content instead — which is the exact failure
mode the skill is built to avoid.

## The bar for a change

**Adding a matching tier or loosening one.** State the confidence band, and
say what happens on a false positive. Anything below high confidence must
not auto-apply. A higher match rate bought by auto-applying weak evidence is
a regression, not an improvement.

**Adding an anomaly check.** It must be cheap to dismiss. A check that fires
on 200 rows a month gets ignored within two closes, and then so does every
other check. Say what the expected hit rate is on a normal ledger.

**Touching boundaries.** `references/boundaries.md` is the constitution.
Widening it — letting the skill pick a rate, opine on treatment, or conclude
that something is compliant — will not be merged. Narrowing or clarifying it
will be.

**Statutory content.** Encode sequence and dependency, never the calendar.
"ITC reconciliation happens after 2B is available and before the summary
return is filed" is stable. "File by the 20th" is a liability the day it
changes.

## Data hygiene

No real client data enters this repository, in any form, including in an
issue or a PR description. CI greps for GSTIN-shaped strings outside
`examples/` and fails the build.

Synthetic fixtures go in `examples/` with obviously fake entity names.

## Style

1. Numbered lists, not bullets, in documentation.
2. Rupee amounts in Indian digit grouping — `₹1,24,80,000`.
3. Tables for anything the reader will compare across.
4. No emoji in the skill source; the model reads it as content.
5. Second person, imperative. The audience is the model, not a human reader.
