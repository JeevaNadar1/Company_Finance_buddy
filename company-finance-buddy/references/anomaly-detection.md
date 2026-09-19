# Anomaly Detection

Where this genuinely beats manual review. A person scanning 5,000 ledger lines misses what a pattern check doesn't.

**Flag, don't fix.** Every anomaly here has an innocent explanation and a serious one. Surfacing it is the contribution; deciding which it is, is not.

---

## Duplicate payments

The one that recovers actual cash.

**Check:** same vendor, same amount, within 30 days. Then loosen — same amount and same date, any vendor. Then same invoice number across different vendor records.

**Innocent:** genuine recurring payment, instalments, a legitimate second invoice for the same amount.
**Serious:** paid twice. Recoverable if caught early, awkward after a year.

```
DUPLICATE CANDIDATES
  Sharma & Co   ₹1,45,000   12 Aug (PMT-4402) · 19 Aug (PMT-4451)
                Same amount, 7 days apart, no invoice ref on either
```

---

## Vendor name variants

Quiet, cumulative, and it corrupts every vendor-level analysis you run.

**Check:** fuzzy match across the vendor master. Normalise — strip `Pvt`, `Private`, `Ltd`, `Limited`, `&`, `and`, punctuation, case — then compare.

`ABC Pvt Ltd` · `ABC Private Limited` · `A.B.C. Pvt. Ltd.` · `ABC PVT LTD` — one vendor, four ledgers, four sets of ageing, four GST reconciliation failures.

**Match on GSTIN where present.** Same GSTIN under two names is conclusive.

---

## Round numbers

**Check:** entries ending in `000` or `0000`, above a threshold, in accounts where round numbers are unusual.

**Innocent:** a genuinely round contract value, an agreed retainer.
**Serious:** a manual estimate posted as an actual and never trued up. These sit in the books indefinitely.

Rent at ₹1,50,000 is fine. Professional fees at exactly ₹2,00,000 with no invoice reference is worth a look.

---

## Weekend and holiday postings

**Check:** entry date, not posting date, falling on a non-working day.

**Innocent:** batch processing, automated entries, genuine weekend operations.
**Serious:** backdating.

Flag the pattern rather than the instance — one weekend entry is nothing, forty in a month is a system behaviour worth understanding.

---

## Threshold clustering

**Check:** entries falling just below an approval limit. If authorisation is required above ₹50,000, count entries between ₹45,000 and ₹49,999.

**Innocent:** coincidence, at low volumes.
**Serious:** splitting to avoid approval.

The signal is concentration, not any single entry.

---

## Sequence gaps

**Check:** gaps in invoice, receipt, cheque and voucher number sequences.

**Innocent:** cancelled documents, multiple series, manual numbering.
**Serious:** a missing document, or one that was removed.

---

## Period-end concentration

**Check:** proportion of the month's entries posted in the last two days.

**Innocent:** ordinary close activity.
**Serious:** cut-off manipulation — pulling revenue in or pushing cost out.

Compare against prior months. A jump is what matters, not the absolute level.

---

## New vendors

**Check:** vendors appearing for the first time this period.

Not suspicious by itself — but it's a master-data control point, and new vendors are where both errors and fraud concentrate. Worth a list every month.

**Higher-signal version:** new vendor, first transaction above a material threshold, paid within days of creation.

---

## Balances with the wrong sign

**Check:** debit balances in creditors, credit balances in debtors, negative inventory, negative accumulated depreciation.

**Innocent:** advances misposted, genuine overpayments awaiting adjustment.
**Serious:** a misposting that's distorting both sides.

**These almost always indicate a real error.** Higher-yield than most checks on this list.

---

## Reversed and reposted

**Check:** an entry reversed and a similar one posted shortly after.

**Innocent:** correcting a mistake — normal and expected.
**Serious:** a pattern of reversals in the same account, or reversals clustered at period end.

---

## Movement variance

**Check:** each ledger against its trailing three-month average. Flag anything outside a set band.

**The highest-yield check on this list**, because it catches errors that reconcile perfectly. A cost posted to the wrong head still ties — only the movement review shows it.

```
MOVEMENT REVIEW — accounts outside ±30%

Professional fees    ₹4,82,000   vs avg ₹1,20,000   +302%
Travel               ₹  18,000   vs avg ₹  92,000    -80%
Repairs              ₹2,10,000   vs avg ₹  34,000   +517%
```

**Every one needs a sentence of explanation** before the report goes out. "Professional fees up because of the statutory audit fee" closes it. No explanation means it's unexplained, and unexplained is where errors live.

---

## Dormant accounts reactivated

**Check:** ledgers with no movement for six months that transacted this period.

Innocent more often than not. Cheap to check, occasionally revealing.

---

## Benford's law

**Check:** distribution of leading digits across a large transaction set. Naturally-occurring financial data skews heavily toward 1 as a leading digit; fabricated numbers usually don't.

**Only meaningful above a few thousand transactions**, and only ever a prompt to look closer. **Never a conclusion.** Plenty of legitimate datasets fail it — anything with pricing floors, contract minimums, or a narrow value band.

Include it if the volume supports it. Present it as a curiosity, not a finding.

---

## Reporting anomalies

**Group by type. Sort by value within each. State the innocent explanation alongside the serious one.**

```
ANOMALY REVIEW — August

DUPLICATE CANDIDATES (2) — ₹1,72,000
  Sharma & Co  ₹1,45,000  12 & 19 Aug, no invoice ref
  Krishna Tr.  ₹  27,000  03 & 04 Aug, same amount

MOVEMENT OUTSIDE ±30% (3)
  Professional fees  +302%  — audit fee?
  Repairs            +517%  — unexplained
  Travel              -80%  — unexplained

WRONG-SIGN BALANCES (4) — ₹3,84,000
  Debit balances in creditors, 4 vendors — advances?

NEW VENDORS (7)
  1 paid within 3 days of creation: Vertex Supply, ₹2,40,000
```

**Don't editorialise.** "Repairs up 517% — unexplained" is a flag. "Repairs up 517% — this looks suspicious" is a conclusion you're not positioned to draw, and it puts the reader on the defensive about something that probably has a boring answer.
