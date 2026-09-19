# Expected output

What a correct run produces against the fixtures in this directory. Wording
will vary. The numbers, the banding and the escalations should not.

---

## GST ITC reconciliation — August 2026

```
                          Count       Taxable            ITC
Purchase register            12     16,19,500       2,61,290
GSTR-2B                      11     14,30,500       2,36,890

Matched — high                6      7,65,500       1,17,190
Matched — medium ⚠            2      4,65,000         83,700
Low confidence — review       2      1,37,000         24,660
Unmatched — books             2      2,52,000         35,740   ← ITC at risk
Unmatched — 2B                1        63,000         11,340   ← missing entry
```

**₹35,740 of credit is at risk** because two vendors have not reported. That
is the line that drives action; the invoice counts do not.

### Matched — high confidence (auto-apply)

| Books | Vendor | Invoice | Taxable | ITC | Tier |
|---|---|---|---|---|---|
| PR-0001 | Anant Enterprises | ANT/2026-27/0114 | 2,10,000 | 37,800 | 1 |
| PR-0003 | Meridian Packaging | MP/8821 | 88,000 | 10,560 | 1 |
| PR-0004 | Sunrise Logistics | SL-2026-0442 | 56,000 | 2,800 | 2 |
| PR-0006 | Orbit Stationers | OS/2026/0033 | 12,500 | 2,250 | 1 |
| PR-0008 | Meridian Packaging | MP/8847 | 1,34,000 | 16,080 | 1 |
| PR-0012 | Vertex Components | VC/26/1243 | 2,65,000 | 47,700 | 1 |

`PR-0004` matched on tier 2 — the 2B date is 09 August against a books date
of 08 August. GSTIN, invoice number and value all agree, so a one-day
difference is a posting-date difference, not a different invoice.

### Matched — medium confidence (suggest, flag for review)

| Books | Invoice in books | Invoice in 2B | Taxable | ITC | Tier | Why medium |
|---|---|---|---|---|---|---|
| PR-0002 | KT-2026-0007 | KT/2026/07 | 1,45,000 | 26,100 | 3 | Same invoice after normalisation — separators stripped, leading zeros dropped |
| PR-0005 | VC/26/1180 | VC/26/1I80 | 3,20,000 | 57,600 | 4 | Invoice numbers differ by one character; GSTIN, value and date all agree |

These are reported separately. Folding them into "matched" is the move that
makes the whole report unusable, because the 98% figure then never gets
reviewed.

### Low confidence — escalated, not applied

**`PR-0007` · Anant Enterprises · ₹96,000 · ITC ₹17,280 · 14 Aug**

> Nearest 2B entry: same GSTIN, same value ₹96,000, invoice `ANT-121-A`
> dated 29 July. Books show `ANT/2026-27/0121` dated 14 August.
> Value and vendor agree; the invoice number does not normalise to the same
> string and the dates are 16 days apart. Could be the same invoice reported
> under the vendor's internal reference, or a different invoice of the same
> value. **Needs the physical bill checked.** Not applied.

**`PR-0011` · Deccan Hardware · ₹41,000 · ITC ₹7,380 · 25 Aug**

> The books row has no GSTIN. A 2B entry from `27AAJCD6677M1Z3` matches on
> value and sits one day later. Matching on value and date alone, with no
> GSTIN on either side of the key, is the weakest evidence available.
> **Confirm the vendor's registration and update the master.** Not applied.

Tiers 5 and 6 never auto-apply. A false positive here means claiming credit
the entity is not entitled to, which is not a reconciliation error — it is an
exposure.

### Unmatched in books — ITC at risk ₹35,740

| Vendor | Invoice | Date | Taxable | ITC | Action |
|---|---|---|---|---|---|
| Krishna Traders | KT-2026-0019 | 20 Aug | 1,78,000 | 32,040 | Chase — vendor has not reported |
| Sunrise Logistics | SL-2026-0501 | 22 Aug | 74,000 | 3,700 | Chase |

Both are late in the month, so check next period's 2B before treating either
as a genuine non-filing. Cross-period drift resolves a large share of these
on its own.

### Unmatched in 2B — missing purchase entry

`PPS/2026/214` · Pinnacle Print Solutions · `27AAKCP8899N1Z6` · 19 Aug ·
taxable ₹63,000 · ITC ₹11,340.

Present in 2B, absent from the books. Either the invoice was never booked or
it sits under a different vendor master. Expense is understated and the
credit is unclaimed. This is the direction of error people check least often.

---

## TDS reconciliation — Q2 FY2026-27

```
                              Count      TDS
Books (receivable)                5    62,800
26AS                              5    59,440
Difference                             3,360
```

| Case | Books | 26AS | Gap | Read |
|---|---|---|---|---|
| Northgate Foods | 3,600 | 3,240 | 360 | Base or rate difference — confirm which section and whether GST was included in the base |
| Ridgeline Capital | 15,000 | — | 15,000 | Deducted per books, not visible in 26AS. Deposit or filing pending. **Chase the deductor** |
| Lattice Media | — | 12,000 | (12,000) | Q1 credit appearing now. Recognise it; not an error |

Reconciles: `360 + 15,000 − 12,000 = 3,360`.

Only the Ridgeline item is cash at stake. Credit that does not appear in 26AS
is credit that cannot be taken, regardless of what the books say.

---

## Bank and anomalies

**Duplicate payment — flag, do not net off.**

> `BK-0007` and `BK-0008` · ₹2,10,000 each · 14 Aug · narration
> `TRF ANANT ENT` · **same UTR `N026224551900` on both lines**.
>
> An identical UTR on two lines usually means the bank reported one payment
> twice, not that two payments went out. But "usually" is not a basis for
> removing ₹2,10,000 from the books. Confirm against the bank portal, then
> reverse whichever side is wrong.

**Vendor master duplicate.**

> *Meridian Packaging Pvt Ltd* (`PR-0003`) and *Meridian Packaging Private
> Limited* (`PR-0008`) share GSTIN `27AAECM9012H1Z8`. One vendor, two ledger
> accounts, two ageing lines, and a payables balance that looks smaller than
> it is on both. Merge the masters.

**Cut-off.**

> `BK-0015` · cheque 004417 · ₹62,000 · presented 31 Aug. Confirm the issue
> date. A cheque issued in July and presented on the last day of August is a
> reconciling item in July, not an August payment.

**Statement ties.** Opening ₹44,00,000, closing ₹34,49,760, every line
accounted for.

---

## What a wrong run looks like

Useful as a test, because each of these is a plausible failure:

1. Reporting **10 of 12 matched** by folding tiers 5 and 6 into the matched
   count. The number improves and the report becomes worthless.
2. Auto-applying `PR-0011` because the value and date line up. No GSTIN on the
   books side means there is no key — only a coincidence of amount.
3. Leading with invoice counts instead of ₹35,740 at risk.
4. Netting the duplicate payment off the bank balance to make the
   reconciliation close.
5. Treating the Lattice Media 26AS credit as an error because it is not in
   the current month's books.
6. Saying anything about whether the ITC position is *compliant*. The skill
   reconciles; it does not conclude.
