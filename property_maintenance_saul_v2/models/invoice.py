from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

# For debug use only
from odoo.exceptions import UserError,ValidationError


class AccountMoveModified(models.Model):
    _inherit = 'account.move'

    def action_invoice_register_payment(self):
        res = super(AccountMoveModified, self).action_invoice_register_payment()
        new_context = res['context'].copy()

        payment = self.invoice_line_ids[0]
        payment_type = 'r'
        if payment.is_service:
            payment_type = 's'
        elif not str(payment.maintenance_id) == 'maintenance.request()': 
            payment_type = 'm'
        elif self.gastos_extra:
            payment_type = 'o'
        elif self.is_commission:
            payment_type = 'c'
        
        new_context.update({'default_tipo_de_pago': payment_type})
        res.update({
            'context': new_context,
            })
        return res


class AccountPaymentModified(models.Model):
    _inherit = 'account.payment'

    def post(self):
        res = super(AccountPaymentModified, self).post()
        # raise UserError(str(res))
        return res


class TenancyRentScheduleModified(models.Model):
    _inherit = 'tenancy.rent.schedule'

    is_service = fields.Boolean()
    maintenance_id = fields.Many2one('maintenance.request')

