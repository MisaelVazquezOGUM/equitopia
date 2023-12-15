# See LICENSE file for full copyright and licensing details
from odoo import models, api, fields


class PaymentParser(models.AbstractModel):
    _name = 'report.property_rent_report.report_rent_voucher_details'
    _description = 'Property Rent Report'

    def get_amount(self, data):
        """
        This method is used to get total amount
        -----------------------------------
        @param self: The object pointer
        """
        tot_amount = 0.0
        for line in data.rent_schedule_ids:
            if line.paid is True:
                tot_amount = tot_amount + line.amount
        return tot_amount

    def get_amount_due(self, data):
        """
        This method is used to get total amount due
        -------------------------------------------
        @param self: The object pointer
        """
        tot_paid_amount = 0.0
        due_amt = 0.0
        total_rent = data.total_rent
        for line in data.rent_schedule_ids:
            if line.paid is True:
                tot_paid_amount += line.amount
        due_amt = total_rent - tot_paid_amount
        return due_amt

    def get_date(self, data):
        """
        This method is used to set Date
        -------------------------------------------
        @param self: The object pointer
        """
        line_date = []
        date = fields.datetime.now()
        for line in data.rent_schedule_ids:
            if line.paid:
                line_date.append(line.start_date)
        if line_date:
            date = line_date[-1]
        return date

    @api.model
    def _get_report_values(self, docids, data=None):
        payslips = self.env['account.analytic.account'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.analytic.account',
            'docs': payslips,
            'data': data,
            'get_amount': self.get_amount,
            'get_amount_due': self.get_amount_due,
            'get_date': self.get_date,
        }
        return docargs
