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
    move_ids = fields.Many2many(
        "account.move",
        string="Journal Entries",
        readonly=True,
    )
    move_count = fields.Integer(
        compute="_compute_move_count",
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

    @api.depends("move_ids")
    def _compute_move_count(self):
        for wizard in self:
            wizard.move_count = len(wizard.move_ids)

    @api.depends("move_id.line_ids.debit", "move_ids.line_ids.debit")
    def _compute_total_debit(self):
        for wizard in self:
            moves = wizard.move_ids or wizard.move_id
            wizard.total_debit = sum(moves.mapped("line_ids.debit"))

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get("active_ids") or []
        move_id = res.get("move_id") or self.env.context.get("default_move_id")
        if not active_ids and move_id:
            active_ids = [move_id]

        # The same wizard is opened from both form and list views.
        moves = self.env["account.move"].browse(active_ids).exists()
        if moves:
            moves = moves._validate_journal_voucher_moves()
            res.update(
                {
                    "move_id": moves[:1].id,
                    "move_ids": [(6, 0, moves.ids)],
                }
            )
        return res

    def action_print(self):
        self.ensure_one()
        moves = (self.move_ids or self.move_id).exists()
        if not moves:
            raise UserError(_("Please select a journal entry to print."))
        moves = moves._validate_journal_voucher_moves()

        return self.env.ref(
            moves[:1]._get_journal_voucher_report_ref(self.paper_format)
        ).report_action(
            moves,
            data={
                "paper_format": self.paper_format,
                "move_id": moves[:1].id,
                "active_ids": moves.ids,
            },
        )
