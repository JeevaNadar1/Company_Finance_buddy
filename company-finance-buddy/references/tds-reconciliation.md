# TDS Reconciliation

Two directions, two different problems. Both need doing.

---

## TDS receivable — books vs 26AS / AIS

Tax your **customers** deducted from payments to you. You claim it against your liability, so an unreported deduction is cash you've lost.

### The matching problem

| Source | Holds |
|---|---|
| Your books | TDS receivable, by customer, per invoice |
| **26AS** | What deductors have *filed*, by TAN |
| **AIS** | Broader — includes transactions beyond TDS |

**Match on TAN + amount + quarter.** Deductor names differ between your ledger and their filing constantly — match on TAN, display the name.

### The mismatch buckets

| Bucket | Meaning | Action |
|---|---|---|
| In books, not in 26AS | Deductor hasn't filed their return | **Chase.** Most common. |
| In books, not in 26AS | Deductor used the wrong PAN | Chase — needs a correction return |
| Amount differs | Rate applied differently, or partial | Query with the invoice |
| In 26AS, not in books | Deduction you didn't record | Find the payment; book it |
| Quarter differs | Timing | Usually resolves; track separately |

**Wrong-PAN cases are the painful ones.** The deductor has to file a correction return, which they have no urgency about. Catch these early — the longer the gap, the harder the ask.

### What to report

```
TDS RECEIVABLE — [quarter]

Per books        ₹8,42,600
Per 26AS         ₹7,91,400
Difference       ₹  51,200   ← at risk

UNMATCHED — not appearing in 26AS
  Meridian Systems    TAN MUMM01234C    ₹28,400   Q2 invoices ×3
  Cortez Retail       TAN DELC05678F    ₹15,800   Q2 invoice ×1
  Vantage Logistics   TAN BLRV09876A    ₹ 7,000   Q1 — chased twice
```

**Sort by value, flag repeat offenders.** A vendor unmatched three quarters running is a different conversation from a first miss.

---

## TDS payable — deducted, deposited, filed

Tax **you** deducted from vendor payments. Three stages, and each has its own failure.

```
deducted  →  deposited  →  return filed  →  appears in vendor's 26AS
```

### What to check

**Deducted correctly** — every payment attracting TDS had it applied. The reconciliation is: expense ledger movements against TDS deduction entries. Payments to a vendor with no corresponding deduction are the flag.

**Whether a payment attracts TDS, and at what rate, is a tax determination — not yours.** Work from the rate already applied or the vendor's declared status. If a payment has no deduction and no stated reason, flag it as a question rather than concluding either way.

**Deposited in full** — total deducted for the month against the challan total. A shortfall means interest.

**Return filed and matched** — the return should reconcile to the challans, and to what your vendors will see.

### The reconciliation

```
TDS PAYABLE — [month]

Opening balance              ₹  1,84,000
Deducted this month          ₹  3,26,400
Deposited                    ₹ (1,84,000)   prior month
Closing balance              ₹  3,26,400    due next month

BY SECTION
  194C  contractors          ₹  1,42,000
  194J  professional         ₹  1,48,400
  194I  rent                 ₹    36,000

FLAGGED
  · 4 vendor payments totalling ₹2,84,000 with no deduction and no
    exemption noted — confirm whether these should have attracted TDS
  · 1 vendor has no PAN on file — higher rate may apply, needs checking
```

**Missing PAN is worth surfacing every time.** The consequence is a materially higher deduction rate, and it's a master-data fix that keeps getting deferred.

---

## Common causes of difference

**Timing.** You book TDS on invoice; the deductor deposits on payment. Across a quarter end this always creates a gap. Track it as timing, not as a mismatch.

**Rounding.** Small differences per transaction, accumulating.

**Section applied differently.** You booked under one section, they deducted under another. The amount may still match.

**Partial payment.** They deducted on what they paid, you booked on what you invoiced.

**Grossing.** Deduction computed on a different base — with or without GST. This is a treatment question; report the difference, don't resolve it.

---

## Practical notes

**Reconcile quarterly, minimum.** 26AS updates as deductors file, so a monthly reconciliation catches too little to be worth the effort.

**Pull 26AS and AIS both.** AIS carries transactions 26AS doesn't, and the difference is sometimes the explanation.

**Keep a chase log.** Who was chased, when, response. Deductors who need three reminders every quarter are a pattern worth escalating commercially, not just administratively.

**Don't net receivable against payable.** They're different heads with different treatment. Presenting a net figure hides both problems.

**Rates and sections change.** Thresholds and rates are revised regularly. Never hardcode them — work from what's in the books and flag anything that looks inconsistent for the CA to check.
