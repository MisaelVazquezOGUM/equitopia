# See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _
import time
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import ValidationError


class CommissionInvoiceLine(models.Model):
    _name = "commission.invoice.line"
    _description = "Commission Invoice Line"
    _order = 'date desc, id desc'

    date = fields.Date(
        string='Start Date',
        readonly=True)
    end_date = fields.Date(
        string='End Date',
        readonly=True)
    name = fields.Char(
        string="Description")
    commission_type = fields.Selection(
        selection=[('fixed', 'Fixed percentage'),
                   ('fixedcost', 'By Fixed Cost')],
        string='Type', readonly=True)
    currency_id = fields.Many2one(
        'res.currency',
        store=True,
        default=lambda self: self.env.company.currency_id,
        readonly=True)
    rent_amt = fields.Monetary(
        string='Rent Amount',
        currency_field='currency_id',
        default=0.0, readonly=True)
    amount = fields.Monetary(
        default=0.0,
        currency_field='currency_id',
        string='Commission Amount', readonly=True)
    commission_id = fields.Many2one(
        comodel_name='commission.invoice',
        string='Commission')
    invc_id = fields.Many2one(
        comodel_name='account.move',
        string='Invoice')
    inv = fields.Boolean(
        string='INV')
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company,
        string="Owner Company")
    invoiced = fields.Boolean(
        string='Invoiced')

    @api.constrains('date', 'end_date')
    def check_date_overlap(self):
        for line in self:
            if line.date and line.end_date and line.end_date < line.date:
                raise ValidationError(
                    _('End date should be grater then Start Date!'))
        return True


class CommissionInvoice(models.Model):
    _name = "commission.invoice"
    _rec_name = 'number'
    _description = "Commission Invoice"

    @api.depends('commission_line.amount')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        if self.amount_total == 0.0:
            for data in self.commission_line:
                self.amount_total += data.amount

    number = fields.Char(
        string='Commission ID',
        default='/')
    patner_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Partner',
        help='Name of tenant where from commission is taken')
    date = fields.Date(
        String='Commission Date',
        default=lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT))
    tenancy = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy')
    description = fields.Text(
        string='Description')
    property_tenancy_id = fields.Many2one(
        comodel_name='account.asset.asset',
        related='tenancy.property_id',
        string='Property Tenancy')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    state = fields.Selection(
        [('draft', 'Open'),
         ('cancel', 'Cancel'),
         ('invoice', 'Invoiced')
         ], 'State', readonly=True,
        default='draft')
    commission_type = fields.Selection(
        selection=[('fixed', 'Fixed percentage'),
                   ('fixedcost', 'By Fixed Cost')],
        string='Type',
        default='fixed')
    commission_line = fields.One2many(
        comodel_name='commission.invoice.line',
        inverse_name='commission_id',
        string='Commission')
    amount_total = fields.Float(
        string='Total',
        store=True,
        readonly=True,
        compute='_amount_all',
        track_visibility='always')
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id, readonly=True)
    agent = fields.Many2one(
        comodel_name='res.partner',
        domain=[('agent', '=', True)])
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company', readonly=True,
        default=lambda self: self.env.company)
    invc_id = fields.Many2one(
        comodel_name='account.move',
        string='Invoice')
    inv = fields.Boolean(
        string='INV')
    color = fields.Integer('Color Index')

    @api.onchange('patner_id')
    def onchange_patner_id(self):
        self.tenancy = self.env['account.analytic.account'].search(
                [('tenant_id', '=', self.patner_id.id),
                 ('is_property', '=', True),
                 ('state', '!=', 'close'),
                 ('state', '!=', 'cancelled')], limit=1).id or False

    def create_invoice(self):
        """
        This method is used to create supplier invoice.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        account_jrnl_obj = self.env['account.journal'].search(
            [('type', '=', 'purchase')], limit=1)
        for data in self:
            inv_line_values = {
                'name': 'Commission For ' + data.number or "",
                'analytic_account_id': data.tenancy.id or False,
                # 'origin': 'Commission',
                'quantity': 1,
                'account_id': data.property_id.expense_account_id.id or False,
                'price_unit': data.amount_total or 0.00,
            }
            inv_values = {
                'invoice_origin': 'Commission For ' + data.number or "",
                'type': 'in_invoice',
                'property_id': data.property_id.id,
                'partner_id': data.agent.id or False,
                'invoice_line_ids': [(0, 0, inv_line_values)],
                'invoice_date': datetime.now().strftime(
                    DEFAULT_SERVER_DATE_FORMAT) or False,
                # 'account_id': data.agent.property_account_payable_id.id or False,
                'journal_id': account_jrnl_obj and account_jrnl_obj.id or False,
                'company_id': data.company_id.id or False,
                'currency_id': data.currency_id.id or False
            }
            acc_id = self.env['account.move'].with_context({'default_type': 'in_invoice'}).create(inv_values)
            data.write({'inv': True, 'invc_id': acc_id.id, 'state': 'invoice'})
        return {
            'view_type': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invc_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': self._context,
        }
    
    def create_commission_invoice(self):
        """
        This method is used to create supplier invoice.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        account_jrnl_obj = self.env['account.journal'].search(
            [('type', '=', 'purchase')], limit=1)
        for data in self:
            inv_line_values = {
                'name': 'Commission For ' + data.number or "",
                #'analytic_account_id': data.tenancy.id or False,
                # 'origin': 'Commission',
                'quantity': 1,
                'account_id': data.property_id.expense_account_id.id or False,
                'price_unit': data.amount_total or 0.00,
            }
            inv_values = {
                'invoice_origin': 'Commission For ' + data.number or "",
                'type': 'in_invoice',
                'property_id': data.property_id.id,
                'partner_id': data.agent.id or False,
                'invoice_line_ids': [(0, 0, inv_line_values)],
                'invoice_date': datetime.now().strftime(
                    DEFAULT_SERVER_DATE_FORMAT) or False,
                # 'account_id': data.agent.property_account_payable_id.id or False,
                'journal_id': account_jrnl_obj and account_jrnl_obj.id or False,
                'company_id': data.company_id.id or False,
                'currency_id': data.currency_id.id or False
            }
            acc_id = self.env['account.move'].with_context({'default_type': 'in_invoice'}).create(inv_values)
            data.write({'inv': True, 'invc_id': acc_id.id, 'state': 'invoice'})
            acc_id.action_post()

    def open_invoice(self):
        """
        This Method is used to Open invoice .
        ------------------------------------
        @param self: The object pointer
        """
        return {
            'view_type': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invc_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': self._context or {},
        }

    @api.model
    def create(self, vals):
        """
        This Method is used to create sequence for commission.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        res = super(CommissionInvoice, self).create(vals)
        if res:
            res.number = self.env['ir.sequence'].get('commission.invoice')
        return res

    def button_close(self):
        """
        This button method is used to Change commission state to cancel.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        if not self.tenancy.state == 'close' or \
                self.tenancy.state == 'cancelled':
            raise ValidationError(_("Please First close " + str(
                self.tenancy.name) + " Tenancy!"))
        return self.write({'state': 'close'})


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.depends('commission_type', 'fix_qty', 'fix_cost', 'total_rent')
    def calculate_commission(self):
        """
        This method is used to calculate commistion as per commition type
        -----------------------------------------------------------------
        @param self: The object pointer
        """
        self.total_commission = 0.0
        for data in self:
            if data.commission == True:
                if data.commission_type == 'fixed':
                    data.total_commission = data.total_rent * (
                        data.fix_qty / 100.0)
                if data.commission_type == 'fixedcost':
                    data.total_commission = data.fix_cost

    commission_type = fields.Selection(
        selection=[('fixed', 'Fixed percentage'),
                   ('fixedcost', 'By Fixed Cost')],
        string='Type')
    fix_qty = fields.Float(
        string='Fixed Percentage(%)')
    fix_cost = fields.Float(
        string='Fixed Cost')
    agent = fields.Many2one(
        comodel_name='res.partner',
        domain=[('agent', '=', True)])
    commission = fields.Boolean(
        'Commission')
    commission_create = fields.Boolean(
        'Create')
    total_commission = fields.Float(string="Total Commission")

    def create_commission(self):
        """
        This button method is used to Change Tenancy state to Open.
        -----------------------------------------------------------
        @param self: The object pointer
        """
        for data in self:
            if not data.rent_entry_chck:
                raise ValidationError("First you have to schedule rent after you can create commission.")
            if data.total_commission == 0.00:
                raise ValidationError(
                    _('Total Commission must be grater than zero.'))
            line_vlas = {
                'name': 'Commission',
                'commission_type': data.commission_type,
                'rent_amt': data.total_rent,
                'date': data.date_start,
                'end_date': data.date,
                'amount': data.total_commission,
            }
            vals = {
                'patner_id': data.tenant_id.id,
                'tenancy': data.id,
                'property_id': data.property_id.id,
                'agent': data.agent.id,
                'commission_line': [(0, 0, line_vlas)],
            }
            self.env['commission.invoice'].create(vals)
            data.write({'commission_create': True})

    @api.onchange('commission')
    def onchange_property_id(self):
        """
        This method is used to check if the commistion field False than
        othe field value will be null or zero or false.
        ---------------------------------------------------------------
        @param self: The object pointer
        """
        if self.commission is False:
            self.agent = 0
            self.commission_type = ''
            self.fix_qty = 0.00
            self.fix_cost = 0.00
