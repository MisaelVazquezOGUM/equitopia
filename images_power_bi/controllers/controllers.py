# -*- coding: utf-8 -*-
# from odoo import http


# class ImagesPowerBi(http.Controller):
#     @http.route('/images_power_bi/images_power_bi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/images_power_bi/images_power_bi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('images_power_bi.listing', {
#             'root': '/images_power_bi/images_power_bi',
#             'objects': http.request.env['images_power_bi.images_power_bi'].search([]),
#         })

#     @http.route('/images_power_bi/images_power_bi/objects/<model("images_power_bi.images_power_bi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('images_power_bi.object', {
#             'object': obj
#         })
