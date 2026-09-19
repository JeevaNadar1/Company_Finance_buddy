# Zoho Books

Using the connector, where it's available.

---

## Read first, always

**Pull and reconcile before writing anything back.**

Every write is an entry in someone's books. It carries an audit trail, it may be reported, and undoing it means a reversal that also shows.

```
1. PULL      ledgers, trial balance, bills, invoices, bank feeds
2. ANALYSE   reconcile and detect offline
3. REPORT    findings and proposed entries
4. CONFIRM   explicit approval, per action
5. WRITE     only what was approved
```

---

## Never write without explicit confirmation

Not general permission. **Confirmation on the specific action.**

| Never without confirmation | Because |
|---|---|
| Post a journal entry | It's a book entry with an audit trail |
| Mark a transaction reconciled | Asserts a conclusion you may not be entitled to |
| Modify or delete a record | Alters history |
| Change a categorisation | Changes the P&L |
| Approve or issue anything | Not yours to do |
| Mark an invoice paid | Financial assertion |
| Merge vendor records | Destructive, and hard to unwind |

**"Go ahead and fix the reconciliation" is not authorisation to post twelve journal entries.** Show what you'd post, itemised, and get a yes on the list.

```
PROPOSED ENTRIES — 3, totalling ₹47,200
  1. Dr Bank charges ₹1,240 / Cr Bank — Aug charges not booked
  2. Dr Bank ₹4,960 / Cr Interest income — interest credited 31 Aug
  3. Dr Freight ₹41,000 / Cr Accrued expenses — GRN received, no invoice

Confirm each, or say "post all three".
```

---

## What to pull

| Need | Pull |
|---|---|
| Reconciliation base | Trial balance, opening and closing |
| Ledger detail | Account transactions for the period |
| Purchase register | Bills with vendor GSTIN, date, taxable value, tax |
| Sales register | Invoices, same fields |
| Bank | Bank transactions and feed status |
| Ageing | Receivables and payables ageing |
| Fixed assets | Where maintained in Zoho |
| Vendor master | For duplicate and variant detection |

**Pull everything before starting.** Discovering a missing source mid-reconciliation means redoing it.

---

## Batch, don't loop

One call returning a period's transactions beats one call per transaction. Sequential per-record calls are slow, hit rate limits, and provide nothing extra.

---

## Reconcile offline

**Pull the data, reconcile in your own working, report the result.**

Don't use the connector's own matching as the reconciliation. You need to control the matching tiers, the normalisation, and the confidence bands — which is the whole method in `gst-reconciliation.md`.

---

## What Zoho won't have

Plan to source these separately:

- **GSTR-2B** — from the GST portal
- **26AS / AIS** — from the Income Tax portal
- **Bank statements** — the feed may lag or miss items; reconcile against the actual statement
- **Physical inventory counts**
- **Contracts and engagement letters** — for accrual basis

**The reconciliation is only as good as the external source.** Reconciling Zoho against Zoho proves nothing.

---

## Errors

**Read the error, fix, retry in the same turn.** Don't report a failure and stop.

| Error | Response |
|---|---|
| Auth expired | Say so; the user reconnects |
| Rate limited | Back off, batch harder |
| Record not found | Verify the ID; don't create |
| Validation failed | Report what was rejected and why — never retry with modified data unasked |

**Never work around a validation failure by changing the data.** The validation exists for a reason, and altering the entry to get it accepted is how bad data enters clean.

---

## Audit trail

**Every write should be traceable to an instruction.**

Log: what was posted, when, on whose confirmation, and why. When someone asks in six months why there's a ₹41,000 freight accrual in August, the answer needs to exist.

**Narrations should be self-explanatory.** "Adj" is useless. "Freight accrual — GRN 4471, invoice pending" is a complete answer to a future question.
