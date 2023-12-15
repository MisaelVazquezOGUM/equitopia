
#-*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError
from datetime import date,datetime
import calendar
import re
import dateutil.relativedelta
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from odoo.modules import get_module_path
import numpy as np
import logging
_logger = logging.getLogger(__name__)
# report de resultado de todo el hisorial de cada propiedad
# con sus metricas
class Estado_resultados(models.Model):

	_name="estado.result"
	_rec_name="mes_estado"

	property_id = fields.Many2one(
	    'account.asset.asset',
	    string='Property',
	)

	company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id)

	currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.currency_id',
        string='Currency',
        required=True)

	imagen = fields.Binary(
	    string='Photo',
	    attachment=True,
	)

	rent_cronograma = fields.Float(
	    string='Scheduled Rents',
	)
	rent_efectivo = fields.Float(
	    string='Effective Rental',
	)

	ingreso_neto = fields.Float(
	    string='Net Income',
	)
	
	dias_libres = fields.Float(
	    string='Free',
	)
	dias_ocupados = fields.Float(
	    string='Not Free',
	)

	porcent_libre = fields.Float(
	    string='Free',
	)

	procetaje_ocupado = fields.Float(
	    string='Not Free',
	)

	mantenimientos = fields.Float(
	    string='Maintenance',
	)
	servicios = fields.Float(
	    string='Services',
	)
	otros_gastos = fields.Float(
	    string='Other budget',
	)
	comisiones = fields.Float(
	    string='Management Commission',
	)
	#datos historicos
	rent_cobradas = fields.Float(
	    string='Received Rents',
	)
	rent_por_cobrar = fields.Float(
	    string='Rents to Be Received',
	)
	#rango de filtros
	fecha_report = fields.Datetime(
	    string='Report Date',
	    default=lambda self: fields.datetime.now(),
	)

	enviado = fields.Selection([
		('Sent', 'Email Sent'),
    	('Resent', 'Email Resent'),
		])

	manager_id = fields.Many2one(
	    'res.partner',
	    string='Manager',
	)
	owner_id = fields.Many2one(
	    'landlord.partner',
	    string='Owner',
	)

	ingresos_netos = fields.Float(
	    string='Net Income',
	    compute='_compute_total_exp'
	)

	mes_estado = fields.Char(
	    string='Month',
	)

	year_state = fields.Char(string='Year', default=str(date.today().year))

	mes_num=fields.Char(
	    string='No. month',
	)

	estado = fields.Char(
	    string='State',
	)

	foreport = fields.Boolean(
	    string='Website',
	)

	totalgastos_full = fields.Float(
	    string='Total spends',
	)

	preview = fields.Boolean(
	    string='Preview',
	)

	reservaciones = fields.Text(
	    string='Reservations',
	)

	expense_table_ids = fields.One2many(
        comodel_name='expense.table',
        inverse_name='state_result_id',
        string='Expense Table')
	
	tot_exp = fields.Float(string='Total Expense', compute='_compute_total_exp')

	@api.model
	def default_get(self, fields_list):
		defaults = super(Estado_resultados, self).default_get(fields_list)
		active_id = self.env.context.get('active_id')
		if active_id or active_id != '': 
			defaults['property_id'] = active_id

		return defaults


	@api.depends('expense_table_ids')
	def _compute_total_exp(self):
		income = 0
		discharge = 0
		if self.expense_table_ids:
			records = self.env['expense.table'].search([('state_result_id','=',self._origin.id)])
			for rec in records:
				income += rec.enter_pay
				discharge += rec.exit_pay

			self.tot_exp = income - discharge  
			self.ingresos_netos = income - discharge 
		else:
			self.tot_exp = 0.0
			self.ingresos_netos = 0.0

	invoice_com_id = fields.Many2one(comodel_name='commission.invoice')
    #Al seleccionar una propiedad llama a la funcion o accion para cargar los respectivos datos 
	@api.onchange('property_id')
	def _onchange_property_id(self):
		fecha_actual=self.fecha_report
		# dict_state={
		# 	'new_draft':'Reserva Abierta',
		# 	'draft':'Disponible',
		# 	'normal':'En Arrendamiento',
		# 	'close':'Ventas',
		# 	'sold':'Vendido',
		# 	'open':'Correr',
		# 	'cancel':'Cancelar',
		# 	}
		dict_state = {
			'new_draft': 'Open Reservation',
			'draft': 'Available',
			'normal': 'In Lease',
			'close': 'Sales',
			'sold': 'Sold',
			'open': 'Run',
			'cancel': 'Cancel',
		}
		self.mes_estado=self.mes_find(fecha_actual.month)
		self.mes_num=fecha_actual.month
		if self.property_id:
			self.imagen=self.property_id.image
			self.manager_id=self.property_id.property_manager.id
			self.owner_id=self.property_id.property_owner.id
			self.estado=dict_state[self.property_id.state]
			self.calc_property_id()
			if self._origin.id:
				if self.expense_table_ids.ids:
					self.env['expense.table'].go_update(self.property_id.id, self._origin.id, self.fecha_report)
					self.env['expense.table'].go_create(self.property_id.id, self._origin.id, self.fecha_report)
				else:
					self.env['expense.table'].go_create(self.property_id.id, self._origin.id, self.fecha_report)

	def unlink(self):
		for rec in self:
			if rec.expense_table_ids:
				for exp_tab in rec.expense_table_ids:
					exp_tab.delete_all(rec.id)
		return super(Estado_resultados, self).unlink()


	def update_this_record(self):
		for rec in self:
			rec._onchange_property_id()

	def update_record(self):
		records = self.env['estado.result'].search([])
		for rec in records:
			rec._onchange_property_id()
			_logger.info(f'********Records State Result Updated*******')

	@api.model
	def _disable_days(self):
		cal = calendar.setfirstweekday(calendar.SUNDAY)
		cal = calendar.monthcalendar(date.today().year,date.today().month)
		
		fech = datetime.now()
		days = 0
		days_max=calendar.monthrange(int(fech.year),int(fech.month))
		date_start=date(int(fech.year),int(fech.month),1)
		date_stop=date(int(fech.year),int(fech.month),int(days_max[1]))	
		reservaciones=self.env['calendar.event'].search([('property_calendary','=',self.property_id.id),
			('start','>=',date_start),('stop','<=',date_stop)])

		if reservaciones:
			for item in reservaciones:
				days = (item.stop-item.start).days
				init = item.start.day
				end = item.stop.day
				for i in range(len(cal)):
					for j in range(len(cal[i])):
						if type(cal[i][j]) == int:
							if cal[i][j] == 0:
								cal[i][j] = ' '
							elif cal[i][j] >= init and cal[i][j] <= end:
								cal[i][j] ='X'
							else:
								cal[i][j] = str(cal[i][j])
						elif type(cal[i][j]) == str:
							if cal[i][j].isdigit():
								if int(cal[i][j]) >= init and int(cal[i][j]) <= end:
									cal[i][j] ='X'
		else:
			for i in range(len(cal)):
				for j in range(len(cal[i])):
					if type(cal[i][j]) == int:
						if cal[i][j] == 0:
							cal[i][j] = ' '
						else:
							cal[i][j] = str(cal[i][j])

		return cal
			#Seteo de variable de calendario



	def action_state_property_unic_send(self):
		"""enviar por correo de forma unica ya generado el reporte"""
		if not self.manager_id:
			raise UserError("No cuentas con mangejandro de cuenta")
		if not self.owner_id:
			raise UserError("No cuenta con Duehow to print a calendar in an odoo qweb reportño para el envio")
		template_id=self.env.ref('custom_property.email_template_estado').id
		self.env['mail.template'].browse(template_id).send_mail(self.id,force_send=True)
		self.enviado='Reenviado'
	
	def action_state_property_send(self,linea_values):
		"""
		envia correo electronico de los estados de propiedad
		valida sus respetivos remitentes y destinatarios
		"""
		template_id=self.env.ref('custom_property.email_template_estado').id
		self.env['mail.template'].browse(template_id).send_mail(linea_values.id,force_send=True)
		linea_values.enviado='Enviado'

	'''Metodo para generar la factura de la comision del total del estado de la cuenta'''
	def generate_invoice_to_supplier(self):
		today = date.today()
		invoice_obj = self.env['commission.invoice']
		if self.property_id:

			if self.ingresos_netos == 0:
				raise ValidationError(_('Cannot generate invoice with value 0'))
			if self.ingresos_netos < 0:
				raise ValidationError(_('Invoice cannot be generated with negative income'))
			invoice_sup_dict = {
				'date': today,
				'description':'Payment of income commission for the month of '+ self.mes_estado,
				'property_id': self.property_id.id or False,
				'agent':self.property_id.property_manager.id or False,
				'commission_type':'fixed',
				'amount_total':self.ingresos_netos,
				'currency_id':self.property_id.currency_id.id
			}
			self.invoice_com_id = invoice_obj.create(invoice_sup_dict)
			self.invoice_com_id.create_commission_invoice()
		else:
			raise ValidationError(_('Select a property'))


			'''inv_line_dict = {
				'quantity': 1,
				'price_unit': self.ingresos_netos * (self.property_id.commission_percentage/100) or 0.0,
				'account_id': self.property_id.expense_account_id.id or False,
				'name': 'Pago de Comisión de rentas del Mes de '+ self.mes_estado,
				'is_service': False,
				'maintenance_id': False,
			}

			inv_line_values = {
				'partner_id': self.property_id.property_manager.id or False,
				'type': 'in_invoice',
				'invoice_line_ids': [(0, 0, inv_line_dict)],
				'property_id': self.property_id.id or False,
				'gastos_extra': False,
				'is_commission': True,
			}
			_logger.info(inv_line_values)

			self.invoice_id = invoice_obj.create(inv_line_values)
			self.invoice_id.action_post()
		else:
			raise ValidationError(_('Select a property'))'''

	'''Metodo para lanzar la vista de la factura de la comision generada'''
	def view_record_invoice(self):
		view = self.env.ref('account.view_move_form')

		launch_view = {
			'name':_("Factura a Proveedor"),
			'res_model':'account.move',
			'views':[(view.id,'form')],
			'type': 'ir.actions.act_window',
			'target': 'current',
			'res_id': self.invoice_com_id.invc_id.id
		}
		return launch_view
	
	def mes_find(self,mes):
		vec=['','JUNUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']
		return vec[mes]	

	def drawing_chats_rent(self):		
		titles=["Programadas","Efectivas"]
		rentas_estados=[self.rent_cronograma,self.rent_efectivo]
		plt.bar(titles,rentas_estados,color="blue",width=0.4)
		plt.title("Rentas")
		path = get_module_path('custom_property')
		plt.savefig(path+'/static/src/img/rentbar.png')
		plt.close()
	
	def drawing_chats_porcent(self):
		estados_propiedad = [self.porcent_libre,self.procetaje_ocupado]
		title_porcent = ["Libre","Ocupado"]
		plt.pie(estados_propiedad, labels=title_porcent, autopct="%0.1f %%")
		plt.axis("equal")
		plt.title("Porcetajes de ocupacion")
		path = get_module_path('custom_property')
		plt.savefig(path+'/static/src/img/procetajeocupacion.png')
		plt.close()

	def drawing_chats_histo(self):
		historial_rentas=[self.rent_cobradas,self.rent_por_cobrar]
		titles=['RC','RPC']
		plt.bar(titles,historial_rentas,color="blue",width=0.4)
		plt.title("historial rentas")
		path = get_module_path('custom_property')
		plt.savefig(path+'/static/src/img/historibar.png')
		plt.close()

	def drawing_chats_metric(self):
		metricas=[self.mantenimientos,self.servicios,self.otros_gastos,self.comisiones]
		titles=['Man','Servi','OG','Comi']
		plt.bar(titles,metricas,color="blue",width=0.4)
		plt.title("Metricas")
		path = get_module_path('custom_property')
		plt.savefig(path+'/static/src/img/metricbar.png')
		plt.close()

	#Funcion que nunca se manda a llamar
	def drawin_chart_bar_histor(self):
		total_neta=[0,0,0,0,0,0,0,0,0,0,0,0]
		total_gastos=[0,0,0,0,0,0,0,0,0,0,0,0]

		fecha_actual=datetime.now()
		inicio=datetime(fecha_actual.year,1,1)
		fin=datetime(fecha_actual.year,12,31)

		data=self.env['estado.result'].search([('id','=',self.id),('fecha_report','>=',inicio),
			('fecha_report','<=',fin)])	

		x=0
		for item in data:
			gastos=item.mantenimientos+item.servicios+item.otros_gastos+item.comisiones
			total_neta[x]=item.ingresos_netos
			total_gastos[x]=gastos
			x=x+1

		#titles=['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SET','OCT','NOV','DIC']
		titles = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


		x_axis=np.arange(len(titles))

		plt.bar(x_axis-0.2,total_neta,0.4,label="Income")
		plt.bar(x_axis+0.2,total_gastos,0.4,label="Expenses")

		plt.xticks(x_axis,titles)
		plt.xlabel("Month")
		plt.ylabel("Quantity")
		plt.title("Income vs expenses")
		plt.legend()	
		path = get_module_path('custom_property')
		plt.savefig(path+'/static/src/img/total.png')
		plt.close()

	def calc_property_id(self):		
		if self.property_id:
			#si no entonces toma solo el de la consulta como resultado solo una propiedad
			propiedades=self.env['account.asset.asset'].search([('id','=',self.property_id.id)])
		else:
			#si el campo de propiedad esta vacio como resultado todas las propiedades
			propiedades=self.env['account.asset.asset'].search([])		

		
		fecha_actual=self.fecha_report
		report_id=0
		days_max=calendar.monthrange(int(fecha_actual.year),int(fecha_actual.month))
		date_start=date(int(fecha_actual.year),int(fecha_actual.month),1)
		date_stop=date(int(fecha_actual.year),int(fecha_actual.month),int(days_max[1]))		
		datfor=self.env['estado.result']
		for item in datfor.search([('foreport','=',True),('mes_num','=',int(fecha_actual.month))]):
			item.foreport=False		
		for pd in propiedades:
			pagos=self.env['account.payment']
			contratos=self.env['account.analytic.account']
			#rentas
			rent_cobradas=sum(self.env['tenancy.rent.schedule'].search([
				('paid','=',True),
				('property_id','=',pd.id)]).mapped('amount'))

			rent_por_cobrar=sum(self.env['account.move'].search([('type','=','out_invoice'),
				('property_id','=',pd.id)]).mapped('amount_residual'))				
			#rentas mensual
			rent_efectivo_ten = self.env['tenancy.rent.schedule'].search([
				('paid','=',True),
				('move_check','=',True),
				('property_id','=',pd.id)])
			if rent_efectivo_ten:
				ids_rent = [x.invc_id.id for x in rent_efectivo_ten]
				
				rent_efectivo = sum(pagos.search([('property_id','=',pd.id),('tipo_de_pago','=','r'),
							('payment_date','>=',date_start),('payment_date','<=',date_stop),('invoice_ids','in',ids_rent)]).mapped('amount'))
				_logger.info(f'***********rents_pay: {rent_efectivo}')
			else:
				rent_efectivo = 0.0

			rent_cronograma=sum(self.env['tenancy.rent.schedule'].search([
				('paid','=',False),
				('move_check','=',True),
				('property_id','=',pd.id),
				('start_date','>=',date_start),
				('start_date','<=',date_stop)]).mapped('amount'))
			

			#servicos
			servicios=sum(pagos.search([('property_id','=',pd.id),('tipo_de_pago','=','s'),
					('payment_date','>=',date_start),('payment_date','<=',date_stop)]).mapped('amount'))
			#mantenimientos
			mantenimientos=sum(pagos.search([('property_id','=',pd.id),('tipo_de_pago','=','m')]).mapped('amount'))
			#eservaciones
			activiades=self.env['calendar.event'].search([('start_date','>=',date_start),
				('stop_date','<=',date_stop),('property_calendary','=',pd.id)])
			ocupados=0			
			for item in activiades:
				ocupados+=(item.stop_date-item.start_date).days

			dias_ocupados=ocupados
			procetaje_ocupado=(ocupados*100)/int(days_max[1])
			dias_libres=int(days_max[1])-ocupados
			porcent_libre=100-procetaje_ocupado
			otros_gastos=sum(pagos.search([('property_id','=',pd.id),('tipo_de_pago','=','o'),
			  	('payment_date','>=',date_start),('payment_date','<=',date_stop)]).mapped('amount'))

			reservaciones=self.env['calendar.event'].search([('property_calendary','=',pd.id),
				('start','>=',date_start),('stop','<=',date_stop)])

			html=''
			for item in reservaciones:
				html+=str(item.start)+">"+str(item.stop)+'\n'

			# dict_state={
			# 'new_draft':'Reserva Abierta',
			# 'draft':'Disponible',
			# 'normal':'En Arrendamiento',
			# 'close':'Ventas',
			# 'sold':'Vendido',
			# 'open':'Correr',
			# 'cancel':'Cancelar',
			# }

			dict_state = {
				'new_draft': 'Open Reservation',
				'draft': 'Available',
				'normal': 'In Lease',
				'close': 'Sales',
				'sold': 'Sold',
				'open': 'Running',
				'cancel': 'Cancelled',
			}

			totalgastos=mantenimientos+servicios+otros_gastos		

			#comsiones
			#comisiones=sum(pagos.search([('property_id','=',pd.id),('tipo_de_pago','=','c'),
			#  	('payment_date','>=',date_start),('payment_date','<=',date_stop)]).mapped('amount'))
			comisiones=sum(contratos.search([('property_id','=',pd.id),('commission','=',True),
			  	('chech_in','>=',date_start),('chech_in','<=',date_stop)]).mapped('total_commission'))

			if len(propiedades)>1:
				data_save={
			     'property_id':pd.id, 
				 'fecha_report':fecha_actual,
				 'manager_id':pd.property_manager.id,
				 'owner_id':pd.property_owner.id,				 
				 'imagen':pd.image,
				 'rent_cobradas':rent_cobradas,
				 'rent_cronograma':rent_cronograma,
				 'rent_por_cobrar':rent_por_cobrar,
				 'rent_efectivo':rent_efectivo,
				 'servicios':servicios,
				 'mantenimientos':mantenimientos,
				 'dias_ocupados':dias_ocupados,
				 'procetaje_ocupado':procetaje_ocupado,
				 'dias_libres':dias_libres,
				 'porcent_libre':porcent_libre,
				 'otros_gastos':otros_gastos,
				 'mes_estado':self.mes_find(fecha_actual.month),
				 'year_state':str(date.today().year),
				 'mes_num':fecha_actual.month,
				 'estado':dict_state[pd.state],
				 'foreport':True,
				 'totalgastos_full':totalgastos,
				 'preview':True,
				 'recervaciones':html,
				 'comisiones':comisiones
				}
				estados_lista=datfor.search([('property_id','=',pd.id),('foreport','=',True)])
				if len(estados_lista)>=1:
					estados_lista.update(data_save)
					if pd.send_state_result:
						self.action_state_property_send(estados_lista)
				else:
					linea_values=self.create(data_save)
					if pd.send_state_result:
						self.action_state_property_send(linea_values)

	
			else:
				self.rent_cobradas=rent_cobradas
				self.rent_cronograma=rent_cronograma
				self.rent_por_cobrar=rent_por_cobrar
				self.rent_efectivo=rent_efectivo
				self.servicios=servicios
				self.mantenimientos=mantenimientos
				self.otros_gastos = otros_gastos
				self.dias_ocupados=dias_ocupados
				self.procetaje_ocupado=procetaje_ocupado
				self.dias_libres=dias_libres
				self.porcent_libre=porcent_libre
				self.foreport=True
				self.totalgastos_full=totalgastos
				self.reservaciones=html
				self.comisiones=comisiones
				#self.preview=False


			#cargar informacion para la graficar


			# graphmonth=self.env['graph.state.result'].search([('mes_cargado','=',str(fecha_actual.month))])
		
			# if len(graphmonth):
			# 	graphmonth.update({
			# 		'ingreso_neto':rent_efectivo-(totalgastos),
			# 		'total_gastos':totalgastos,
			# 		'rentas_efectivas':rent_efectivo,
			# 		'fecha_report':fecha_actual,
			# 		'mes_cargado':fecha_actual.month
			# 		})
			# else:
			# 	self.env['graph.state.result'].create({
			# 		'property_id':pd.id,
			# 		'ingreso_neto':rent_efectivo-(totalgastos),
			# 		'total_gastos':totalgastos,
			# 		'rentas_efectivas':rent_efectivo,
			# 		'fecha_report':fecha_actual,
			# 		'mes_cargado':fecha_actual.month
			# 		})

#si en  dado caso se el reporte de hace cada dia 1 de mes entonce hay que restarle uno al mes