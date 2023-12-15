
#-*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class Graph_view_state(models.Model):

	_name="graph.state.result"

	_rec_name="property_id"

	rentas_efectivas = fields.Float(
		string='Effective Rents',
	)

	fecha_report = fields.Datetime(
		string='Date',
	)

	total_gastos = fields.Float(
		string='Total Expenses',
	)

	ingreso_neto = fields.Float(
		string='Net Income',
	)

	property_id = fields.Many2one(
		'account.asset.asset',
		string='Property',
	)

	mes_cargado = fields.Char(
		string='Month',
	)


