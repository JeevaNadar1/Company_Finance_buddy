# Company Finance Buddy

A Claude Skill for Indian month-end close — GST reconciliation, TDS matching, anomaly detection and the MIS pack.

> A tool that categorises 100% of transactions confidently is worse than one that does 85% and escalates the rest.

<sub>Claude Skill · 9 files · 1,377 lines · India / GST / Ind AS · MIT</sub>

---

## Why this one is built differently

Most automation tries to maximise coverage. This deliberately doesn't, for one reason:

**Accounting errors are silent.**

A miscategorised transaction doesn't throw an error. It produces a trial balance that ties, a P&L that looks reasonable, and a set of books that's wrong. Nobody finds out until the audit, the notice, or the filing.

That makes it the opposite of code, where wrong usually crashes. Here, wrong looks exactly like right.

So the design centre isn't automation — it's **confidence banding and honest escalation**. The 15% it won't touch is where unusual transactions live, and unusual transactions are where both the money and the risk concentrate.

## What it does

| | |
|---|---|
| **GST ITC reconciliation** | Purchase register vs GSTR-2B, six matching tiers, invoice-number normalisation, cross-period handling |
| **TDS reconciliation** | Books vs 26AS/AIS both directions, mismatch bucketing, chase lists |
| **Bank reconciliation** | Auto-match the obvious, surface and age the rest |
| **Anomaly detection** | Duplicates, vendor variants, wrong-sign balances, movement variance, threshold clustering |
| **Close sequencing** | Dependency-ordered checklist, cut-off through reporting |
| **MIS pack** | Schedules, ageing, variance narrative, open-items log |
| **Zoho Books** | Read-first, write only on itemised confirmation |

## GST is the centrepiece

It's the only reconciliation with **direct cash impact**. Input tax credit is generally restricted to what appears in your GSTR-2B — an invoice your vendor hasn't reported is credit you can't claim, regardless of holding the invoice, paying it, and receiving the goods.

On a purchase register of a few crore, unmatched ITC of even 2% is real money sitting unclaimed.

**Six matching tiers**, from exact-key down to value-only:

| Tier | Keys | Confidence |
|---|---|---|
| 1 | GSTIN + invoice no. + date + value | High — exact |
| 2 | GSTIN + invoice no. + value | High |
| 3 | GSTIN + normalised invoice no. + value | Medium |
| 4 | GSTIN + value + date ±7d | Medium |
| 5 | GSTIN + value only | **Low — escalate** |
| 6 | Value + date, no GSTIN | **Low — escalate** |

Tiers 5 and 6 **never auto-apply**. A false positive there means claiming credit you aren't entitled to.

### Two things that cause most real-world false mismatches

**Invoice number formatting.** `INV/2024/0001` and `INV-2024-1` are the same invoice. The skill normalises both sides — strip separators, upper-case, drop leading zeros, drop the FY segment — matches on normalised, and reports the original.

**Cross-period drift.** An invoice dated 30 September appears in October's 2B if the vendor filed late. Single-month reconciliation generates false unmatched items that resolve themselves next period, and chasing them wastes the whole exercise. This reconciles across a window.

### What the output looks like

```
GST ITC RECONCILIATION — August

                      Count      Taxable            ITC
Purchase register       486    1,24,80,000     22,46,400
GSTR-2B                 441    1,18,20,000     21,27,600

Matched — high          412    1,10,40,000     19,87,200
Matched — medium ⚠       29       7,80,000      1,40,400
Unmatched — books        45       6,60,000      1,18,800  ← at risk

TOP UNCLAIMED (vendor not filed)
  Anant Enterprises     ₹2,10,000    ITC ₹37,800
  Krishna Traders       ₹1,45,000    ITC ₹26,100
```

**Leads with rupees at risk.** Invoice counts don't drive action. And medium-confidence is always shown separately — folding it into "matched" is the dishonest move that makes a report useless.

## Confidence over coverage

| Band | Action |
|---|---|
| **High** — exact match on key fields | Auto-apply, log it |
| **Medium** — one field differs | Suggest, flag for review |
| **Low** — plausible, weak evidence | **Escalate. Never auto-apply.** |
| **None** | **Escalate with what was tried** |

A reconciliation reporting 98% matched with a third of those guessed is worse than one reporting 85% honestly — because the 98% won't get reviewed.

**When it can't match, it escalates with the working shown:**

> `PMT-4471` · ₹2,10,000 · 14 Aug · "TRF ANANT ENT"
> Nearest match: Anant Enterprises bill AE/2024/882, ₹2,08,500, 09 Aug.
> Amount differs by ₹1,500. Could be a TDS deduction or a short payment — needs someone to check the bill.

Five-minute review instead of a two-hour search.

## What it will never do

| Never | Why |
|---|---|
| Determine tax treatment or rate | Professional judgement with statutory consequence |
| Advise on tax positions | Requires a qualified CA |
| Assert that filings are compliant | Only a professional can conclude that |
| Decide capitalise vs expense | Judgement, audit-relevant |
| Decide revenue recognition timing | Same |
| Sign off or finalise anything | Not its call |
| Guess a categorisation to hit 100% | The core failure mode |

**The line it draws:** applying a rule someone else set is mechanical. *Choosing* the rule is judgement.

If you say "freight under ₹5,000 goes to direct expenses", it applies that consistently. It won't decide the policy for you.

When you ask it to cross the line, it says so once and stays useful:

> "I can't tell you the right GST rate — that's an HSN classification question with penalty exposure, so it needs your CA. What I can do: this vendor has invoiced under three different HSN codes in six months, which may be worth asking about. Here are the invoices."

## No hardcoded dates

GST due dates, TDS rates, e-invoicing thresholds and QRMP eligibility all change, and penalties attach to getting them wrong.

**The skill holds the sequence, not the calendar:**

```
Outward return  →  2B available  →  ITC reconciled  →  summary return + payment
TDS deducted    →  deposited     →  return filed    →  appears in payee's 26AS
```

That's stable. The dates aren't, and it tells you to verify them each period.

What the sequence tells you regardless: ITC reconciliation must happen *after* 2B is available and *before* the summary return is filed. **That window is the pressure point in every Indian close, and it's short.**

## Anomaly detection

Where AI genuinely beats manual review — a person scanning 5,000 lines misses what a pattern check doesn't.

Duplicate payments · vendor name variants (`ABC Pvt Ltd` vs `ABC Private Limited` — one vendor, two ledgers, two sets of ageing) · round-number entries never trued up · weekend postings · threshold clustering · sequence gaps · wrong-sign balances · movement variance vs trailing average.

**It flags, it doesn't fix.** Every anomaly has an innocent explanation and a serious one. Surfacing it is the contribution; deciding is not.

The highest-yield check is **movement variance**, because it catches errors that reconcile perfectly. A cost posted to the wrong head still ties — only the movement review shows it.

## Zoho Books

Read-first, always. Pull and reconcile before writing anything back.

**No write without confirmation on the specific action.** "Go ahead and fix the reconciliation" is not authorisation to post twelve journal entries — it shows the proposed entries itemised and gets a yes on the list.

It also won't work around a validation failure by altering the data. The validation exists for a reason.

## What's inside

```
company-finance-buddy/
├── SKILL.md                        the close pipeline + hard boundaries
├── references/
│   ├── boundaries.md               read first — what it must never do
│   ├── close-checklist.md          dependency-ordered close
│   ├── gst-reconciliation.md       ITC matching against 2B
│   ├── tds-reconciliation.md       26AS / AIS matching
│   ├── anomaly-detection.md        review checks
│   ├── reporting.md                MIS pack and schedules
│   └── zoho-books.md               connector discipline
└── assets/
    └── templates.md                recon formats, close calendar, chase email
```

Progressive disclosure — only `SKILL.md` loads on every trigger.

## Install

Settings → Capabilities → Skills → Upload, then select `company-finance-buddy.skill`.

Triggers on its own description — closing a month, reconciling GST, chasing unmatched invoices, reviewing a trial balance, or uploading a purchase register, 2B JSON or 26AS.

## Limitations

**India-specific.** GST, TDS, 26AS, Ind AS. Not adapted for US GAAP or UK VAT.

**Single entity.** No group consolidation, intercompany elimination or minority interest.

**Not a replacement for a CA.** It reconciles, detects and reports. Every judgement, treatment and sign-off stays with a qualified professional. That's a design decision, not a gap.

**Only as good as the external source.** Reconciling Zoho against Zoho proves nothing. GSTR-2B and 26AS come from the portals.

**Verify statutory positions.** ITC restriction mechanics, claim time limits and late-filed invoice treatment have all been revised. Confirm the current position rather than assuming last year's rules hold.

## License

MIT
