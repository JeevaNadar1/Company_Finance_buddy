# Changelog

Notable changes to Company Finance Buddy.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is semantic, applied to skill behaviour:

1. **Major** — a boundary changes, or output that previously auto-applied no
   longer does (or the reverse).
2. **Minor** — a new check, matching tier, schedule or report.
3. **Patch** — wording, formatting, documentation, false-positive tuning.

## [Unreleased]

### Added
1. Unpacked skill source tree under `company-finance-buddy/`, so the skill
   can be read, diffed and reviewed without unzipping the bundle.
2. `scripts/validate.py` — structural validation: frontmatter, description
   budget, reference resolution, progressive-disclosure line budgets, and a
   warning pass for hardcoded statutory values.
3. `scripts/build.sh` — deterministic packaging into `.skill`.
4. `Makefile` targets: `validate`, `build`, `release-check`, `clean`.
5. CI on push and pull request: validation, plus a check that the committed
   bundle is not stale against the source.
6. Release workflow that builds the bundle and attaches it to a tagged
   release.
7. Synthetic fixtures under `examples/` — purchase register, GSTR-2B
   extract, 26AS extract, bank statement, and the expected reconciliation
   output for each.
8. `docs/ARCHITECTURE.md` and `docs/USAGE.md`.
9. `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
   issue and pull request templates.

### Changed
1. Nothing in skill behaviour. This release is repository scaffolding only —
   the packaged bundle is byte-identical in content to v1.0.0.

## [1.0.0]

### Added
1. GST ITC reconciliation against GSTR-2B across six matching tiers, with
   invoice-number normalisation and a cross-period window.
2. TDS reconciliation against 26AS and AIS, both directions, with mismatch
   bucketing and chase lists.
3. Bank reconciliation with auto-matching and ageing of the remainder.
4. Anomaly detection: duplicates, vendor name variants, wrong-sign balances,
   movement variance, threshold clustering, sequence gaps, weekend postings.
5. Dependency-ordered close checklist from cut-off through reporting.
6. MIS pack: schedules, ageing, variance narrative, open-items log.
7. Zoho Books connector discipline — read-first, no write without itemised
   confirmation.
8. Hard boundaries in `references/boundaries.md`: no tax treatment, no rate
   determination, no compliance assertion, no sign-off, no guessing to reach
   100% coverage.
