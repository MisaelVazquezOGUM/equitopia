from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import base64

class AccountAssetAsset(models.Model):
	_inherit = 'account.asset.asset'
	_description = 'images.power.bi'

	url_image = fields.Char()

	def _generate_images(self):
		records = self.env['account.asset.asset'].search([])
		print("+++++++++++++++++++++++++++++++++++++++ AQUI ESTAS DANDO CLICK +++++++++++++++++++++++++++++++++++++++")
		for record in records:
			#print("Esto es record",record)
			if record.image:
				#print("Ingresa cuando tiene imagen")
				file_send =  base64.b64decode(record.image)
				try:
					#genera un nuevo archivo con mismo nombre y mismo contenido en la ruta dada
					open(f'/odoo/custom/produccion/equitopia/images_power_bi/static/images_power_bi/imagen_{record.id}.jpg','wb').write(file_send)
				except Exception as e:
					raise ValidationError(f'Ocurrio un error al genrar el archivo local: {e}')
				url_local = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
				record.url_image = str(url_local) + f'/images_power_bi/static/images_power_bi/imagen_{record.id}.jpg'
			else:
				url_local = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
				#print("Ingresa cuando no tiene imagen",url_local)
				record.url_image = str(url_local) + '/images_power_bi/static/images_power_bi/sin_imagen.jpg'
				