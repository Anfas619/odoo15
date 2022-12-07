{
    'name': 'HelpDesk',
    'version': '15.01.0.0',
    'category': 'Website/Helpdesk',
    'description': "For Client to book Tickets for HelpDesk module",
    'depends': [
        'base','website'
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/template.xml',
        'views/tickets.xml',
        'views/config.xml',





    ],

    'application': True,

}