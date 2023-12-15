# -*- coding: utf-8 -*-
# from odoo import http


# class PropertyMaintenanceSaul(http.Controller):
#     @http.route('/property_maintenance_saul/property_maintenance_saul/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/property_maintenance_saul/property_maintenance_saul/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('property_maintenance_saul.listing', {
#             'root': '/property_maintenance_saul/property_maintenance_saul',
#             'objects': http.request.env['property_maintenance_saul.property_maintenance_saul'].search([]),
#         })

#     @http.route('/property_maintenance_saul/property_maintenance_saul/objects/<model("property_maintenance_saul.property_maintenance_saul"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('property_maintenance_saul.object', {
#             'object': obj
#         })
