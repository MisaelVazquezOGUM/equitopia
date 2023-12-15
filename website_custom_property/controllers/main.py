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
		ingreso=[]
		egresos=[]	

		for item in range(1,meses):
			dias=calendar.monthrange(int(ano),int(item))
			diasuma=calendar.monthrange(int(ano),int(item+1))
			start+=timedelta(days=int(dias[1]))
			fin=date(start.year,start.month,diasuma[1])
			fechas_rangos.append([start,fin])
		for vfecha in fechas_rangos:
			total_ingreso=0.0
			total_egresos=0.0
			#cobrado.append(invoice.amount_residual)

			for inv in invoice:
				
				damain_ingreso=request.env['account.payment'].sudo().search([
					#('communication','=',inv.name),
					('payment_type','=','inbound'),
					('payment_date','>=',vfecha[0]),
					('payment_date','<=',vfecha[1])])

				damain_egreso=request.env['account.payment'].sudo().search([
					#('communication','=',inv.name),
					('payment_type','=','outbound'),
					('payment_date','>=',vfecha[0]),
					('payment_date','<=',vfecha[1])])



					#('tipo_de_pago','=','r')])
				total_ingreso+=sum(damain_ingreso.mapped('amount'))
				total_egresos+=sum(damain_egreso.mapped('amount'))

			ingreso.append(total_ingreso)
			egresos.append(total_egresos)
			
		return [ingreso,egresos]

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
		month_range=calendar.monthrange(int(ano),int(mes))
		
		start_filter=date(int(ano),int(mes),1)
		stop_filer= date(int(ano),int(mes),int(month_range[1]))

		#buscar propiedades del usuario
		tipo_busqueda=False
		rentas_historicas_cobradas=0.0
		rentas_historicas_ha_cobrar=0.0
		full_total_mente=0.0
		full_total_ser=0.0
		full_neto_total=0.0
		rentas_efectivas=0.0
		rentas_programadas=0.0
		if int(seleciona_propiedad)==-1:
			propidades=request.env['estado.result'].sudo().search([('owner_id','=',self.get_user_login()),
				('foreport','=',True),('mes_num','=',int(mes))])			
			tipo_busqueda=True
		else:
			propidades=request.env['estado.result'].sudo().search([
				('owner_id','=',self.get_user_login()),('property_id','=',int(seleciona_propiedad)),
				('foreport','=',True),('mes_num','=',int(mes))])
		
		
		rentas_historicas_cobradas+=sum(propidades.mapped('rent_cobradas'))
		rentas_historicas_ha_cobrar+=sum(propidades.mapped('rent_por_cobrar'))
		full_total_mente+=sum(propidades.mapped('mantenimientos'))
		full_total_ser+=sum(propidades.mapped('servicios'))
		full_neto_total+=sum(propidades.mapped('ingresos_netos'))
		rentas_efectivas+=sum(propidades.mapped('rent_efectivo'))
		rentas_programadas+=sum(propidades.mapped('rent_cronograma'))

		data=[]		
		propidades_estadisticas=[]	
		etiqueta=[]
		for property_tenant in propidades:
			metricas=[]
			metricas.append(property_tenant.ingresos_netos)
			metricas.append(property_tenant.mantenimientos)
			metricas.append(property_tenant.servicios)
			metricas.append(property_tenant.otros_gastos)
			metricas.append(property_tenant.comisiones)
			data.append({
			  'imagen':property_tenant.imagen or None,#imagen
			  'estado':property_tenant.estado,#self.get_dicc_status(property_tenant.estado,property_tenant),#estado
			  'propiedad':property_tenant.property_id.name,#propiedad
			  'propiedad_id':property_tenant.property_id.id,#propiedad_id,
			  'use_property':[property_tenant.dias_libres,property_tenant.dias_ocupados],
			  'general_pediente':[property_tenant.rent_efectivo,property_tenant.rent_cronograma],
			  'metricas':metricas,
			})
			invoice=request.env['account.move'].sudo().search([('property_id','=',property_tenant.property_id.id),
				('type','=','out_invoice')])
			propidades_estadisticas.append(self.data_month(ano,mes,invoice))
			etiqueta.append(property_tenant.property_id.name)

		result={
		'data':data,
		'propiedad_estadisticas':propidades_estadisticas,
		'etiqueta':etiqueta,
		'renta_global_cobrados':rentas_historicas_cobradas,
		'rentas_globla_pendientes':rentas_historicas_ha_cobrar,
		'total_mantenimiento':full_total_mente,
	    'total_servicios':full_total_ser,
	    'total_neto':full_neto_total,
	    'rentas_efectivas':rentas_efectivas,
	    'rentas_programadas':rentas_programadas,
		}
		return result 

       

	@http.route(['/my_properties'], type='http', auth="user", website=True)
	def my_properties_http(self, **post):
		contac_user=request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])
		if contac_user.partner_id.title.name == False or contac_user.partner_id.name == False:
			# raise UserError("El usuario no tiene un título o un nombre válido")
			name = ""
		else:
			name=contac_user.partner_id.title.name+": "+ contac_user.partner_id.name
		vals = {
          'name':name, 
		}
		return request.render("website_custom_property.my_properties_onload", vals)


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
				fecha=datetime(inicio.year,inicio.month,inicio.day)#.strftime("%B/%d/%Y")
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
			#buscar contrato relacionado con el calendario
			cont_ref=request.env['account.analytic.account'].sudo().search(
				[('id','=',evento.property_tanency.id)])
			total_rent_recibido=0.0
			total_rent_pend=0.0
		
			#crear fecha de inicio y fin de mes
			dia=calendar.monthrange(evento.start.year,evento.start.month)[1]
			inicio=evento.start.replace(day=1)#dias inicial del mes
			fin=evento.stop.replace(day=dia)#dia final del  mes


			for inv_ref in cont_ref.rent_schedule_ids:
				if inv_ref.invc_id.type=='out_invoice':
					total_rent_recibido=sum(request.env['account.payment'].sudo().search([
					('communication','=',inv_ref.invc_id.name),('payment_date','>=',inicio),
					('payment_date','<=',fin),('tipo_de_pago','=','r')]).mapped('amount'))					
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



	@http.route('/property/dashbord', methods=['POST', 'GET'], csrf=False, type='http', auth="user", website=True)
	def print_id(self, **kw):		
		property_id=request.env['estado.result'].sudo().search([('owner_id','=',self.get_user_login()),('foreport','=',True)])
		if property_id:
			pdf = request.env.ref('custom_property.report_estado_propiedad').sudo().render_qweb_pdf([property_id.id])[0]
			pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
		return request.make_response(pdf, headers=pdfhttpheaders)


	# @http.route('/loadata/propiedad',type='json',website=True,auth='user')
	# def print_data_propiedad_(self, **kw):
	# 	propiedades=kw.get('propiedades')
	# 	fecha=kw.get('fecha_ano_mes_cuerr')
	# 	split_fecha=fecha.split('/')

	# 	nom_numero=0

	# 	if (split_fecha[0]=='enero'):
	# 		nom_numero=1
	# 	if (split_fecha[0]=='febrero'):
	# 		nom_numero=2
	# 	if (split_fecha[0]=='marzo'):
	# 		nom_numero=3
	# 	if (split_fecha[0]=='abril'):
	# 		nom_numero=4
	# 	if (split_fecha[0]=='mayo'):
	# 		nom_numero=5
	# 	if (split_fecha[0]=='junio'):
	# 		nom_numero=6
	# 	if (split_fecha[0]=='julio'):
	# 		nom_numero=7
	# 	if (split_fecha[0]=='agosto'):
	# 		nom_numero=8
	# 	if (split_fecha[0]=='septiembre'):
	# 		nom_numero=9
	# 	if (split_fecha[0]=='octubre'):
	# 		nom_numero=10
	# 	if (split_fecha[0]=='noviembre'):
	# 		nom_numero=11
	# 	if (split_fecha[0]=='diciembre'):
	# 		nom_numero=12

	# 	fecha_start=date(int(split_fecha[1]),int(nom_numero),1)
	# 	days_max=calendar.monthrange(int(fecha_start.year),int(fecha_start.month))[1]
	# 	fecha_stop=date(int(split_fecha[1]),int(nom_numero),days_max)

	# 	cantidad_recibido=0.0


	# 	for pd in propiedades:
	# 		cantidad_recibido=sum(request.env['account.payment'].sudo().search([
	# 			('property_id','=',pd),('tipo_de_pago','=','r'),
	# 			('payment_date','>=',fecha_start),('payment_date','<=',fecha_stop)]).mapped('amount'))


	# 		cantidad_programada=request.env['account.move'].sudo().search([
	# 			('property_id','=',pd)]).mapped('amount_residual')

	# 	#	raise UserError(str(cantidad_recibido))


	# 	#raise UserError(fecha_filter)
		




	



	@http.route('/tenant_details',type='http',website=True,auth='user')
	def get_view_contrato(self,**kw):
		contrato=kw.get('contrato')
		alert=kw.get('link_alerta')
		if alert:
			request.env['alert.clock'].sudo().search([('id','=',alert)]).marcarleido=True

		data_contrato=request.env['account.analytic.account'].sudo().search([('id','=',contrato)])
		locale.setlocale(locale.LC_ALL, '')
		data_rent=[]
		for item in data_contrato.rent_schedule_ids:
			data_rent.append({
				'hecho_pago':item.hecho_pago,
				'start_date':item.start_date.strftime('%m/%d/%Y'),
				'amount':str(locale.currency(item.amount,grouping=True)),
				'pen_amt':str(locale.currency(item.pen_amt,grouping=True)),
				'cheque_detail':item.cheque_detail,
				'inv':item.invc_id.name,
				'note':item.note
				})
	
		data_mente=[]
		for item in data_contrato.maintenance_per_property:
			data_mente.append({
				'name':item.name.name,
				'tems':item.team.name,
				'frequency':item.frequency,
				'cost':str(locale.currency(item.cost,grouping=True)),
				})

		tipo=data_contrato.tipo_tarifa
		tipo_tarifa_des=''	
		if tipo=='1':
			tipo_tarifa_des='Tarifa Normal'
		if tipo=='2':
			tipo_tarifa_des='Tarifa Alta'
		if tipo=='3':
			tipo_tarifa_des='Tarifa Baja'

		frecuencia=data_contrato.frequency
		frecuencia_des=''

		if frecuencia=='Daily':
			frecuencia_des='Dia'
		if frecuencia=='Weekly':
			frecuencia_des='Semanal'
		if frecuencia=='Monthly':
			frecuencia_des='Mensual'
		if frecuencia=='Semestral':
			frecuencia_des='Semestral'
		if frecuencia=='Yearly':
			frecuencia_des='Año'




		data={
		'name':data_contrato.name,
		'code':data_contrato.code,
		'propiedad':data_contrato.property_id.name,
		'manejando':data_contrato.manager_id.name,
		'moneda':data_contrato.currency_id.name,
		'inquilino':data_contrato.tenant_id.name,
		'compania':data_contrato.company_id.name,
		'deposito':str(locale.currency(data_contrato.deposit,grouping=True)),
		'despo_recivido':data_contrato.deposit_received,
		'contacto':data_contrato.contact_id.name,
		'fecha':data_contrato.ten_date.strftime('%m/%d/%Y %H:%M:%S'),
		'despo_regreso':str(locale.currency(data_contrato.amount_return,grouping=True)),
		'desp_cantregreso':data_contrato.deposit_return,
		'tipotarifa':tipo_tarifa_des,
		'hora_entrada':data_contrato.hora_entrada,
		'hora_salida':data_contrato.hora_salida,
		'check_in':data_contrato.chech_in.strftime('%m/%d/%Y %H:%M:%S'),
		'banedera_in_real':data_contrato.bandera_in_realizado,
		'usuario_accesos':data_contrato.entrega_acceso_id.name,
		'email':data_contrato.email,
		'telefono':data_contrato.telefono,
		'chech_out':data_contrato.chech_out.strftime('%m/%d/%Y %H:%M:%S'),
		'banedera_out_real':data_contrato.bandera_out_realizado,
		'sugerencia':data_contrato.suggested_month,
		'frecuencia':frecuencia_des,
		'totalrenta':str(locale.currency(data_contrato.total_rent,grouping=True)),
		'rent_schedule':data_rent,
		'mantenimientos':data_mente,
		}

		return request.render("website_custom_property.contractos_view_data", data)
		














		



