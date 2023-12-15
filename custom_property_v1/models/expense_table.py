from odoo import api,models,fields,_
from odoo.exceptions import UserError,ValidationError
from datetime import date,datetime
import calendar
import logging
_logger = logging.getLogger(__name__)

moves = [
    ('m','Maintenance'),
    ('r','Rent'),
    ('s','Services'),
    ('oe','Other Expense'),
    ('co','Commission'),
]

class ExpenseTable(models.Model):

    _name = 'expense.table'
    _description = 'Expense Table'

    state_result_id = fields.Many2one(comodel_name='estado.result',string='State Result')
    date_exp = fields.Date(string='Date')
    name_exp = fields.Char(string='Name')
    type_move = fields.Selection(moves,string='Movement Type')
    enter_pay = fields.Float(string='Income')
    exit_pay = fields.Float(string='Discharge')
    invoice_id = fields.Many2one(comodel_name='account.move')

    def go_create(self,prop_id,stat_id):
        self.get_records(stat_id,prop_id)
    
    def go_update(self,prop_id,stat_id):
        self.delete_all(stat_id)

    '''
        Metodo para eliminar los registros de la tabla, esto para el momento en que se elimina un estado de cuenta
        elimine tambien los datos y no dejar basura
    '''
    def delete_all(self,stat_id):
        records = self.env['expense.table'].search([('state_result_id','=',stat_id)])
        for rec in records:
            rec.unlink()

    '''Metodo para obtener los registros de los gastos
        obtiene las rentas,los gastos de servicios, los gastos de mantenimiento, y las comisiones facturadas
    '''
    def get_records(self,state_result_id,prop_id):
        vals_ot_exp = {}
        exp = []
        fecha_actual=datetime.now()
        days_max=calendar.monthrange(int(fecha_actual.year),int(fecha_actual.month))
        date_start=date(int(fecha_actual.year),int(fecha_actual.month),1)
        date_stop=date(int(fecha_actual.year),int(fecha_actual.month),int(days_max[1]))

        table_exist = self.env['expense.table'].search([('state_result_id','=',state_result_id)])
        #Rentas
        rent_efectivo_ten = self.env['tenancy.rent.schedule'].search([
				('paid','=',True),
				('move_check','=',True),
				('property_id','=',prop_id),
				('start_date','>=',date_start),
				('start_date','<=',date_stop)])
        
        
        ids_rent = [x.invc_id.id for x in rent_efectivo_ten]
        _logger.info(f'*******ids_rent: {ids_rent}')
        
        rents_pay = self.env['account.payment'].search([('property_id','=',prop_id),('tipo_de_pago','=','r'),
					('payment_date','>=',date_start),('payment_date','<=',date_stop),('invoice_ids','in',ids_rent)])
        _logger.info(f'***********rents_pay: {rents_pay}')

        if rents_pay:
            for rent in rents_pay:
                vals_ot_exp = {
                    'state_result_id':state_result_id,
                    'date_exp':rent.payment_date,
                    'name_exp':rent.display_name,
                    'type_move':'r', 
                    'enter_pay':float(rent.amount),
                    'exit_pay':0.0,
                    'invoice_id':rent.invoice_ids[0].id
                }
                exp.append(vals_ot_exp)
        
        #Servicios
        servicios=self.env['account.payment'].search([('property_id','=',prop_id),('tipo_de_pago','=','s'),
					('payment_date','>=',date_start),('payment_date','<=',date_stop)])
        
        if servicios:
            for serv in servicios:
                vals_ot_exp = {
                    'state_result_id':state_result_id,
                    'date_exp':serv.payment_date,
                    'name_exp':serv.display_name,
                    'type_move':'s', 
                    'enter_pay':0.0,
                    'exit_pay':float(serv.amount),
                    'invoice_id':serv.invoice_ids[0].id
                }
                exp.append(vals_ot_exp)

        #Mantenimientos
        mantenimientos=self.env['account.payment'].search([('property_id','=',prop_id),('tipo_de_pago','=','m')])

        if mantenimientos:
            for mant in mantenimientos:
                vals_ot_exp = {
                    'state_result_id':state_result_id,
                    'date_exp':mant.payment_date,
                    'name_exp':mant.display_name,
                    'type_move':'m', 
                    'enter_pay':0.0,
                    'exit_pay':float(mant.amount),
                    'invoice_id':mant.invoice_ids[0].id
                }
                exp.append(vals_ot_exp)

        otros_gastos=self.env['account.payment'].search([('property_id','=',prop_id),('tipo_de_pago','=','o'),
			  	('payment_date','>=',date_start),('payment_date','<=',date_stop)])
        
        if otros_gastos:
            for ot_exp in otros_gastos:
                vals_ot_exp = {
                    'state_result_id':state_result_id,
                    'date_exp':ot_exp.payment_date,
                    'name_exp':ot_exp.display_name,
                    'type_move':'oe', 
                    'enter_pay':0.0,
                    'exit_pay':float(ot_exp.amount),
                    'invoice_id':ot_exp.invoice_ids[0].id
                }
                exp.append(vals_ot_exp)
        
        #comsiones
        comisiones=self.env['account.payment'].search([('property_id','=',prop_id),('tipo_de_pago','=','c'),
			  	('payment_date','>=',date_start),('payment_date','<=',date_stop)])
        
        if comisiones:
            for comm in comisiones:
                vals_ot_exp = {
                    'state_result_id':state_result_id,
                    'date_exp':comm.payment_date,
                    'name_exp':comm.display_name,
                    'type_move':'co', 
                    'enter_pay':0.0,
                    'exit_pay':float(comm.amount),
                    'invoice_id':comm.invoice_ids[0].id
                }
                exp.append(vals_ot_exp)
        
        self.env['expense.table'].create(exp)
