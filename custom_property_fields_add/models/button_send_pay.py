#-*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError

class button_send_deposit (models.Model):
    _inherit = "account.payment"
    def action_quotation_send(self):
            """
            Envio correo electronico de depositos de inquilino
            """
            if not self.partner_id:
                raise UserError ("No cuentas con un socio")
            if not self.company_id:
                raise UserError("No cuentas con un remitente")
            template_id=self.env.ref('custom_property_backend.email_template_depositos_de_inquilino').id
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(self.id, force_send=True)
           

   