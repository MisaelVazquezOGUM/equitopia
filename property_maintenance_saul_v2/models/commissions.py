from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime

# For debug use only
from odoo.exceptions import UserError,ValidationError


class AccountComission(models.Model):
    _name = 'account.asset.commission'

    commission_percentage = fields.Float(string="Comisión (porcentaje)")
    commission_value = fields.Float(string="Comisión", readonly=True)
    property_id = fields.Many2one('account.asset.asset')

    @api.onchange('commission_percentage')
    def check_commission(self):
        if self.commission_percentage > 100:
            raise ValidationError('Error en valores de comisión: No puedes elegir un porcentaje mayor al 100%')
        if self.commission_percentage < 0:
            raise ValidationError('Error en valores de comisión: No puedes elegir un porcentaje negativo')


class AccountAssetModified(models.Model):
    _inherit = 'account.asset.asset'
    commission_ids = fields.One2many('account.asset.commission', inverse_name='property_id', string='Commissions')
    commission_percentage = fields.Float(string="Commission (percentage)")
    commission_value = fields.Float(string="Commission")

    def create_tenancy(self):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Crear contrato',
                'res_model': 'account.analytic.account',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('property_management.property_analytic_view_form').id,
                'target': 'current',
                'context': {
                    'default_property_id': self.id,
                    'default_property_owner_id': self.property_owner.id,
                    'default_commission_value': self.commission_value,
                    'default_commission_percentage': self.commission_percentage,
                    }
                }


class AccountAnalyticModified(models.Model):
    _inherit = 'account.analytic.account'

    def _compute_commission(self):
        for rec in self:
            commission = 0
            for entry in rec.rent_schedule_ids:
                if entry.invc_id.invoice_line_ids.name == 'Pago de renta':
                    commission += entry.invc_id.amount_total * rec.commission_percentage * 0.01
            rec.commission_value = commission

    commission_value = fields.Float(string="Commission", compute='_compute_commission')
    commission_percentage = fields.Float(string="Commission (percentage)")

    def open_payment(self):
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('property_management.property_analytic_view_form').id,
                'res_model': 'account.analytic.account',
                'res_id': self.id,
                'target': 'current',
                }

