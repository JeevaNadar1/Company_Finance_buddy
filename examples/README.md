# Example fixtures

Synthetic data for August 2026, sized to be read end-to-end rather than to
look realistic in volume. Twelve purchase invoices, eleven 2B entries, five
TDS credits and fifteen bank lines.

Every entity is invented. Every GSTIN, TAN and UTR is structurally shaped but
meaningless. Nothing here is client data.

## Files

| File | What it is |
|---|---|
| `purchase-register-aug2026.csv` | Books-side purchase register, 12 invoices |
| `gstr2b-aug2026.json` | GSTR-2B extract, 11 B2B entries |
| `tds-receivable-books-aug2026.csv` | TDS receivable per books, 5 customers |
| `form26as-q2fy2026-27.csv` | 26AS Part A extract, 5 credits |
| `bank-statement-aug2026.csv` | Current account, 15 lines |
| `expected-output.md` | What a correct run produces against all of the above |

The JSON is shaped like a 2B extract, not a portal-accurate schema. It has
the fields that matter for matching — `ctin`, `inum`, `idt`, `txval`, `rt`,
`camt`, `samt`, `iamt` — and omits the rest.

## What each fixture is engineered to trigger

**GST — one invoice per matching tier, by design.**

1. `PR-0001` Anant — tier 1, everything agrees.
2. `PR-0004` Sunrise — tier 2, 2B date is one day later than the books date.
3. `PR-0002` Krishna — tier 3, books say `KT-2026-0007`, 2B says `KT/2026/07`.
   Same invoice, different formatting. This is the single most common cause
   of a false mismatch in practice.
4. `PR-0005` Vertex — tier 4, the vendor typed `VC/26/1I80` where the books
   say `VC/26/1180`. Capital I for 1. Matches on GSTIN, value and date only.
5. `PR-0007` Anant — tier 5, value matches but the invoice number is
   unrecognisable and the 2B date falls in the prior month. Low confidence.
   **Must escalate, must not auto-apply.**
6. `PR-0011` Deccan — tier 6, the books row has no GSTIN at all. Value and
   date match a 2B entry. **Must escalate.**

Plus the three cases that are not tier problems:

1. `PR-0009` and `PR-0010` appear in the books and not in 2B. This is ITC at
   risk — the vendors have not reported the invoices.
2. `PPS/2026/214` from Pinnacle Print Solutions appears in 2B and not in the
   books. That is a missing purchase entry, and the opposite risk: understated
   expense and unclaimed credit.
3. `PR-0003` and `PR-0008` are the same vendor recorded as
   *Meridian Packaging Pvt Ltd* and *Meridian Packaging Private Limited*.
   Two ledgers, two ageing lines, one vendor. The anomaly pass should catch it.

**TDS.**

1. `TDS-003` Northgate — books hold ₹3,600 against ₹3,240 in 26AS. A base or
   rate difference, not a missing credit.
2. `TDS-005` Ridgeline — in books, absent from 26AS. The deductor has either
   not deposited or not filed. This is a chase, not an adjustment.
3. Lattice Media — in 26AS, absent from books. A Q1 credit surfacing late.
   Recognise it; do not assume it is an error.

**Bank.**

1. `BK-0007` and `BK-0008` — identical narration, identical amount, identical
   UTR, same day. A duplicate payment, or the same payment reported twice by
   the bank. **Flag, do not net off.**
2. `BK-0007` at ₹2,10,000 against Anant's bill of ₹2,10,000 matches cleanly;
   the tier-5 case in the README's worked example is a different, harder
   variant of the same situation.
3. `BK-0015` cheque 004417 presented on 31 August — a cut-off item.

Opening balance is ₹44,00,000 and the statement ties to ₹34,49,760.

## Running them

Attach the purchase register and the 2B JSON to a conversation and ask for the
ITC reconciliation. Compare against `expected-output.md`.

The fixtures exist to test behaviour, not accuracy of arithmetic. The question
is not whether the totals come out right — it is whether tiers 5 and 6 get
escalated instead of quietly matched, and whether medium-confidence matches
are reported separately rather than folded into the matched count.
