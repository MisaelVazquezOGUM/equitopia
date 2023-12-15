from odoo import http
from odoo.http import request
import os
import logging
from werkzeug.datastructures import FileStorage

_logger = logging.getLogger(__name__)

class ContractController(http.Controller):

    @http.route('/contractfiles/<string:filename>', type='http', auth="public")
    def contract_file(self, filename, **kwargs):
        _logger.info("YYYYYYYYYYYYYYYY")
        _logger.info(filename)
        file_path = os.path.join('/home/misael/odoo/contractfiles/', filename)
        _logger.info(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                file_storage = FileStorage(file)
                return request.make_response(file_storage.read(), [
                    ('Content-Type', 'application/pdf'),
                    ('Content-Disposition', f'attachment; filename={filename}')
                ])
        else:
            return request.not_found()
