# Journal Voucher Report

![Odoo 19](https://img.shields.io/badge/Odoo-19.0-875A7B?style=flat-square)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=flat-square)
![Category](https://img.shields.io/badge/Category-Accounting-4ECDC4?style=flat-square)

Print journal vouchers from posted journal entries in Odoo 19.

This module adds a focused journal voucher printing flow for accounting teams that work with general journal entries. It supports printing from both form and list contexts, validates accounting safety rules, and provides dedicated A4 and A5 voucher outputs.

## Highlights

- Adds a **Print JV** flow for journal entries.
- Supports **single-entry** and **batch** printing.
- Allows printing from **form view** and **list selection**.
- Restricts usage to **posted entries** only.
- Rejects non-`entry` moves and mixed-company selections.
- Includes a print wizard with **paper format** selection.
- Ships with dedicated **A4** and **A5** voucher reports and paper formats.

## Workflow

1. Open one or more posted journal entries.
2. Launch the journal voucher print wizard.
3. Choose the paper format.
4. Print the resulting journal voucher PDF.

## Technical Notes

- `models/account_move.py`
  Adds the journal voucher action and validates the selected moves.
- `wizard/journal_voucher_print_wizard.py`
  Reuses one wizard for both single-record and multi-record printing.
- `report/journal_voucher_report.py`
  Supplies the report values for both A4 and A5 report models.
- `report/journal_voucher_layout.xml`
  Keeps the voucher layout isolated inside this addon.

## Module Layout

```text
tha_journal_voucher_report/
|-- models/
|-- wizard/
|-- report/
|-- security/
|-- views/
`-- __manifest__.py
```

## Dependencies

- `account`
- `web`

## Installation

1. Place the module in your custom addons path.
2. Update the Apps list in Odoo.
3. Install **Journal Voucher Report**.

## License

This module is licensed under `LGPL-3`.
