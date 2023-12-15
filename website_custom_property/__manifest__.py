{
    'name': 'Website Custom dashboard Property',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'summary': """
            custom dashboard property:
            
     """,
    'author': '',
    'license': 'LGPL-3',
    'website': '',
    'depends': [
       'website',
       'property_management',
       'property_landlord_management',
       'om_account_asset',
       'custom_property'
    ],
    'data': [
       'security/ir.model.access.csv',
       'security/property_security.xml',
       'views/website_template.xml', 
       'views/website_dashboard.xml',
       #'views/my_property.xml',
       'views/propietario_calendario.xml',
       'views/Website_alert_clock.xml',
       'views/view_contrato.xml',
       'views/alert_clock.xml',
     
       
    ],
   
}
