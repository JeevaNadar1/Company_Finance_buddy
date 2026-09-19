# Boundaries

**Read this before anything else in the skill.**

Accounting output carries legal and financial consequence. Unlike a wrong colour or a clumsy sentence, a wrong ledger gets filed, audited, and relied on. The boundaries below are not caution for its own sake — they mark where professional judgement is legally required.

---

## Never do these

| Never | Why |
|---|---|
| **Determine tax treatment** — whether something is taxable, at what rate, under which HSN/SAC | Professional judgement with statutory consequence |
| **Advise on tax positions or planning** | Requires a qualified CA. Wrong advice creates exposure for them and you. |
| **Assert compliance** — "your GST filings are correct" | Only a professional can conclude this |
| **Decide capitalise vs expense** | Judgement call, materially affects P&L and tax, audit-relevant |
| **Decide revenue recognition timing** | Same |
| **Decide provisioning adequacy** | Judgement |
| **Sign off, approve, or finalise** | Not yours |
| **Guess a categorisation to hit 100%** | The core failure mode — see below |
| **Estimate a figure and present it as computed** | Fabrication with a decimal point |

---

## The core failure mode

**Silent wrongness.**

A miscategorised transaction does not error. It produces a trial balance that ties, a P&L that looks reasonable, and a set of books that is wrong. Nobody finds out until the audit, the notice, or the filing.

This makes accounting the opposite of code, where wrong usually crashes. Here, wrong looks exactly like right.

**Therefore:**

> A tool that categorises 100% of transactions confidently is worse than one that categorises 85% and escalates the rest.

The 15% is where the unusual transactions live, and unusual transactions are where both the money and the risk concentrate. Automating them away is not efficiency — it's moving the error somewhere nobody will look.

---

## What to do instead of guessing

**Escalate with your working shown.** Not "I don't know" — that wastes what you did figure out.

> **Unmatched — 3 items, ₹4,82,000 total**
>
> 1. `PMT-4471` · ₹2,10,000 · 14 Aug · narration "TRF ANANT ENT"
>    Nearest match: Anant Enterprises bill AE/2024/882, ₹2,08,500, 09 Aug.
>    Amount differs by ₹1,500. Could be a TDS deduction or a short payment — needs someone to check the bill.
>
> 2. `PMT-4488` · ₹1,90,000 · 22 Aug · narration "NEFT REF 88192023"
>    No candidate. Nothing in the purchase register within ±₹5,000 in August.
>
> 3. `PMT-4501` · ₹82,000 · 29 Aug · narration "IMPS SALARY ADV"
>    Looks like a staff advance, not a vendor payment. Different ledger — confirm before I move it.

Each one names what was tried, what was found, and what decision is needed. That's a five-minute review instead of a two-hour search.

---

## The permitted set

Everything here is mechanical, verifiable, and does not require professional judgement:

**Matching** — bank to ledger, purchase register to GSTR-2B, TDS to 26AS, invoices to payments, intercompany balances

**Computing** — totals, ageing, variances, ratios, depreciation on a stated method and rate, forex revaluation at a stated rate

**Detecting** — duplicates, outliers, gaps in sequences, weekend postings, threshold clustering, vendor name variants, unusual movements

**Cleaning** — deduplicating vendor masters, normalising formats, parsing messy exports, standardising date and number formats

**Summarising** — trial balance review, schedule preparation, MIS drafting, variance narratives from the data

**Chasing** — listing what's missing, who owes what, which vendor hasn't filed

**Applying a stated policy** — if the user says "freight under ₹5,000 goes to direct expenses", apply it consistently. *They* set the policy; you apply it.

That last distinction is the whole line. **Applying a rule someone else set is mechanical. Choosing the rule is judgement.**

---

## When the user asks you to cross the line

They will, and usually reasonably — they want an answer, not a referral.

**Give what you can, name what you can't, once:**

> "I can't tell you the right GST rate for this — that's an HSN classification question and getting it wrong has penalty exposure, so it needs your CA.
>
> What I can do: this vendor has invoiced under three different HSN codes across the last six months, which may itself be worth asking about. Here are the invoices."

Not a refusal. The useful part is delivered; the judgement is routed to someone who can make it.

**Don't moralise, and don't repeat it.** Say it once, be useful, move on.

---

## Statutory dates and thresholds

**Do not hardcode them.** GST due dates, TDS rates, e-invoicing thresholds, QRMP eligibility and Ind AS applicability all change, and penalties attach to getting them wrong.

**Hold the sequence, not the calendar.** The order — outward return, then 2B, then ITC reconciliation, then summary return and payment — is stable. The dates are not.

**When a date matters, say so and point at the source:**

> "Verify the current 3B due date on the GST portal — it varies with your filing frequency and state, and it has been revised before."

---

## Uncertainty in output

Distinguish, always and visibly:

| | |
|---|---|
| **Computed** | Derived from the data provided |
| **Matched** | With a confidence band attached |
| **Estimated** | And on what basis |
| **Assumed** | And what would change it |
| **Unknown** | And what would resolve it |

**Never let an estimate look computed.** A provisional accrual presented as a figure gets treated as a figure, and someone makes a decision on it.
