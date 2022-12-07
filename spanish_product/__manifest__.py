{
    'name': 'Spanish Name',
    'version': '15.01.0.0',
    'description': "For adding a new field spanish name of product",
    'depends': [
        'base', 'point_of_sale', 'sale_management'
    ],
    'assets': {
        'web.assets_qweb': [
            '/spanish_product/static/src/xml/spanish.xml',
            '/spanish_product/static/src/xml/pos_spanish_view.xml',
            '/spanish_product/static/src/xml/pos_spanish_order.xml',
        ],
        'web.assets_backend': [
            '/spanish_product/static/src/js/spanish.js',
            '/spanish_product/static/src/js/pos_spanish_view.js',
            '/spanish_product/static/src/js/pos_spanish_order.js',
        ],
    },

    'data': [
        'views/spanish_product.xml'

    ],

    'application': True,

}
