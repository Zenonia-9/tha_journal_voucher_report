from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_open_journal_voucher_print_wizard(self):
        self.ensure_one()
        if self.move_type != "entry":
            raise UserError(_("Journal vouchers can only be printed for journal entries."))
        if self.state != "posted":
            raise UserError(_("You can only print journal vouchers for posted entries."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Print"),
            "res_model": "journal.voucher.print.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_move_id": self.id,
                "active_ids": self.ids,
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

