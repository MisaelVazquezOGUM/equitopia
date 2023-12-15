# © <2022> <proogeeks (dev@proogeeks.com) (dev@proogeeks.com)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class BoardPowerBi(models.Model):
    _name = 'board.power.bi'
    _description = 'Embeber tableros power bi'

    def get_url_power_bi(self):
        valor = self.env['board.power.bi'].search([('power_bi_general','=',True)]).name
        if valor != False or valor != '':
            url = f'<iframe title="Tablero General Rentas"  style="height: 100%; width: 100%; position: absolute;" src="{valor}" frameborder="0" allowFullScreen="true"></iframe>'  
            self.url = url
        else:
            self.url = f'<br/><h2 style="text-align: center;">Configure la URL de Power BI...</h2>'
   
         
    name = fields.Char(string='Tablero URL')
    power_bi_general = fields.Boolean(string='Activo', default=False)
    url = fields.Html(string="URL", sanitize = False, compute='get_url_power_bi')
    user = fields.Char(string="Usuario")
    password = fields.Char(string="Contraseña")
    