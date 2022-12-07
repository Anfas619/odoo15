{
    'name': 'Most View Sold Products',
    'version': '1.2',
    'category': 'Website/Most View Sold Products',
    'description': "Trending Products in Website",
    'depends': [
        'base', 'website_sale'
    ],
    'assets': {
        'web.assets_frontend': [
            '/most_product/static/src/js/dynamic.js',
        ],
    },
    'data': [
        'views/most_product.xml'

    ],


    'installable': True,
    'application': True

}