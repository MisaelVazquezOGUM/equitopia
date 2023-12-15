from odoo import api, models, fields
from odoo.exceptions import UserError
import datetime

class Contratos(models.Model):
    _inherit = 'account.analytic.account'

    commission_invoice = fields.Many2one('account.move', string="Commission Invoice")

    def gen_commissions_invoice(self):
        month = datetime.date.today().month
        contracts = self.search([('chech_out','<=',datetime.date.today()), ('commission_invoice','=',False)])
        skip_list = []
        for contract in contracts:
            if contract in skip_list:
                continue
            same_property = [contract]
            skip_list.append(contract)
            commission = contract.property_id.rent_amount * 0.1
            for new_contract in contracts:
                if new_contract.property_id == same_property[0].property_id:
                    same_property.append(new_contract)
                    skip_list.append(new_contract)
                    commission += new_contract.property_id.rent_amount * 0.1
                    
            contract = same_property[0]
            inv_line_dict = {
                'quantity': 1,
                'price_unit': commission or 0.0,
                'account_id': contract.property_id.expense_account_id.id or False,
                'analytic_account_id': contract.id or False,
                'name': 'Comision',
                'is_service': False,
                'maintenance_id': False,
            }
            inv_line_values = {
                'partner_id': contract.property_owner_id.id or False,
                'type': 'in_invoice',
                'invoice_line_ids': [(0, 0, inv_line_dict)],
                'property_id': contract.property_id.id or False,
                'new_tenancy_id': contract.id,
                'gastos_extra': False,
                'is_commission': True,
            }

            new_invoice = self.env['account.move'].create(inv_line_values)
            new_invoice.action_post()
            for contract in same_property:
                contract.commission_invoice = new_invoice.id

class Factura(models.Model):
    _inherit = 'account.move'

    is_commission = fields.Boolean(string="is commission?")

