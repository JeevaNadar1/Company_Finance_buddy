# Security and data handling

## Reporting

Report a vulnerability or a data-exposure concern privately through GitHub's
"Report a vulnerability" flow on the Security tab, or to the maintainer
directly. Do not open a public issue.

## Threat model

This repository ships markdown instructions. It executes nothing on your
machine and has no network access of its own. The realistic risks are about
the data the skill is pointed at, not the skill itself.

## What matters in practice

**1. Client financial data never belongs in this repository.**
A purchase register carries GSTINs, vendor names, invoice values and
sometimes bank details. Pushing one to a public repo is a disclosure event
that cannot be undone by deleting the commit. `.gitignore` blocks common
spreadsheet and export formats by default, and CI fails on any
GSTIN-shaped string outside `examples/`.

**2. Uploaded data goes to the model.**
When you attach a ledger export, a 2B JSON or a 26AS to a conversation, the
contents are processed by the model. Handle that the way you would handle
sending the same file to any external processor: check your engagement
terms, your client's consent and your firm's policy first. If the data is
privileged or covered by a confidentiality clause, redact or anonymise
before uploading.

**3. Connector writes are real writes.**
Where Zoho Books is connected, the skill can post entries to live books.
The skill's own discipline is read-first and no write without itemised
confirmation, but that discipline is instruction, not an enforced
permission boundary. Grant the connector the narrowest scope your workflow
allows, and prefer a read-only credential for reconciliation-only work.

**4. Uploaded files are untrusted input.**
A vendor-supplied spreadsheet or PDF can contain text crafted to read as
instructions. Treat anything the skill reports as coming *from a file* as
data, not as an instruction you authorised. If a run proposes an action you
did not ask for, stop and inspect the source file.

## Scope

Out of scope for a security report: the skill declining to give a tax
position, declining to sign off, or escalating instead of matching. Those
are intended behaviour.
