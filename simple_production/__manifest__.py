{
    'name': 'Simple Production',
    'version': '1.2',
    'category': 'Manufacturing/Simple',
    'description': "For BOM and Manufacturing",
    'depends': [
        'base', 'account','mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/bill_of_material.xml',
        'views/manufacturing_order.xml',

    ],
    'installable': True,
    'application': True
}
