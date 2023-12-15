
#-*- coding: utf-8 -*-
from datetime import date, datetime

from odoo import models, fields, api,_
from odoo.exceptions import UserError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
class Calendar_event_manager(models.Model):

	_inherit="calendar.event"


	property_calendary = fields.Many2one(
	    'account.asset.asset',
	    string='Propiedad',
	)
	property_tanency = fields.Many2one(
	    'account.analytic.account',
	    string='Contrato',
	)



	    


