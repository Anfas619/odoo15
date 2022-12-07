{
    'name': 'Due Limit',
    'version': '15.01.0.0',
    'description': "For adding a limit to POS orders for Customers",
    'depends': [
        'base', 'point_of_sale', 'pos_sale',
    ],

    'assets': {
        'point_of_sale.assets': [
            '/due_limit/static/src/js/due_limit.js',

        ],
    },

    'data': [
        'views/due_limit.xml'

    ],

    'application': True,

}
