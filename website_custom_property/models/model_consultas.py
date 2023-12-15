#-*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError
class Website_consult(models.Model):

    _name='alert.clock'

    _rec_name="duenos_id"

    _order = 'create_date desc'

    actividad=fields.Selection(
        string='Actividad',
        selection=[
                 ('new_payment', 'Nuevo pago'),
                 ('new_tenancy', 'Nuevo contrato'),
                 ('checking_in', 'Comprobada Entrada'),
                 ('checking_out', 'Comprobada Salida'),
                 ('deposit_received', 'Deposito recibido'),
                 ('deposit_returned', 'Deposito devuelto'),
             
        ],
        )
    
    propiedad_id = fields.Many2one('account.asset.asset',string='Propiedad')

    contratos_id = fields.Many2one('account.analytic.account',string='Contratos')

    duenos_id = fields.Many2one('landlord.partner',string='Dueños')

    marcarleido = fields.Boolean(
        string='leido',
    ) 

    
class Website_payment_tenancy(models.Model):

    _inherit='account.payment'

    def insert_accion(self,accion):
        self.env['alert.clock'].create({
            'actividad':accion,
            'propiedad_id':self.property_id.id,
            'contratos_id':self.tenancy_id.id,
            'duenos_id':self.property_id.property_owner.id,
        })

    def post(self):
        res=super(Website_payment_tenancy,self).post()
        if self.partner_type=='supplier' and self.payment_type=='outbound':
            self.insert_accion('deposit_returned')
        #recepcion de dinero    
        if self.partner_type=='customer' and self.payment_type=='inbound' and self.communication=="Deposit Received":
            self.insert_accion('deposit_received')        
        #pago normal
        if self.partner_type=='customer' and self.payment_type=='inbound' and self.communication!="Deposit Received":
            self.insert_accion('new_payment')
        return res
