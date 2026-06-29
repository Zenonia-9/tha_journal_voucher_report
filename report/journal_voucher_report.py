from odoo import _, api, models
from odoo.exceptions import UserError


def _get_journal_voucher_report_values(report_model, docids, data=None):
    data = data or {}
    if not docids and data.get("active_ids"):
        docids = data.get("active_ids")
    elif not docids and data.get("move_id"):
        docids = [data.get("move_id")]

    docs = report_model.env["account.move"].browse(docids).exists()

    # List-view printing sends all selected moves directly to this report.
    if not docs:
        raise UserError(_("Please select at least one journal entry to print."))
    if any(move.move_type != "entry" for move in docs):
        raise UserError(_("Print JV can only be used for journal entries."))
    if any(move.state != "posted" for move in docs):
        raise UserError(_("You can only print posted journal entries."))

    company_currency = docs[:1].company_currency_id or report_model.env.company.currency_id
    return {
        "doc_ids": docs.ids,
        "doc_model": "account.move",
        "docs": docs,
        "data": data,
        "company_currency": company_currency,
    }


class JournalVoucherReport(models.AbstractModel):
    _name = "report.tha_journal_voucher_report.journal_voucher"
    _description = "Journal Voucher"
    _table = "tjvr_report_jv"
    _auto = False

    @api.model
    def _get_report_values(self, docids, data=None):
        return _get_journal_voucher_report_values(self, docids, data=data)


class JournalVoucherA5Report(models.AbstractModel):
    _name = "report.tha_journal_voucher_report.journal_voucher_a5"
    _description = "Journal Voucher A5"
    _table = "tjvr_report_jv_a5"
    _auto = False

    @api.model
    def _get_report_values(self, docids, data=None):
        return _get_journal_voucher_report_values(self, docids, data=data)
