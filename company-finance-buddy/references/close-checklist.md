# The Close, In Sequence

Order matters. Each step depends on the one before, and running them out of order buries discrepancies instead of finding them.

---

## The dependency chain

```
CUT-OFF
   ↓
INGEST          ledgers · bank · purchase register · sales register · 2B · 26AS
   ↓
RECONCILE       bank → GST → TDS → control accounts
   ↓
ADJUST          accruals · prepaids · depreciation · forex · provisions
   ↓
REVIEW          trial balance · anomalies · variances
   ↓
REPORT          MIS · schedules · open items
```

**Never adjust before reconciling.** An accrual posted on top of an unreconciled ledger makes the discrepancy permanent — it's now buried under an entry that looks deliberate.

---

## 1. Cut-off

Fix the boundary before anything else.

- [ ] Period locked in the system, or a clear cut-off communicated
- [ ] Goods received not invoiced identified
- [ ] Invoices received after cut-off, dated within the period, listed
- [ ] Sales dispatched not invoiced identified
- [ ] Bank statement pulled to the exact period end

**Cut-off errors are the most common source of a close that has to be redone.** An invoice booked in the wrong period moves revenue or cost between months, and finding it later means reopening both.

---

## 2. Ingest

Pull everything before starting. Reconciling with a missing source means doing it twice.

| Source | Format |
|---|---|
| General ledger | Export or Zoho pull |
| Trial balance | Opening and closing |
| Bank statements | All accounts, full period |
| Purchase register | With GSTIN, invoice no., date, taxable value, tax |
| Sales register | Same |
| **GSTR-2B** | **JSON preferred** — Excel mangles long invoice numbers |
| GSTR-1 filed | To reconcile against books |
| 26AS / AIS | Quarterly |
| Fixed asset register | For depreciation |
| Payroll summary | |
| Forex rates | Period-end, from a stated source |

**Note what's missing before you start**, rather than discovering it mid-reconciliation.

---

## 3. Reconcile

In this order. Each one narrows what the next has to explain.

### Bank
- [ ] Every account, opening to closing
- [ ] Unpresented cheques listed and aged
- [ ] Deposits in transit listed
- [ ] Bank charges, interest, direct debits booked
- [ ] Unexplained items escalated with narration and amount

### GST
- [ ] Purchase register vs GSTR-2B → `references/gst-reconciliation.md`
- [ ] Sales register vs GSTR-1 vs books
- [ ] RCM items identified and excluded from 2B matching
- [ ] ITC at risk quantified in rupees
- [ ] Vendor chase list produced, sorted by value

### TDS
- [ ] Receivable vs 26AS → `references/tds-reconciliation.md`
- [ ] Payable: deducted, deposited, filed
- [ ] Payments with no deduction and no stated reason flagged
- [ ] Missing vendor PANs flagged

### Control accounts
- [ ] Debtors ledger to control account
- [ ] Creditors ledger to control account
- [ ] Inventory to physical or perpetual records
- [ ] Fixed assets to the register
- [ ] Intercompany balances agreed both sides
- [ ] Suspense account **cleared to zero**

**A suspense balance carried into reporting is an unresolved error with a label on it.** Clear it or escalate it — never report over it.

---

## 4. Adjust

Only after reconciliation is clean.

- [ ] Accruals for known unbilled costs
- [ ] Prepaid amortisation
- [ ] Depreciation, per the stated method and rate
- [ ] Forex revaluation on monetary balances, at a stated rate
- [ ] Provisions per existing policy
- [ ] Reversals of prior-period accruals now actualised

**Depreciation method, useful life and provisioning adequacy are policy decisions.** Apply the policy that exists. If none exists, escalate — don't pick one.

**Mark every estimate as an estimate**, in the ledger narration and in the report.

---

## 5. Review

- [ ] Trial balance ties
- [ ] Month-on-month movement reviewed on every material line
- [ ] Anything above a set variance threshold explained
- [ ] Anomaly checks run → `references/anomaly-detection.md`
- [ ] Negative balances where none should exist
- [ ] Debit balances in creditors, credit balances in debtors
- [ ] Round-number entries reviewed
- [ ] New ledger accounts opened this period reviewed

**Variance review is where errors surface that reconciliation missed.** A ledger can reconcile perfectly and still be wrong if the entries went to the wrong head — only the movement review catches that.

---

## 6. Report

- [ ] P&L with prior-period and budget comparatives
- [ ] Balance sheet
- [ ] Cash flow
- [ ] Supporting schedules for every material line
- [ ] Debtor and creditor ageing
- [ ] Open items log with owners
- [ ] **Every estimate marked as an estimate**

→ `references/reporting.md`

---

## Statutory sequence

**Deadlines change. The sequence doesn't.**

```
Outward supplies reported  →  2B available  →  ITC reconciled  →  summary return + payment

TDS deducted  →  deposited  →  return filed  →  appears in payee's 26AS
```

**Verify every current due date** against the GST and Income Tax portals, or with your CA, each period. Frequencies differ by turnover and filing scheme, and they have been revised.

**What the sequence tells you regardless of dates:** ITC reconciliation must happen *after* 2B is available and *before* the summary return is filed. That window is the pressure point in every Indian close, and it's short.

---

## Open items

Nothing closes with zero open items. What matters is that they're visible.

```
OPEN ITEMS — [period]

# | Item                                    | Owner  | Value      | Since
1 | Anant Ent. invoice not in 2B            | Purch. | ₹37,800    | Aug
2 | Meridian TDS not in 26AS                | AR     | ₹28,400    | Jul
3 | Inventory count variance, Warehouse 2   | Ops    | ₹1,12,000  | Aug
4 | 4 payments, no TDS deducted — confirm   | CA     | ₹2,84,000  | Aug
```

**Age them.** An item open three months is a different problem from one open three days, and only the ageing makes that visible.
