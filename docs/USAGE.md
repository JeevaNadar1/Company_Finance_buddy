# Usage

## Install

Claude → Settings → Capabilities → Skills → Upload → `company-finance-buddy.skill`.

The skill triggers on its own description. Closing a month, reconciling ITC,
chasing unmatched invoices, reviewing a trial balance, or uploading a purchase
register, 2B JSON or 26AS will all fire it. You do not need to name it.

## Before the first run

Tell it three things once, at the start of a close. They determine most of
what it does afterwards, and it cannot infer any of them.

1. **Entity and period.** "Single entity, Maharashtra, GSTIN starts 27,
   closing August 2026, FY 2026-27."
2. **Your standing policies.** Anything that is a rule someone already set —
   "freight under ₹5,000 goes to direct expenses", "we accrue utilities on
   a two-month lag", "capex threshold is ₹50,000". It will apply these
   consistently. It will not invent them, and it will not decide them for you.
3. **Where the data comes from.** Zoho Books connected, or file uploads, or
   both. Reconciling Zoho against Zoho proves nothing — 2B and 26AS have to
   come from the portals.

## A close, in order

The sequence matters more than the individual steps, because most of them
have a dependency that makes doing them early a waste.

### 1. Cut-off

Ask for the cut-off review first. Goods received not invoiced, invoices dated
in the period but booked after, cheques issued in the prior month presented in
this one. Everything downstream inherits whatever the cut-off gets wrong.

### 2. Bank reconciliation

Upload the statement and the bank ledger. It auto-matches the obvious, then
ages what is left. What you are looking for in the remainder is not the count
— it is anything old. A three-month-old unreconciled item is either an error
nobody owns or a transaction that never happened.

### 3. GST ITC reconciliation

**Wait until 2B is available.** Running this before is the most common wasted
hour in an Indian close.

Upload the purchase register and the 2B extract. Ask for the reconciliation
across a window rather than the single month — an invoice dated 30 August can
appear in September's 2B if the vendor filed late, and single-month matching
will report it as unmatched and send you chasing a vendor who did nothing
wrong.

Read the output in this order:

1. **Rupees at risk** — unmatched in books. That is credit you cannot claim.
2. **Unmatched in 2B** — invoices you have not booked. Understated expense.
3. **Low-confidence escalations** — usually two or three, five minutes each.
4. **Medium-confidence matches** — scan, approve or reject as a batch.

Then chase. Ask for the chase list grouped by vendor; `assets/templates.md`
has the email format.

### 4. TDS

Both directions. TDS you deducted and deposited, and TDS deducted by your
customers as it appears in 26AS or AIS.

The three buckets that come out are not the same problem and should not be
handled together: a rate or base difference is an adjustment, a credit missing
from 26AS is a chase, and a credit in 26AS with nothing in books is usually a
prior-period item surfacing late.

### 5. Ledger scrutiny and anomalies

Ask for the anomaly pass over the full trial balance. Duplicates, vendor name
variants, wrong-sign balances, round numbers never trued up, movement variance
against the trailing average.

Movement variance earns the most attention, because it is the only check that
catches an error which reconciles perfectly. A cost in the wrong head still
ties.

Everything it returns is a flag, not a finding. It surfaces; you decide.

### 6. Accruals, provisions, schedules

Provide the policy, get the computation. Ask for the supporting schedules —
fixed assets, prepaid, ageing — as a set rather than one at a time.

### 7. MIS pack

Ask last, once the items above are closed or logged as open. You get the
schedules, the ageing, the variance narrative and an open-items log. The open
items are the most useful part of the pack, because they are what the next
close inherits.

## Working with it well

**Give it the rule, not the answer.** "Anything under ₹5,000 to direct
expenses" gets applied consistently to 400 rows. "Is this capex?" gets a
correct refusal.

**Treat medium-confidence as a review queue, not as matched.** It is
separated for a reason. Approving the batch without reading it removes the
only safeguard the banding provides.

**Escalations are the output, not a failure.** Roughly fifteen percent will
come back unresolved. That fifteen percent is where the unusual transactions
are, which is where both the money and the risk sit. A run that escalated
nothing on a real ledger is a run that guessed.

**Give it the previous month's open-items log.** Half of any close is the
prior close's unfinished business.

## Where it stops

It will not determine a tax treatment or rate, advise on a tax position,
state that a filing is compliant, decide capitalise versus expense, decide
revenue-recognition timing, or sign anything off. Those need a qualified CA,
and the exposure for getting them wrong is statutory.

When you ask for one of those, it says so once and then hands over whatever
helps the person who can make the call — the invoices, the pattern, the
inconsistency it noticed. That is the useful version of a refusal.

## Zoho Books

Where connected, it reads first and reconciles before writing anything.

Writes require confirmation on the specific action. Approving "fix the
reconciliation" does not authorise twelve journal entries — it will itemise
them and ask for a yes on the list. Say no to individual lines; that is what
the itemisation is for.

For reconciliation-only work, a read-only credential is the better setup.

## Verify the statutory position each period

ITC restriction mechanics, claim time limits, treatment of late-filed
invoices, e-invoicing thresholds and QRMP eligibility have all been revised
more than once. The skill deliberately holds the sequence, not the calendar.
Confirm the current position rather than assuming last year's rules hold.
