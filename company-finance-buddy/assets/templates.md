# Templates

Copy-ready formats. Adapt to the entity — a template applied mechanically reads as one.

---

## Close calendar

Working days relative to period end. **Deadlines are pinned to statutory dates that change — verify each period.**

```
CLOSE CALENDAR — [month]

D+0    Cut-off. Lock the period.
D+1    Ingest all sources. Note what's missing.
D+1    Bank reconciliation, all accounts.
D+2    Sales register vs books. Outward return prep.
D+2    TDS: deducted vs deposited. Challan check.
D+3    Purchase register cleaned, vendor names normalised.
D+4    ── 2B available ──  ITC reconciliation.
D+5    Vendor chase list issued.
D+5    Accruals, prepaids, depreciation, forex.
D+6    Trial balance review. Anomaly checks.
D+6    Variance narrative drafted.
D+7    ── Summary return + payment ──
D+8    MIS pack issued.
D+8    Open items log circulated with owners.

VERIFY EACH PERIOD: outward return date · 2B availability
· summary return date · TDS deposit date · TDS return (quarterly)
```

---

## GST ITC reconciliation

```
GST ITC RECONCILIATION — [period]
Prepared [date] · Source: purchase register [ref] · GSTR-2B [download date]

                        Count      Taxable            ITC
Purchase register         486    1,24,80,000     22,46,400
GSTR-2B                   441    1,18,20,000     21,27,600
                        ─────    ───────────     ─────────
Matched — high            412    1,10,40,000     19,87,200
Matched — medium ⚠         29       7,80,000      1,40,400
Unmatched — books          45       6,60,000      1,18,800  ← at risk
Unmatched — 2B              0              —             —
RCM excluded               12       5,20,000             —

MEDIUM CONFIDENCE — review before claiming
  #  Vendor          GSTIN            Invoice     Books      2B        Note
  1  Anant Ent.      27AAAA1111A1Z5   AE/24/882   2,08,500   2,08,500  date +2d
  2  Krishna Tr.     27BBBB2222B2Z6   KT-4471     1,45,000   1,45,000  inv fmt

UNMATCHED — not in 2B · vendor chase list
  Vendor              Invoice      Date      Taxable      ITC       Status
  Anant Enterprises   AE/24/901    18 Aug   2,10,000    37,800    chase 1
  Krishna Traders     KT-4488      22 Aug   1,45,000    26,100    chase 2
  Sharma & Co         SC/2024/33   29 Aug     92,000    16,560    new

TOTAL ITC AT RISK: ₹1,18,800
```

**Lead with rupees at risk.** Invoice counts don't drive action.

---

## Bank reconciliation

```
BANK RECONCILIATION — [account] — [period]

Balance per bank statement                        18,42,600
  Add:  deposits in transit                    (3)   2,40,000
  Less: unpresented cheques                    (7)  (1,82,400)
  Less: bank error — [ref]                             (12,000)
                                                   ──────────
Adjusted bank balance                              18,88,200

Balance per books                                  18,94,400
  Less: bank charges not booked                        (1,240)
  Add:  interest credited not booked                    4,960
  Less: [unexplained — see below]                     (10,000)
                                                   ──────────
Adjusted book balance                              18,88,200   ✓

UNEXPLAINED — 1 item
  31 Aug · ₹10,000 · "IMPS/PQR/889201" · no matching entry
  → escalated to [owner]

UNPRESENTED CHEQUES — ageing
  #  Cheque    Date      Payee            Amount    Days
  1  004471    12 Jun    Vertex Supply     42,000    80  ← stale
  2  004488    28 Aug    Krishna Traders   65,000     3
```

**Age the unpresented cheques.** Anything past 90 days needs a decision.

---

## Open items log

```
OPEN ITEMS — [period]

#  Item                                  Owner   Value       Since   Age
1  Anant Ent. invoice not in 2B          Purch.  ₹37,800     Aug     8d
2  Meridian TDS not in 26AS              AR      ₹28,400     Jul     39d  ⚠
3  Inventory variance, Warehouse 2       Ops     ₹1,12,000   Aug     6d
4  4 payments, no TDS — confirm          CA      ₹2,84,000   Aug     4d
5  Unexplained bank debit ₹10,000        Fin     ₹10,000     Aug     2d

AGED OVER 30 DAYS: 1 item, ₹28,400
```

**Age everything, flag anything over 30 days.** Age is what turns a list into a priority.

---

## Accrual schedule

```
ACCRUALS — [period]

Item                     Amount      Basis                      Reverses
Audit fee              3,50,000      actual — invoice recd      on payment
Electricity               42,000     EST · 3-month average      on invoice
Legal — Sharma & Co     1,20,000     EST · engagement letter    on invoice
Freight                   38,000     actual — GRN 4471          on invoice
                       ──────────
                       5,50,000      of which EST: 1,62,000

PRIOR PERIOD REVERSED
Electricity — Jul         38,000     actual came in at 41,200 (+3,200)
```

**Show prior-period accuracy.** An accrual consistently off by 20% needs its basis revisited.

---

## Anomaly summary

```
ANOMALY REVIEW — [period]

DUPLICATE CANDIDATES (2) — ₹1,72,000
  Sharma & Co    ₹1,45,000   12 & 19 Aug   no invoice ref on either
  Krishna Tr.    ₹  27,000   03 & 04 Aug   same amount

MOVEMENT OUTSIDE ±30% (3)
  Professional fees   +302%   ₹4,82,000 vs avg ₹1,20,000   audit fee?
  Repairs             +517%   ₹2,10,000 vs avg ₹  34,000   UNEXPLAINED
  Travel               -80%   ₹  18,000 vs avg ₹  92,000   UNEXPLAINED

WRONG-SIGN BALANCES (4) — ₹3,84,000
  Debit balances in creditors — advances misposted?

NEW VENDORS (7)
  ⚠ Vertex Supply — ₹2,40,000 paid 3 days after creation

VENDOR NAME VARIANTS (3 groups)
  "ABC Pvt Ltd" / "ABC Private Limited"  — same GSTIN, 2 ledgers
```

---

## MIS header

Goes on **every page** — people circulate single sheets.

```
[Entity] · Management Accounts · [period]
Basis: PROVISIONAL · 5 items open (₹4,72,200) · 3 accruals estimated (₹1,62,000)
Prepared [name] [date] · Not audited · Not reviewed by CA
```

---

## Vendor chase email

```
Subject: GST invoice not reflecting in our 2B — [invoice no.]

Hi [name],

Invoice [number] dated [date] for ₹[amount] isn't appearing in our
GSTR-2B for [period]. We're unable to claim input credit of ₹[ITC]
until it does.

Could you confirm whether it's been included in your GSTR-1 filing
for the period?

If it was filed late it should appear next period — just let us know
so we can track it accordingly.

Thanks,
[name]
```

**Name the ITC amount.** It's the number that gets it actioned.
