{
    'name': 'Stock Report Email',
    'version': '15.01.0.0',
    'category': 'Inventory/Stock Report Email',
    'description': "For Inventory manager to receive emails of stock report ",
    'depends': [
        'base','mail','stock'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/stock_email.xml',
        'report/stock_email_report.xml',
        'report/stock_email_report_template.xml',


    ],

    'application': True,

}