from odoo import _, api, fields, models
from odoo.exceptions import UserError


class JournalVoucherPrintWizard(models.TransientModel):
    _name = "journal.voucher.print.wizard"
    _description = "Journal Voucher Print Wizard"

    move_id = fields.Many2one(
        "account.move",
        string="Journal Entry",
        required=True,
        readonly=True,
    )
    paper_format = fields.Selection(
        selection=[
            ("a4", "A4"),
            ("a5", "A5"),
        ],
        string="Paper Format",
        required=True,
        default="a4",
    )
    company_id = fields.Many2one(
        related="move_id.company_id",
        string="Company",
        readonly=True,
    )
    journal_id = fields.Many2one(
        related="move_id.journal_id",
        string="Journal",
        readonly=True,
    )
    date = fields.Date(
        related="move_id.date",
        string="Date",
        readonly=True,
    )
    currency_id = fields.Many2one(
        related="move_id.company_currency_id",
        readonly=True,
    )
    total_debit = fields.Monetary(
        string="Total Debit",
        compute="_compute_total_debit",
        readonly=True,
        currency_field="currency_id",
    )

    @api.depends("move_id.line_ids.debit")
    def _compute_total_debit(self):
        for wizard in self:
            wizard.total_debit = sum(wizard.move_id.line_ids.mapped("debit"))

    def action_print(self):
        self.ensure_one()
        move = self.move_id.exists()
        if not move:
            raise UserError(_("Please select a journal entry to print."))
        if move.move_type != "entry":
            raise UserError(_("Journal vouchers can only be printed for journal entries."))
        if move.state != "posted":
            raise UserError(_("You can only print journal vouchers for posted entries."))

        return self.env.ref(
            move._get_journal_voucher_report_ref(self.paper_format)
        ).report_action(
            move,
            data={
                "paper_format": self.paper_format,
                "move_id": move.id,
                "active_ids": move.ids,
            },
        )

