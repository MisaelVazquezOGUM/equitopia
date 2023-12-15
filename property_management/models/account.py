# See LICENSE file for full copyright and licensing details

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Account Entry"

    asset_id = fields.Many2one(
        comodel_name='account.asset.asset',
        help='Asset')
    schedule_date = fields.Date(
        string='Schedule Date',
        help='Rent Schedule Date.')
    source = fields.Char(
        string='Account Source',
        help='Source from where account move created.')

    def _check_balanced(self):
        moves = self.filtered(lambda move: move.line_ids)
        if not moves:
            return
        prec = self.env['decimal.precision'].precision_get('Account')
        self.env['account.move.line'].flush(['debit', 'credit', 'move_id'])
        self.env['account.move'].flush(['journal_id'])
        if self.ids:
            self._cr.execute("""
                SELECT move_id FROM account_move_line WHERE move_id in %s
                GROUP BY move_id HAVING abs(sum(debit) - sum(credit)) > %s
                """, (tuple(self.ids), 10 ** (-max(5, prec))))
            if self._cr.fetchall():
                raise UserError(_("Cannot create unbalanced journal entry."))
        return True

    def action_invoice_register_payment(self):
        return super(AccountMove, self.with_context(
            default_property_id=self.property_id.id, default_tenancy_id=self.new_tenancy_id.id)).action_invoice_register_payment()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    tenancy_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy',
        help='Tenancy Name.')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')
    amount_due = fields.Monetary(
        comodel_name='res.partner',
        related='partner_id.credit',
        readonly=True,
        default=0.0,
        help='Display Due amount of Customer')

    def post(self):
        res = super(AccountPayment, self).post()
        invoice_obj = self.env['account.move']
        context = dict(self._context or {})
        for rec in self:
            if context.get('return'):
                invoice_browse = invoice_obj.browse(
                    context.get('active_id')).new_tenancy_id
                invoice_browse.write({'amount_return': rec.amount})
            if context.get('deposite_received'):
                tenancy_active_id = \
                    self.env['account.analytic.account'].browse(
                        context.get('active_id'))
                tenancy_active_id.write({'amount_return': rec.amount})
        return res

    @api.model
    def create(self, vals):
        res = super(AccountPayment, self).create(vals)
        if res and res.id and res.tenancy_id and res.tenancy_id.id:
            if res.payment_type == 'inbound':
                res.tenancy_id.write({'acc_pay_dep_rec_id': res.id})
            if res.payment_type == 'outbound':
                res.tenancy_id.write({'acc_pay_dep_ret_id': res.id})
        return res

    def _prepare_payment_moves(self):
        rec = super(AccountPayment, self)._prepare_payment_moves()
        for line in rec:
            line['asset_id'] = self.property_id.id
            line['source'] = self.tenancy_id.name
            if line and line.get('line_ids'):
                for move in line.get('line_ids'):
                    if move and move[2] and self._context.get('account_deposit_received'):
                        if move[2].get('debit') > 0 and self.tenancy_id and self.tenancy_id.id:
                            if self.payment_type in ('inbound', 'outbound'):
                                move[2].update({
                                    'analytic_account_id': self.tenancy_id.id,
                                    'property_id': self.property_id.id
                                            })
        return rec


class AccountInvoice(models.Model):
    _inherit = "account.move"

    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')
    new_tenancy_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy')

