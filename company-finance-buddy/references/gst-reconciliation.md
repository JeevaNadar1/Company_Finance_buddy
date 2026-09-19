# GST Reconciliation

The biggest time sink in an Indian close, and the only reconciliation with direct cash impact.

---

## Why this one matters most

Input tax credit is generally restricted to invoices appearing in your GSTR-2B. If a vendor hasn't reported an invoice, **you cannot claim that credit in the period** — regardless of whether you have the invoice, paid it, and received the goods.

That's working capital, not bookkeeping. On a purchase register of a few crore, unmatched ITC of even 2% is real money sitting unclaimed.

**GSTR-2B is static.** Generated once for a period, it doesn't change afterwards. That's what makes it reconcilable — unlike the dynamic view, which shifts under you.

---

## The two reconciliations

**Inward — purchase register vs GSTR-2B.** Determines claimable ITC. The hard one.

**Outward — sales register vs GSTR-1 vs books.** Confirms what you reported matches what you booked. Easier, but a mismatch here surfaces in departmental scrutiny.

Both matter. Inward is where the time goes.

---

## Matching keys, in order

Match on progressively looser criteria. Report which tier each match came from.

| Tier | Keys | Confidence |
|---|---|---|
| 1 | GSTIN + invoice no. + date + taxable value | **High** — exact |
| 2 | GSTIN + invoice no. + taxable value (date differs) | **High** |
| 3 | GSTIN + normalised invoice no. + value | **Medium** |
| 4 | GSTIN + value + date within ±7 days | **Medium** |
| 5 | GSTIN + value only | **Low — escalate** |
| 6 | Value + date, no GSTIN match | **Low — escalate** |

**Never auto-apply tiers 5 and 6.** Value-only matching produces false positives on round amounts, and a false positive here means claiming credit you aren't entitled to.

---

## Invoice number normalisation

The single largest source of false mismatches. Vendors format inconsistently, and the same invoice appears differently in your register than in their filing.

**Normalise both sides before comparing:**

- Strip spaces, hyphens, slashes → `INV/2024/001` and `INV-2024-001` and `INV 2024 001` collapse to `INV2024001`
- Upper-case everything
- Strip leading zeros in numeric segments → `INV/2024/0001` vs `INV/2024/1`
- Strip the financial-year segment where present → `AE/24-25/882` vs `AE/882`
- Compare the trailing numeric portion as a fallback

**Match on normalised, report the original.** Never rewrite the user's data — show what matched to what, in the form each side actually holds it.

---

## Date drift across periods

Common and routinely mishandled.

**An invoice dated 30 September may appear in October's 2B** if the vendor filed late. It's a September invoice for your books and an October credit for GST.

**Reconcile across a window, not a single month.** Pull two or three periods of 2B and match against a purchase register covering the same span. Single-month matching generates false unmatched items that resolve themselves next period, and chasing them wastes the whole exercise.

**Track the timing difference separately** from genuine mismatches. They need different follow-ups:

| Category | Follow-up |
|---|---|
| In books, in 2B | Claim |
| In books, not in 2B — vendor filed late | Wait; claim next period |
| In books, not in 2B — vendor hasn't filed | **Chase the vendor** |
| In 2B, not in books | Missing bill — find it or query |
| Value mismatch | Query the vendor |
| GSTIN mismatch | Master data error, either side |

---

## Splitting the unmatched

An unmatched list is only actionable once it's split by cause. Each bucket has a different owner and a different action.

**In books, not in 2B** — by far the most valuable output. Sort by value descending; this is your vendor-chase list. A single large unreported invoice is worth more attention than fifty small ones.

**In 2B, not in books** — either a bill you haven't received or booked, or a supply that isn't yours. Both need checking. The second is rarer and more serious.

**Value mismatches** — usually a rate difference, a discount applied one side only, or a rounding difference. Report the delta, not just the flag.

**GSTIN mismatches** — a wrong GSTIN in your master, or the vendor filing under a different registration. Common with multi-state vendors.

---

## What to report

```
GST ITC RECONCILIATION — [period]

Purchase register     486 invoices    ₹1,24,80,000    ITC ₹22,46,400
GSTR-2B               441 invoices    ₹1,18,20,000    ITC ₹21,27,600

Matched (high)        412             ₹1,10,40,000    ITC ₹19,87,200
Matched (medium)       29  ← review     ₹7,80,000     ITC ₹1,40,400
Unmatched — books      45              ₹6,60,000      ITC ₹1,18,800  ← at risk
Unmatched — 2B          0

TOP UNCLAIMED (vendor not filed)
  Anant Enterprises      ₹2,10,000    ITC ₹37,800
  Krishna Traders        ₹1,45,000    ITC ₹26,100
  Sharma & Co            ₹  92,000    ITC ₹16,560
```

**Lead with ITC at risk in rupees.** That's the number that gets someone to act. Invoice counts don't.

**Always show the medium-confidence count separately.** Folding it into "matched" is the dishonest move that makes the report useless.

---

## Reverse charge

**RCM supplies won't appear in 2B as claimable ITC in the ordinary way** — the liability and the credit both sit with you.

Identify RCM items in the purchase register and **exclude them from the 2B matching population** before reconciling. Leaving them in generates a block of false unmatched items every single period.

Which supplies attract RCM is a tax determination — **not yours to make.** Work from the classification already in the books, or ask.

---

## Ineligible credit

Some ITC is blocked regardless of whether it appears in 2B.

**Whether a specific item is blocked is a tax determination.** Do not classify. Work from the flag already in the purchase register, and if there isn't one, report the items unclassified rather than assuming they're all claimable.

Presenting blocked credit as claimable inflates the ITC figure someone then relies on.

---

## Practical notes

**Get 2B as JSON where possible.** The Excel export loses precision on long invoice numbers and mangles some date formats.

**Reconcile monthly, not at year end.** Vendor chasing has a shelf life — a vendor who hasn't filed for eight months is a much harder conversation than one who missed last month.

**Keep the working.** Which invoice matched to which, at what tier. When a notice arrives eighteen months later, the reconciliation working is the answer.

**Verify current rules.** ITC restriction mechanics, time limits for claiming, and the treatment of late-filed invoices have all been revised. Confirm the current position with your CA rather than assuming what held last year still holds.
