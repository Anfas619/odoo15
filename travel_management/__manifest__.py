{
    'name': 'Travel Management',
    'version': '1.2',
    'category': 'Sales/Travel',
    'description': "For Customers Easy to Book Travel",
    'depends': [
        'base', 'account'
    ],
    'assets': {
        'web.assets_backend': [
            'travel_management/static/src/js/action_manager.js']
    },
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/travel_management.xml',
        'views/source_location.xml',
        'views/service_type.xml',
        'views/vehicle.xml',
        'views/facilities.xml',
        'views/tour_package.xml',
        'wizard/travel_wizard.xml',
        'report/travel_management_template.xml',
        'report/travel_management_report.xml',




    ],

    'application': True,

}
