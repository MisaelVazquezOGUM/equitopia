import requests
import base64
import uuid
import time
import os

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account' 

    def generate_and_send_report(self):
        report_obj = self.env['ir.actions.report']
        target_report = report_obj._get_report_from_name('custom_property.report_contrato_general')
        pdf_data, file_type = target_report.render_qweb_pdf(self.ids)
        
        pdf_url = self.save_pdf_and_get_url(pdf_data)
        self.send_pdf_link_via_whatsapp(pdf_url)


    def send_pdf_link_via_whatsapp(self, pdf_url):
        url = "https://graph.facebook.com/v17.0/115201561685325/messages"
        access_token = "EAAJTGwjKcC4BO5Ul3dzbjjH6chZAhwI7g4ZBOl7RHzTTH1Tsq8niUoGg9cPZCzafpPI7nFTiOyg2bLroOZAX1qG1DVaZByOjgOQetdktpX74UOUs2esfHKB8nQCpWk2rNuM126hfkDI6ZA5CWz9CAHXhOXLZA1XCZA5bNh04O6rwLhlb0OVJx2xow7sFFDbtuaaN"  # Replace with your token
        
        data = {
            "messaging_product": "whatsapp",
            "to": "",  # Replace with target phone number
            "type": "text",
            "text": {
                "body": f"Hola, aquí está el contrato que solicitaste: {pdf_url}."
            }
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)
        _logger.info(response.text)


    def save_pdf_and_get_url(self, report_binary_data):
        # Generate a unique filename
        unique_id = uuid.uuid4().hex
        timestamp = int(time.time())
        report_name = f"contract_{self.id}_{timestamp}_{unique_id}.pdf"
        current_directory = os.getcwd()
        _logger.info("XXXXXXXXXXXX")
        _logger.info(current_directory)

        # Define the directory to save files
        directory_path = '/home/misael/odoo/contractfiles/'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        save_path = os.path.join(directory_path, report_name)

        _logger.info("XXXXXXXXXXXX")
        _logger.info(save_path)
        with open(save_path, 'wb') as file:
            file.write(report_binary_data)
        
        # Replace the following URL with your actual ngrok URL
        public_url = f'https://4938-189-232-196-131.ngrok-free.app/contractfiles/{report_name}'
        return public_url