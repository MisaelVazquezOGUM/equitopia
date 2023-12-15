
#-*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class Tenant_partner_user(models.Model):

    _inherit="tenant.partner"

    portal_activo=fields.Boolean(string='Portal')

    bandera_portal=fields.Boolean(string='Portal',compute="_no_interno")
    def _no_interno(self):
        group_internal=self.env.ref('base.group_user')
        res_tenant=self.env['res.users'].search([('tenant_id','=',self.id)])
        res_tenant.write({'groups_id': [(3, group_internal.id)]})
        self.bandera_portal=False    
    def active_portal(self):    
        group_portal=self.env.ref('base.group_portal')
        res_tenant=self.env['res.users'].search([('tenant_id','=',self.id)])
        res_tenant.write({'groups_id': [(4, group_portal.id)]})
        self.portal_activo=True
        sql_update="""UPDATE res_users SET password=1 WHERE tenant_id = %s"""%self.id
        self.env.cr.execute(sql_update)
        
class Landlord_partner_list(models.Model):

    _inherit="landlord.partner"

    dashbord = fields.Boolean(
        string='Dashbord',
        compute="_watch_dashbord"
    )

    portal_activo=fields.Boolean(string='Portal')
    bandera_portal=fields.Boolean(string='Portal',compute="_no_interno")
    def _no_interno(self):
        """
        Al cargar de inicio el usuario se saca del grupo para meterlo a otro
        """
        group_internal=self.env.ref('base.group_user')
        res_tenant=self.env['res.users'].search([('partner_id','=',self.parent_id.id)])
        res_tenant.write({'groups_id': [(3, group_internal.id)]})
        self.bandera_portal=False

    def active_portal(self):
        """
        Para activar el usuario portal de dueno o compañia
        """
        group_portal=self.env.ref('base.group_portal')
        res_tenant=self.env['res.users'].search([('partner_id','=',self.parent_id.id)])
        res_tenant.write({'groups_id': [(4, group_portal.id)]})
        self.portal_activo=True
        sql_update="""UPDATE res_users SET password=1 WHERE partner_id = %s"""%self.parent_id.id
        self.env.cr.execute(sql_update)


    def _watch_dashbord(self):
        """
        Mientras que este marcado como dueño simpre estara el grupo que puede ver el dashbord
        Si se desmarca como dueño en es momento se saca del grupo que puede ver el dashbord
        """
        group_portal_dashbord=self.env.ref('website_custom_property.group_portal_dashbord')
        res_tenant=self.env['res.users'].search([('partner_id','=',self._origin.parent_id.id)])
                    
        if self.is_owner:
            res_tenant.write({'groups_id': [(4, group_portal_dashbord.id)]})
            self.dashbord=False
        else:
            res_tenant.write({'groups_id': [(3, group_portal_dashbord.id)]})
            self.dashbord=False

        
    partner_property_ids = fields.One2many(
        'property.usuers',
        'line_property_id',
        string='User Properties',
    )

    def ver_propiedades(self):        
        propiedades=self.env['account.asset.asset'].search([('property_owner','=',self.id)])
        for item in propiedades:
            bandera_busqueda=False            
            for list_all in self.partner_property_ids:
                if list_all.nombre.id==item.id:
                    lista_data={
                    'partner_property_ids':[(1,list_all.id,{
                        'nombre':item.id,
                        'tipo_alquile_id':item.rent_type_id.id,
                        'img_propiedad':item.image,
                        'alquiler':item.ground_rent,
                        'state':item.state
                        })]
                    }
                    self.write(lista_data)                    
                    bandera_busqueda=True

            if not bandera_busqueda:
                lista_data={
                'partner_property_ids':[(0,0,{
                    'nombre':item.id,
                    'tipo_alquile_id':item.rent_type_id.id,
                    'img_propiedad':item.image,
                    'alquiler':item.ground_rent,
                    'state':item.state
                    })]
                }
                self.write(lista_data)


class Landlord_partner_property_lines(models.Model):

    _name = 'property.usuers'

    nombre = fields.Many2one('account.asset.asset',string='Property')

    img_propiedad = fields.Binary(string='Property Image',attachment=True)

    tipo_alquile_id = fields.Many2one('rent.type',string='Rental Type')

    alquiler = fields.Integer(string='Rent')

    state=fields.Selection(
        string='State',
        selection=[
                 ('new_draft', 'Open Reservation'),#
                 ('draft', 'Available'),
                 ('normal', 'At Lease'),
                 ('close', 'Reduction'),
                 ('sold', 'Sold'),
                 ('open', 'Open'),
                 ('cancel', 'Cancel')
        ],
        )


    line_property_id = fields.Many2one('landlord.partner',string='Properties')


    









