#-*- coding: utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import UserError

class get_image (models.Model):
    
    _inherit = "account.payment"
    image= fields.Binary(string = "imagen", attachment=True )
    direccion= fields.Char(string = "Dirección")#compute = '_set_direccion',store = Tru
    Cheak_in = fields.Datetime(string = "Cheak In")
    Cheak_out = fields.Datetime(string = "Cheak out")
  
    
    # FIXME
    # def create(self, values):
    #     
    #     propiedad= self.env['account.asset.asset'].search([
    #         ('id','=',int (values['property_id']))])
    #     contrato= self.env['account.analytic.account'].search([
    #         ('id','=',int (values['tenancy_id']))])
    # 
    #     values.update({
    #         'direccion':self.set_direccion(propiedad),
    #         'image':propiedad.image,
    #         'Cheak_in':contrato.chech_in,
    #         'Cheak_out':contrato.chech_out,
    #         
    #         })
    #     raise UserError(str(values['tipo_de_propiedad']))
    #     
    #     rest = super(get_image, self).create(values)
    #     return rest
    
    
         
    def set_direccion(self, propiedad):
        
        direccion = ''
        if propiedad.street: 
            direccion += propiedad.street +' '
        if propiedad.street2:
            direccion += propiedad.street2 +' '
        if propiedad.township: 
            direccion += propiedad.township +' '
        if propiedad.city:
            direccion += propiedad.city +' '
        if propiedad.state_id:
            direccion += propiedad.state_id.name +' '
        if propiedad.zip :
            direccion += propiedad.zip  +' '
        if propiedad.country_id:
            direccion += propiedad.country_id.name +' '
        return direccion
            
    def _set_imagen(self):
        for rec in self:
            if rec.property_id: 
                rec.image = rec.property_id.image
            
            
    
   
