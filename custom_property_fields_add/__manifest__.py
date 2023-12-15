{
    'name': 'Custom Property Field add',
    'version': '13.0.1.0.0',
    'category': 'Bienes Raíces',
    'summary': """
           Modifica formato de impresión de comprobante de recibo de depósito del inquilino
           Crea botón de envío a correo al comprobante de pago del depósito del inquilino
     """, 
    'author': 'OGUM',
    'license': 'LGPL-3',
    'website': 'https://intranet.ogum.com.mx/',
    'depends': [
       'property_management',
       'property_landlord_management',
       'om_account_asset',
       'calendar',
       'account'
    ],
    'data': [
      # 'security/ir.model.access.csv',
      'data/email_template.xml',
      'views/button_send_pay_view.xml',
      'views/property_invisible.xml',
      'report/report_deposit_custom.xml',
      'data/email_template.xml',
      
    ],
   
}
