# CA35P — Synthetic sales data analysis practice (original)

**Status:** Original educational exercise; **not** an official KASNEB exam, paper or model answer. No independent subject-expert review has been completed. The dataset is wholly fictional and does not contain personal data or third-party questions, photographs or solutions.

**Suggested skills:** CSV import, calculated columns, data validation, conditional sums, branch summaries, business interpretation. Use Excel, LibreOffice or a data-analysis tool. Current KASNEB exam-software and outcome alignment remain unverified.

## Dataset

Use `CA35P_synthetic_sales.csv` (12 transactions, 1–6 October 2026). Fields: transaction ID, date, branch, units, unit price in KES and status (`Paid` or `Refunded`). Each transaction is unique. Define `amount = units × unit_price_kes`. **Gross billed** includes both statuses; **refunded value** is the sum of `Refunded` transactions; **net retained sales** equals gross minus refunded value. This is a simplified exercise, not formal financial-statement revenue recognition.

## Questions

1. Validate that transaction IDs are unique, units/prices are positive and status values belong to the stated two categories.
2. Calculate amount for each transaction and total gross billed value.
3. Calculate refunded value and refund-value percentage of gross billed value.
4. Calculate net retained sales and branch-level net retained sales, excluding refunded transactions.
5. Identify the branch with the largest net retained sales. Explain one limitation of using this six-day fictional sample for management decisions.

## Independently recalculated answer key (arithmetic only)

- Unique IDs: 12; invalid status/negative-or-zero unit and price values: 0.
- Gross billed: **KES 34,000**.
- Refunded: **KES 9,000** (TX004 KES 5,000 + TX009 KES 4,000).
- Refund value as a percentage of gross billed: **26.47%** (9,000 / 34,000 × 100).
- Net retained sales: **KES 25,000**.
- Branch net retained sales: **Nairobi KES 13,900; Mombasa KES 5,800; Kisumu KES 5,300**.
- Highest branch: **Nairobi**. Limitations include tiny, deliberately fabricated sample, no operating costs, no seasonal representativeness, and simplistic treatment of refunds.

### Suggested spreadsheet formulas

Assume the CSV headers are in row 1, data in rows 2–13 and an `amount` column is G. In G2 use `=D2*E2` and fill down. Gross: `=SUM(G2:G13)`; refunds: `=SUMIF(F2:F13,"Refunded",G2:G13)`; net: `=SUMIF(F2:F13,"Paid",G2:G13)`; Nairobi net: `=SUMIFS(G2:G13,C2:C13,"Nairobi",F2:F13,"Paid")`. Check that net equals gross less refunds.

## Rights and review

The exercise and its dataset were authored for this library and may be used and adapted by the project owner. No KASNEB endorsement is implied. Source external references are **not** embedded. Arithmetic was checked by a separate script; curriculum mapping and pedagogical quality await independent review. No AI-training rights are granted or inferred for unrelated third-party materials.
