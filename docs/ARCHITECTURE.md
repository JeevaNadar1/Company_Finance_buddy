# Architecture

Nine markdown files, 1,377 lines, no code. The design work is in what loads
when, what the model is allowed to decide, and what it must hand back.

## Loading model

```
Always loaded        SKILL.md              155 lines
                       ↓  loads on demand
references/          boundaries.md         read first, before acting
                     close-checklist.md    running a close
                     gst-reconciliation.md ITC matching
                     tds-reconciliation.md 26AS / AIS
                     anomaly-detection.md  review checks
                     reporting.md          MIS pack
                     zoho-books.md         connector discipline
assets/              templates.md          output formats
```

Progressive disclosure is not an optimisation here, it is what makes the
depth affordable. `SKILL.md` carries the pipeline and the hard boundaries and
nothing else, so it costs almost nothing on every trigger. The GST file can
then run to 175 lines of matching detail, because it only loads when someone
is actually reconciling GST.

The validator enforces this: 250 lines for `SKILL.md`, 400 per reference. The
moment `SKILL.md` grows into the reference files, every unrelated invocation
starts paying for it.

## Three design decisions

### 1. Confidence banding instead of coverage

The organising constraint is that **accounting errors are silent**. A wrong
categorisation produces a trial balance that ties. Nothing crashes. The error
surfaces at audit, notice or filing — months later, expensively.

That inverts the usual automation objective. Higher coverage is not better if
the added coverage is guessed, because guessed entries look exactly like
correct ones and therefore never get reviewed.

So every match carries a band, and the band determines the action:

| Band | Evidence | Action |
|---|---|---|
| High | Exact agreement on key fields | Auto-apply, log |
| Medium | One field differs, others agree | Suggest, report separately |
| Low | Plausible, weak evidence | Escalate, never apply |
| None | No candidate | Escalate with what was tried |

Medium is reported on its own line, never folded into "matched". That single
formatting decision is what keeps the report honest — a 98% match rate with a
third of it guessed is worse than 85% stated plainly, because the 98% ends
the review.

### 2. Sequence, not calendar

Statutory dates, rates and thresholds change, and penalties attach to getting
them wrong. Encoding them means shipping a liability that ages silently.

What does not change is dependency order:

```
outward return → 2B available → ITC reconciled → summary return + payment
TDS deducted   → deposited    → return filed   → appears in payee's 26AS
```

From that the skill derives the thing that actually matters operationally:
ITC reconciliation must land after 2B is available and before the summary
return is filed, and that window is short. It says to verify the dates each
period rather than asserting them.

The validator warns on anything that looks like a hardcoded due date, rate or
threshold.

### 3. The boundary is rule-application versus rule-selection

`references/boundaries.md` is read first, before anything else runs.

Applying a rule someone else set is mechanical. *Choosing* the rule is
professional judgement with statutory consequence. The skill does the first
and refuses the second — no tax treatment, no rate determination, no
compliance conclusion, no capitalise-versus-expense call, no sign-off.

The refusal is designed to stay useful rather than just decline:

> "I can't tell you the right GST rate — that's an HSN classification
> question with penalty exposure, so it needs your CA. What I can do: this
> vendor has invoiced under three different HSN codes in six months, which
> may be worth asking about. Here are the invoices."

State the limit once, then hand over everything that helps the person who can
make the call.

## Why GST carries the most detail

It is the only reconciliation with direct cash impact. Input tax credit is
generally restricted to what appears in GSTR-2B, so an invoice the vendor has
not reported is credit that cannot be claimed — regardless of holding the
invoice, paying it and receiving the goods.

On a purchase register of a few crore, 2% unmatched is real money.

Two mechanics account for most false mismatches in practice, and both are
handled explicitly:

1. **Invoice-number formatting.** `INV/2024/0001` and `INV-2024-1` are the
   same invoice. Normalise both sides — strip separators, upper-case, drop
   leading zeros, drop the FY segment — match on normalised, report the
   original.
2. **Cross-period drift.** An invoice dated 30 September lands in October's
   2B if the vendor filed late. Single-month reconciliation invents unmatched
   items that resolve themselves next period, and chasing them discredits the
   whole exercise. Reconcile across a window.

## Anomaly detection

The one place where a pattern check clearly beats a human reading 5,000
lines. Duplicates, vendor name variants, round-number entries never trued up,
weekend postings, threshold clustering, sequence gaps, wrong-sign balances,
movement variance against trailing average.

Highest yield is **movement variance**, because it catches errors that
reconcile perfectly. A cost posted to the wrong head still ties; only the
movement review exposes it.

It flags, it does not fix. Every anomaly has an innocent explanation and a
serious one, and distinguishing them is not a pattern-matching problem.

The design constraint on adding checks is dismissal cost. A check that fires
on 200 rows a month is ignored within two closes — and then so is everything
else in the report.

## Connector discipline

Read-first, always. Pull and reconcile before writing anything.

No write without confirmation on the specific action. "Go ahead and fix the
reconciliation" is not authorisation to post twelve journal entries; the
entries are itemised and confirmed as a list. A validation failure is not
worked around by altering the data — the validation exists for a reason.

## Build

```
company-finance-buddy/  →  validate.py  →  build.sh  →  company-finance-buddy.skill
```

The bundle is a deterministic zip: fixed timestamps, sorted entries, no
compression. An unchanged source tree produces a byte-identical artifact, so
the bundle diff in a pull request carries information instead of noise. CI
rebuilds and compares against the committed bundle, which makes a stale
artifact a build failure rather than something discovered after install.
