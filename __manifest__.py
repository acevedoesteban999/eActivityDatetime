# -*- coding: utf-8 -*-
{
    'name': 'Activity DateTime',
    'version': '19.1.1',
    'summary': """ Activity DateTime """,
    'author': 'acevedoesteban999@gmail.com , esteban.acevedo@qa-bit.com',
    'website': 'https://acevedoesteban999/eActivityDatetime',
    'category': '',
    'depends': ['base', 'mail','web'],
    'data': [
        "wizard/mail_activity_schedule.xml",  
        "views/mail_activity.xml",
    ],
    'assets':{
        'web.assets_backend':[
            'activity_datetime/static/src/core/web/*',
        ],
    },
    
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
