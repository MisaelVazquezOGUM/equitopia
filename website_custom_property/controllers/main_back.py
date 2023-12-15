# -*- coding: utf-8 -*-
from curses.ascii import US
from pkgutil import iter_modules
from odoo import http
from odoo.http import Response,request
from odoo.exceptions import UserError
import json
from datetime import date, datetime
import pytz
import locale
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import timedelta
import random
import calendar
class Website_dashborad_property(http.Controller):
    
	def get_user_login(self):
		#usuario que tiene la session iniciada
		usuario=request.env['res.users'].sudo().search([
			('id','=',http.request.env.context.get('uid'))]).partner_id.id
		#propietario
		propierario=request.env['landlord.partner'].sudo().search(
			[('parent_id','=',usuario)]
		).id		
		return propierario

	def data_month(self,ano,mes,invoice):
		mes_inicio=1
		dia_inicio=1
		
		start=date(int(ano),int(mes_inicio),int(dia_inicio))
		stop= date(int(ano),int(mes),int(dia_inicio))		
		
		meses=((stop.year-start.year)*12+stop.month-start.month)+1
		
		fechas_rangos=[]
		dia_suma=calendar.monthrange(int(ano),1)
		fechas_rangos.append([start,date(int(ano),int(1),dia_suma[1])])
		cobrado=[]	

		for item in range(1,meses):
			dias=calendar.monthrange(int(ano),int(item))
			diasuma=calendar.monthrange(int(ano),int(item+1))
			start+=timedelta(days=int(dias[1]))
			fin=date(start.year,start.month,diasuma[1])
			fechas_rangos.append([start,fin])
		
		for vfecha in fechas_rangos:
			total=0.0
			cobrado.append(invoice)
			for inv in invoice:
				data=request.env['account.payment'].sudo().search([
					('communication','=',inv.name),
					('payment_date','>=',vfecha[0]),
					('payment_date','<=',vfecha[1]),
					('tipo_de_pago','=','r')])
				total+=sum(data.mapped('amount'))
			cobrado.append(total)
		return cobrado

	def get_dicc_status(self,value,field):
		"""
		funcion para tomar el label del campo select en ves de su llave
		de las propiedades
		"""
		value_result=''
		kay_val_dict = dict(field._fields['state'].selection)
		for key, val in kay_val_dict.items():
			if key==value:
				value_result=val
		return value_result

	@http.route(['/my_properties/info'], type='json', auth="user", website=True)
	def property_info(self,**kw):
		locale.setlocale(locale.LC_ALL, '')
		formato = '%Y/%m/%d'
		ano=kw.get('ano')
		mes=kw.get('mes')
		seleciona_propiedad=kw.get('propiedad')
		raise UserError(str(seleciona_propiedad))
		month_range=calendar.monthrange(int(ano),int(mes))
		
		start_filter=date(int(ano),int(mes),1)
		stop_filer= date(int(ano),int(mes),int(month_range[1]))

		#buscar propiedades del usuario
		tipo_busqueda=False
		if int(seleciona_propiedad)==-1:
			propidades=request.env['account.asset.asset'].sudo().search(
			[('property_owner','=',self.get_user_login())])
			tipo_busqueda=True
		else:
			propidades=request.env['account.asset.asset'].sudo().search(
			[('property_owner','=',self.get_user_login()),('id','=',seleciona_propiedad)])

			
		data=[]
		html=''
		free_property=[]
		renta_global_total_cobrados=0.0
		rentas_globla_total_pendientes=0.0	
		ingreso_propiedad_cobrados=[]	
		ope_porcent=[]
		etiqueta=[]
		full_total_mente=0.0
		full_total_ser=0.0
		full_neto_total=0.0
		#recorrer propiedades
		for property_tenant in propidades:
			#html+='<tr>'
			contratos=request.env['account.analytic.account'].sudo().search(
				[('property_id','=',property_tenant.id),
				('state','in',['close','open']),
				('is_landlord_rent','=',False)])
			etiqueta.append(property_tenant.name)

			total_rent_general=0.0
			total_rent_pend=0.0
			renta_global_cobrados=0.0
			rentas_globla_pendientes=0.0
			use_property=[]
			data_data=[]
			total_mantenimiento=0.0
			total_servicios=0.0	
			metricas=[]	
			for sumas_itme in contratos:
				for inv_ref in sumas_itme.rent_schedule_ids:
					invoice_payment=request.env['account.payment'].sudo().search([
					('communication','=',inv_ref.invc_id.name),('payment_date','>=',start_filter),
					('payment_date','<=',stop_filer),('tipo_de_pago','=','r')])	
					total_rent_pend+=sum(invoice_payment.mapped('amount'))
					total_rent_general+=inv_ref.invc_id.amount_residual
			#seccion para calcular dias ocupados y libres para la grafica
			#Cargar todas las reservaciones que este en el rengo inicial
			calendary_busy=request.env['calendar.event'].sudo().search([('property_calendary','=',property_tenant.id),
			('start_date','>=',start_filter),('start_date','<=',stop_filer)])

			count_day_busy=0
			for item in calendary_busy:
				count_day_busy+=(item.duration)/24
			use_property.append([			
				int(month_range[1])-count_day_busy,
				count_day_busy,							
			]);			


			invoice=request.env['account.move'].sudo().search([('property_id','=',property_tenant.id)])
			for pagos in invoice:
				#raise UserError(str(invoice.property_id.name))
				
				#consultar los pagos que fueron pago de renta
				renta_global_cobrados=sum(request.env['account.payment'].sudo().
					search([('communication','=',pagos.name),('tipo_de_pago','=','r')]).mapped('amount'))
				#consultar los pagos que fueron de mantenimientos
				total_mantenimiento+=sum(request.env['account.payment'].sudo().
					search([('communication','=',pagos.name),('tipo_de_pago','=','m')]).mapped('amount'))
				#consultar los pagos que fueron de servicio
				total_servicios+=sum(request.env['account.payment'].sudo().
					search([('communication','=',pagos.name),('tipo_de_pago','=','s')]).mapped('amount'))
				renta_global_total_cobrados+=renta_global_cobrados
			rentas_globla_pendientes=sum(invoice.mapped('amount_residual'))
			rentas_globla_total_pendientes+=rentas_globla_pendientes
			full_total_mente+=total_mantenimiento
			full_total_ser+=total_servicios
			ingreso_propiedad_cobrados.append(self.data_month(ano,mes,invoice))

			data_data.append([total_rent_general,total_rent_pend])
			#calcular ingresoneto,Hoa otros gastos	
			#0 total de mantenimientos
			#1 total de servicios
			#2 ingreso neto
			#3 hoa
			#4 otros gastos
			ingreos_neto=renta_global_total_cobrados-(total_mantenimiento+total_servicios)
			full_neto_total+=ingreos_neto

			metricas.append(total_mantenimiento)	
			metricas.append(total_servicios)
			metricas.append(ingreos_neto)
			#metricas2=[4000,2000,1000]
			#raise UserError(metricas)	


			data.append({
			  'imagen':property_tenant.image,#imagen
			  'estado':self.get_dicc_status(property_tenant.state,property_tenant),#estado
			  'propiedad':property_tenant.name,#propiedad
			  'propiedad_id':property_tenant.id,#propiedad_id,
			  'use_property':use_property,
			  'general_pediente':data_data,
			  'metricas':metricas,
			})
       
		result={
		'data':data,
		'renta_global_cobrados':renta_global_total_cobrados,
		'rentas_globla_pendientes':rentas_globla_total_pendientes,
		'ingreso_cobrado':ingreso_propiedad_cobrados,
	    'etiqueta':etiqueta,
	    'total_mantenimiento':full_total_mente,
	    'total_servicios':full_total_ser,
	    'total_neto':full_neto_total,
	 	}
		return result

	@http.route(['/my_properties'], type='http', auth="user", website=True)
	def my_properties_http(self, **post):
		vals = {}
		return request.render("website_custom_property.my_properties_onload", {})


	def get_value_selection(self,value,field):
		"""
		funcion para tomar el label del campo select en ves de su llave
		de los alertas
		"""
		value_result=''
		kay_val_dict = dict(field._fields['actividad'].selection)
		for key, val in kay_val_dict.items():
			if key==value:
				value_result=val
		return value_result



	@http.route(['/clock_alert'], type='http', auth="user", website=True)
	def clock_alert_http(self, **kw):	
		"""
		Carga el contenido de la alerta para mostrarla en la tabla
		"""
		vals={}		
		alertadeusuario=request.env['alert.clock'].sudo().search(
			[('duenos_id','=',self.get_user_login())])
		data_html=[]
		for item in alertadeusuario:
			data_html.append([self.get_value_selection(item.actividad,item),
			item.propiedad_id.name,item.contratos_id.name,
			self.get_correct_date_show(item.create_date),item.contratos_id.id,
			item.marcarleido,item.id,item])
		vals.update({
		 'alerta':data_html,		
		})
		return request.render("website_custom_property.alert_clock",vals)


	@http.route(['/clock_alert_count'], type='json', auth="user", website=True)
	def clock_alert_count(self,**kw):	
		"""
		Cuenta la cantidad de alerta o actividedes por usuario
		"""
		alert_count=request.env['alert.clock'].sudo().search_count(
			[('duenos_id','=',self.get_user_login()),('marcarleido','=',False)])
		result={
			'count_alert':alert_count
		}
		return result


	def get_correct_date(self,fecha):
		"""
		Convertir la fecha que esta guarda en la base de datos a una que sea
		totalmente funcional para el website
		"""		
		user_tz = request.env.user.tz or pytz.utc
		local = pytz.timezone(user_tz)
		fecha_real=datetime.strftime(pytz.utc.localize
			(datetime.strptime(fecha.strftime("%Y-%m-%d %H:%M:%S"), DEFAULT_SERVER_DATETIME_FORMAT)).
			astimezone(local),"%Y-%m-%dT%H:%M:%S")
		return fecha_real
		
		

	def get_correct_date_show(self,fecha):
		"""
		Convertir la fecha que esta guarda en la base de datos a una que sea
		totalmente funcional para el website
		"""
		user_tz = request.env.user.tz or pytz.utc
		local = pytz.timezone(user_tz)
		fecha_real=datetime.strftime(pytz.utc.localize
			(datetime.strptime(fecha.strftime("%Y-%m-%d %H:%M:%S"), DEFAULT_SERVER_DATETIME_FORMAT)).
			astimezone(local),"%d-%m-%Y %H:%M:%S")
		return fecha_real

    #cargar datos para el mini calendario
	@http.route('/minicalendario',type='json',website=True,auth='user')
	def calenary_event_mini(self,**kw):
		eventos=[]
		user_id=request.env['res.users'].sudo().search(
			[('id','=',http.request.env.context.get('uid'))]).partner_id.id
		propiedad_eval=kw.get('propiedad')
		if propiedad_eval==int(-1):
			datos_calendario=request.env['calendar.event'].sudo().search(
			[('partner_ids','in',user_id)])
		else:
			datos_calendario=request.env['calendar.event'].sudo().search(
			[('partner_ids','in',user_id),('property_calendary','=',int(propiedad_eval))])			

		for evento in datos_calendario:
			inicio=evento.start
			fin=evento.stop
			color=self.color_hex_mini()
			for item in range(0,int(evento.duration/24)+1):		
				fecha=datetime(inicio.year,inicio.month,inicio.day).strftime("%B/%d/%Y")
				eventos.append({
					    'title': evento.property_calendary.name+"\n"+evento.property_tanency.name,
			            'date': fecha, 
		            	'link': "/propiedades/calendario"		 		                
                   })

				inicio=inicio+timedelta(days=1)
		result ={
		 'eventos':eventos
		}
		return result

	def color_hex_mini(self):
		color=['#C70039','#FFC300','#1608E4','#DC0AF5','#910AF5','#F5750A','#3B4F1F'
		,'#4A0527','#716C2A','#021005','#AE3F5A']
		index=random.randint(0,10)
		return color[index]

	def color_hex(self):
		color=['#b2e2f2','#c5c6c8','#ffda9e','#fdf9c4','#b0c2f2','#fcb7af','#d8f8e1'
		,'#84b6f4','#fdfd96','#77dd77','#ff6961']
		index=random.randint(0,10)
		return color[index]

	#cargar datos para el calendario
	@http.route('/calendario/eventos',type='http',website=True,auth='user')
	def calendary_event_http(self,**kw):
		locale.setlocale(locale.LC_ALL, '')
		user_id=request.env['res.users'].sudo().search(
			[('id','=',http.request.env.context.get('uid'))]).partner_id.id
		datos_calendario=request.env['calendar.event'].sudo().search(
			[('partner_ids','in',user_id)])
		eventos=[]	
		for evento in datos_calendario:
			inv_ref=request.env['account.analytic.account'].sudo().search(
				[('id','=',evento.property_tanency.id)])
			total_rent_recibido=0.0
			total_rent_pend=0.0
			for inv_ref in inv_ref.rent_schedule_ids:
				pagos=request.env['account.payment'].sudo().search([
					('communication','=',inv_ref.invc_id.name),('payment_date','>=',evento.start),
					('payment_date','<=',evento.stop),('tipo_de_pago','=','r')])
				for item_pago in pagos:
					total_rent_recibido=+item_pago.amount					
			total_rent_pend+=inv_ref.invc_id.amount_residual

			
			eventos.append({
				'id':evento.id,
				'title':evento.name,
				'start':self.get_correct_date(evento.start),
				'end':self.get_correct_date(evento.stop),
				'textColor':"#000000",
				'color':self.color_hex(),
                'descripcion':evento.description,
                'usuario':user_id,
                'contract_id':evento.property_tanency.id,
                'propiedad':evento.property_calendary.name,  
                'idpropieda':evento.property_calendary.id,
                'programado':str(locale.currency(total_rent_pend,grouping=True)),
                'recibido':str(locale.currency(total_rent_recibido,grouping=True)),
                'programado_op':total_rent_pend,
                'recibido_op':total_rent_recibido,
              	})
		#	raise UserError(str(eventos))
		return Response(json.dumps(eventos), 
		content_type='application/json;charset=utf-8',status=200)

	@http.route(['/propiedades/calendario'], type='http', auth="user", website=True)
	def property_calendary_http(self, **kw):		
		return request.render("website_custom_property.propretary_calendary_show_data", {})

	@http.route(['/alert/check'], type='json', auth="user", website=True)
	def alert_marck_http(self, **kw):
		"""
		Marcar como leida la alerta
		"""
		request.env['alert.clock'].search([('id','=',kw.get('dicontrato'))]).update({
			'marcarleido':True
			})

	@http.route(['/load/property/calendary'], type='json', auth="user", website=True)
	def property_calendary_load(self,**kw):
		"""
         Cargar la lista de propiedad para cargarlas en el calendario  
		"""
		propiedad=request.env['account.asset.asset'].sudo().search([('property_owner','=',self.get_user_login())])
		html=''
		for item in propiedad:
			html+="<div class='form-check'>"
			html+="<input type='checkbox' name="+str(item.name)+" class='form-check-input item_check' id="+str(item.id)+" value="+str(item.name)+" />"
			html+="<label class='form-check-label' for="+str(item.id)+">"+str(item.name)+"</label>"			
			html+="</div>"

		result={
		 'load':html
		}

		return result

	@http.route(['/load/property/dashbord'], type='json', auth="user", website=True)
	def property_calendary_mini(self,**kw):
		"""
          Cargar la lista de propiedad para filtar por propiedad
		"""
		propiedad=request.env['account.asset.asset'].sudo().search([('property_owner','=',self.get_user_login())])
		html='<select class="form-control">'
		for item in propiedad:
			html+="<option id="+str(item.id)+">"+str(item.name)+"</option>"
		html+="<option selected id='-1'>Todas</option>"
		html+="<select>"

		result={
		 'load':html
		}

		return result











		



