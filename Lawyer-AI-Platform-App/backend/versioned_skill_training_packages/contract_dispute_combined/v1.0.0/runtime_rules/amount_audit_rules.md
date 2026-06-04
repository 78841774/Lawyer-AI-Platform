# case-fact-extractor-v3 Amount Audit Rules

Source basis: `case-fact-extractor-v3/SKILL.md` and `references/scoring.md`.

Status: readonly legacy asset prepared for versioned training packages.

## Three-Round Verification

Core amounts must complete three-round verification before a case can enter the full A-series analysis chain.

Required checks:

* Extract every principal, contract price, penalty, attorney fee, preservation fee, loss, paid amount, refund, offset, and settlement amount.
* Preserve formula, source evidence, original excerpt, and calculation basis.
* Compare totals across contracts, invoices, receipts, bank flows, platform backend exports, statements, pleadings, and evidence lists.
* Mark differences and return to original vouchers when totals conflict.

## OCR and Screenshot Gate

Amounts from OCR, high-DPI images, screenshots, or scanned tables cannot alone release the amount gate.

If OCR quality is C or D, amounts must stay in audit mode and cannot support final A6, A7, or A12 outputs.

## Output Requirement

The fact report must include an amount audit table and explain whether the case can enter full legal analysis.
