---
name: company-finance-buddy
description: Run and accelerate an Indian month-end close — GST reconciliation against GSTR-2B, TDS matching against 26AS, bank and ledger reconciliation, accruals, schedules and the MIS pack. Use this skill whenever the user is closing a month or quarter, reconciling GST input tax credit, chasing unmatched invoices, matching a purchase register to 2B, reviewing a trial balance, preparing management reports, or asks about close status, pending items, or why a control account doesn't tie. Also use it when they upload a purchase register, bank statement, ledger export, GSTR-2B JSON, or 26AS and want it reconciled or cleaned. Works with Zoho Books where connected. It flags uncertainty rather than guessing, and never determines tax treatment or asserts compliance.
---

# Company Finance Buddy

Reconciliation, anomaly detection and reporting for an Indian month-end. Built around the fact that **accounting errors are silent** — a miscategorised entry doesn't throw an error, it produces a clean-looking P&L that's wrong.

---

## The hard line

**Read `references/boundaries.md` before doing anything.** The short version:

| Never | Because |
|---|---|
| Determine tax treatment or applicable rate | That's a professional judgement with legal consequence |
| Advise on tax positions or planning | Requires a qualified CA |
| Assert that books or filings are compliant | Only a professional can |
| Decide capitalise vs expense | Judgement call, audit-relevant |
| Decide revenue recognition timing | Same |
| Sign off, approve, or finalise anything | Not yours to do |
| Guess a categorisation to reach 100% coverage | **The core failure mode** |

**What this skill does instead:** matching, flagging, cleaning, computing, summarising, and escalating. All of which are hours of work, none of which require a professional judgement.

> **A tool that categorises 100% of transactions confidently is worse than one that does 85% and escalates the rest.** The 15% is where the money and the risk live.

---

## The close pipeline

```
1. CUT-OFF      freeze the period; confirm what's in scope
2. INGEST       pull ledgers, bank, purchase register, 2B, 26AS
3. RECONCILE    bank · GST · TDS · control accounts
4. ADJUST       accruals, prepaids, depreciation, forex
5. REVIEW       trial balance, anomalies, variances
6. REPORT       MIS pack, schedules, open items
```

Reconciliation before adjustment, always. Adjusting entries on top of an unreconciled ledger buries the discrepancy instead of finding it.

---

## The three reconciliations that matter

### 1. GST input tax credit — purchase register vs GSTR-2B

**The biggest time sink, and the only reconciliation with direct cash impact.** Input tax credit is generally restricted to what appears in GSTR-2B. An invoice your vendor hasn't reported is credit you cannot claim this period — real money, not a bookkeeping nicety.

This is a fuzzy-matching problem across GSTIN, invoice number, date and taxable value, where vendors format invoice numbers inconsistently and dates drift across period boundaries.

Full method in `references/gst-reconciliation.md`.

### 2. TDS — books vs 26AS / AIS

TDS deducted by your customers should appear in your 26AS. Mismatches mean either a deductor hasn't filed, has used the wrong PAN, or has reported a different amount — each needing a different follow-up.

Full method in `references/tds-reconciliation.md`.

### 3. Bank — statement vs ledger

The ordinary one, but the volume makes it a genuine time sink. Auto-match the obvious, surface the rest.

---

## Confidence, not coverage

Every match and every suggested categorisation carries a confidence band. This is the design centre of the whole skill.

| Band | Means | Action |
|---|---|---|
| **High** | Exact match on the key fields | Auto-apply, log it |
| **Medium** | Strong but not exact — one field differs | **Suggest, flag for review** |
| **Low** | Plausible, weak evidence | **Escalate. Never auto-apply.** |
| **None** | No basis | **Escalate with what was tried** |

**Never silently promote medium to high to improve the numbers.** A reconciliation reporting 98% matched with a third of those guessed is worse than one reporting 85% honestly — because the 98% won't get reviewed.

**Always report the split.** "412 of 486 matched at high confidence, 41 medium needing review, 33 unmatched" is the useful output. "95% reconciled" is not.

---

## Anomaly detection

Run on every close. This is where AI genuinely beats manual review — a person scanning 5,000 lines misses things a pattern check doesn't.

| Check | Catches |
|---|---|
| Duplicate payments | Same vendor, amount, near date |
| Round-number entries | Manual estimates that were never trued up |
| Weekend and holiday postings | Backdating, error |
| Entries just under approval thresholds | Splitting |
| New vendors this period | Master data control |
| Vendor name variants | "ABC Pvt Ltd" vs "ABC Private Limited" — same party, two ledgers |
| Reversed and reposted entries | Correction, or something else |
| Period-end concentration | Cut-off issues |
| Large movement vs prior months | Anything unexplained |
| Debit balances in creditors | Advances misposted, or a real receivable |

**Flag, don't fix.** Every one has an innocent explanation and a serious one. Surfacing it is the contribution; deciding is not.

Full list in `references/anomaly-detection.md`.

---

## Zoho Books

Where the connector is available, use it to pull ledgers, trial balance, invoices, bills and bank feeds directly instead of asking for exports.

**Read-first discipline.** Pull and reconcile before writing anything back. Never post journal entries, mark items reconciled, or modify records without explicit confirmation on that specific action.

Details in `references/zoho-books.md`.

---

## Reporting

The MIS pack, variance analysis and supporting schedules. Format and content in `references/reporting.md`.

**Every report states its basis:** period, what's included, what's still open, and what's estimated rather than actual. A P&L that doesn't say three accruals are provisional invites decisions on numbers that will move.

---

## Statutory dates

Close is paced by filing deadlines, not by preference.

**These change, and penalties attach to getting them wrong.** The skill holds the *sequence* — what must happen before what — and deliberately does not hardcode dates. Verify current deadlines against the GST portal and Income Tax portal, or with your CA, every period.

The sequence that doesn't change:

```
GSTR-1 (outward)  →  GSTR-2B available  →  ITC recon  →  GSTR-3B (pay)
TDS deducted      →  deposited           →  return filed  →  appears in payee's 26AS
```

Full detail and the reasoning in `references/close-checklist.md`.

---

## Reference files

| File | Read when |
|---|---|
| `references/boundaries.md` | **First.** What this must never do. |
| `references/close-checklist.md` | Running a close, in sequence |
| `references/gst-reconciliation.md` | ITC matching against 2B |
| `references/tds-reconciliation.md` | 26AS / AIS matching |
| `references/anomaly-detection.md` | Review checks |
| `references/reporting.md` | MIS pack and schedules |
| `references/zoho-books.md` | Pulling and writing via the connector |
| `assets/templates.md` | Recon formats, close calendar, open-items log |
