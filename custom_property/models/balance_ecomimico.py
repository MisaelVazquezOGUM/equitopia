
#-*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError
from datetime import datetime
import calendar
#cuando son pago o salida de dinera hay quecambiar el tipo de fectura
#que en ves de que creen unfactura de cliente denbe crearuna factruade proveeodor

class Balance_ecomonico_line(models.Model):

	_name="balance.economyc.report"

	_rec_name="property_mov_id"

	balance_economico_ids = fields.One2many(
	    'balance.economyc.report.lines',
	    'balance_economyc_lines_id',
	    string='Economic balance',
	)

	property_mov_id = fields.Many2one(
	    'account.asset.asset',
	    string='Property',
	)

	company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company')
        #default=lambda self: self.env.user.company_id)

	currency_id = fields.Many2one(
        comodel_name='res.currency',
        #related='company_id.currency_id',
        string='Currency')
        #required=True)


	mes_num = fields.Char(
	    string='Month num',
	)

	
	mes = fields.Selection([
		('1', 'JANUARY'),
		('2', 'FEBRUARY'),
		('3', 'MARCH'),
		('4', 'APRIL'),
		('5', 'MAY'),
		('6', 'JUNE'),
		('7', 'JULY'),
		('8', 'AUGUST'),
		('9', 'SEPTEMBER'),
		('10', 'OCTOBER'),
		('11', 'NOVEMBER'),
		('12', 'DECEMBER'),
	], default=lambda self: str(fields.datetime.now().month))


	fecha = fields.Datetime(
	    string='Date',
	    default=lambda self: fields.datetime.now(),
	)

	@api.onchange('mes')
	def _onchange_mes(self):
		now=datetime.now()
		if self.mes:
			new_date=now.replace(month=int(self.mes))
			self.fecha=new_date
			self.mes_num=new_date.month


	def update_balance(self):
		self._onchange_fecha()


	@api.onchange('property_mov_id','mes')
	def _onchange_fecha(self):		
		"""
		por medio del decorador onchange se crea el balance economico para la propiedad
		"""
		if self.property_mov_id:			
			propiedades=self.env['account.asset.asset'].search([('id','=',self.property_mov_id.id)])
			dia=calendar.monthrange(self.fecha.year,self.fecha.month)[1]
			inicio=datetime(self.fecha.year,self.fecha.month,1)
			fin=datetime(self.fecha.year,self.fecha.month,dia)
			data=self.env['account.payment'].search([('property_id','=',self.property_mov_id.id),
			('calc_balance','=',False),('state','<>','draft'),('payment_date','>=',inicio),
			 ('payment_date','<=',fin)],order='payment_date asc')

			self.currency_id=self.property_mov_id.currency_id.id


			temp_data_old=[]
			array_data=[]
			acum_mov=0.0

			for item in data:
				cantidad=0.0
				if item.payment_type=='outbound':
					cantidad=item.amount*-1
					array_data.append(cantidad)
					acum_mov=acum_mov-item.amount
				else:
					cantidad=item.amount
					array_data.append(cantidad)
					acum_mov=acum_mov+item.amount
				text_descrip=''
				for inv_fac in item.invoice_ids:
					for line in inv_fac.invoice_line_ids:
						text_descrip=line.name+'\n'

				temp_data_old.append((0,0,
					{
						 'payment_mov_id':item.id,
						 'date_mov':item.payment_date,
						 'type_mov':item.payment_type,
						 'type_payment':item.tipo_de_pago,
						 'cant_mov':cantidad,
						 'acum_mov':acum_mov,
						 'decription_mov':item.communication,
						 'currency_id':item.currency_id.id or False,
						 'line_invoice':text_descrip,						 
					}
					))
				item.calc_balance=True

			self.update({
				'balance_economico_ids':[(5,0,0)],
				})

			self.update({
				'balance_economico_ids':temp_data_old,
				})			
	

	def create_crono_balance(self):
		"""
		funcion para actualizar todas las propiedades el balances economico
		"""
		propiedades=self.env['account.asset.asset'].search([])
		doc_id=0
		for pd in propiedades:
			#data_balance=[]
			array_data=[]
			actual=datetime.now()
			dia=calendar.monthrange(actual.year,actual.month)[1]
			inicio=datetime(actual.year,actual.month,1)
			fin=datetime(actual.year,actual.month,dia)				

			estados_mensual=self.env['balance.economyc.report'].search([('property_mov_id','=',pd.id),
				('mes_num','=',actual.month)])

			report_balance=0

			if len(estados_mensual)==0:
				new_data={
				'property_mov_id':pd.id,
				'fecha':actual,
				'mes':str(actual.month),
				'mes_num':actual.month,
				}
				report_balance=self.env['balance.economyc.report'].create(new_data)
			else:
				report_balance=self.env['balance.economyc.report'].search([('id','=',estados_mensual.id)])
			temp_data_old=[]		
			for item in estados_mensual.balance_economico_ids:
				temp_data_old.append((1,item.id,{
						 'payment_mov_id':item.payment_mov_id.id,
						 'date_mov':item.date_mov,
						 'type_mov':item.type_mov,
						 'type_payment':item.type_payment,
						 'cant_mov':item.cant_mov,
						 'acum_mov':item.acum_mov,
						 'decription_mov':item.decription_mov,
						 'currency_id':item.currency_id.id or False,
						 'line_invoice':item.line_invoice,
						}))

			if  temp_data_old:
				ult_rec=temp_data_old[len(temp_data_old)-1]
				acum_mov=ult_rec[2]['acum_mov']
			else:
				acum_mov=0.0	

			data=self.env['account.payment'].search([('property_id','=',pd.id),
			('calc_balance','=',False),('state','<>','draft'),('payment_date','>=',inicio),
			('payment_date','<=',fin)],order='payment_date asc')	


			for item in data: #recorre toda la informacion de pagos de la propiedad
				cantidad=0.0
				if item.payment_type=='outbound':
					cantidad=item.amount*-1
					array_data.append(cantidad)
					acum_mov=acum_mov-item.amount
				else:
					cantidad=item.amount
					array_data.append(cantidad)
					acum_mov=acum_mov+item.amount

				text_descrip=''
				for inv_fac in item.invoice_ids:
					for line in inv_fac.invoice_line_ids:
						text_descrip=line.name+'\n'
				#bucar si hay un balance creado
				temp_data_old.append((0,0,
					{
					     'payment_mov_id':item.id,
						 'date_mov':item.payment_date,
						 'type_mov':item.payment_type,
						 'type_payment':item.tipo_de_pago,
						 'cant_mov':cantidad,
						 'acum_mov':acum_mov,
						 'decription_mov':item.communication,
						 'currency_id':item.currency_id.id or False,
						 'line_invoice':text_descrip,
					}
					))
				item.calc_balance=True		

			
			report_balance.update({
				'balance_economico_ids':temp_data_old,
				})

class Balance_ecomonico(models.Model):

	_name="balance.economyc.report.lines"

	_rec_name='company_id'

	##id relaccion
	property_mov_id = fields.Many2one(
	    'account.asset.asset',
	    string='Propiedad',
	)

	date_mov = fields.Date(
	    string='Fecha de movimiento',
	)
	
	type_mov = fields.Selection([
		('outbound', 'Send Money'),
		('inbound', 'Receive Money'),
		('transfer', 'Internal Transfer')
	])



	type_payment = fields.Selection([('r', "Rent"), 
		("m", "Maintenance"), ("s", "Service"), ("o", "Other"), ("c", "Comissions")])

	cant_mov = fields.Float(string='Quantity')

	acum_mov = fields.Float(string='Accumulated')

	decription_mov = fields.Char(string='Description')

	payment_mov_id = fields.Many2one('account.payment',
	    string='Payment')


	company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company')
       # default=lambda self: self.env.user.company_id)

	currency_id = fields.Many2one(
        comodel_name='res.currency',
        #related='company_id.currency_id',
        string='Currency')
        #required=True)

	line_invoice = fields.Text(
	    string='Payment development',
	)

	balance_economyc_lines_id = fields.Many2one(
	    'balance.economyc.report',
	    string='Balance economic lines',
	)
