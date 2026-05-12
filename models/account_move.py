from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _validate_journal_voucher_moves(self):
        if not self:
            raise UserError(_("No journal entries selected."))
        if any(move.move_type != "entry" for move in self):
            raise UserError(_("Journal vouchers can only be printed for journal entries."))
        if any(move.state != "posted" for move in self):
            raise UserError(_("You can only print journal vouchers for posted entries."))
        if len(self.company_id) > 1:
            raise UserError(_("Selected journal entries must belong to the same company."))
        return self

    def action_open_journal_voucher_print_wizard(self):
        moves = self._validate_journal_voucher_moves()
        return {
            "type": "ir.actions.act_window",
            "name": _("Print"),
            "res_model": "journal.voucher.print.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_move_id": moves[:1].id,
                "default_move_ids": [(6, 0, moves.ids)],
                "active_ids": moves.ids,
                "active_model": "account.move",
            },
        }

    def _get_journal_voucher_report_ref(self, paper_format):
        self.ensure_one()
        if paper_format not in ("a4", "a5"):
            raise UserError(_("Please select a valid paper format."))

        report_by_format = {
            "a4": "tha_jounal_voucher_report.action_report_jv",
            "a5": "tha_jounal_voucher_report.action_report_jv_a5",
        }
        return report_by_format[paper_format]
