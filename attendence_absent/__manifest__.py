{
    'name': 'Absentees',
    'version': '1.2',
    'category': 'Attendances/Absentees',
    'description': "Absent Report",
    'depends': [
        'base', 'hr', 'hr_attendance'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/absent.xml',


    ],

    'installable': True,
    'application': True

}