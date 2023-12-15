
#-*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class Graph_view_state(models.Model):

	_name="graph.state.result"

	_rec_name="property_id"

	rentas_efectivas = fields.Float(
	    string='Rentas efectivas',
	)

	fecha_report = fields.Datetime(
	    string='Fecha',
	)

	total_gastos = fields.Float(
	    string='Total gastos',
	)

	ingreso_neto = fields.Float(
	    string='Ingresos netos',
	)

	property_id = fields.Many2one(
	    'account.asset.asset',
	    string='Propiedad',
	)

	mes_cargado = fields.Char(
	    string='Mes',
	)

