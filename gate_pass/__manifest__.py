{
    'name': 'Gate Pass Management',
    'version': '18.0.1.0.29',
    'category': 'Operations',
    'summary': 'Material, visitor and vehicle gate pass management with approval workflow',
    'description': """
Gate Pass Management
====================

Manage material movements, visitor access, and vehicle entries/exits with
approval workflows, role-based security, PDF reports, and multi-company support.

Features
--------
* Material gate pass with item lines and manager approval
* Visitor check-in / check-out with duration tracking
* Vehicle gate pass with driver and cargo details
* Professional PDF reports
* Mail chatter and activity tracking
    """,
    'author': 'Prissol Private Limited',
    'website': 'https://prissol.com',
    'support': 'hello@prissol.com',
    'depends': [
        'base',
        'web',
        'mail',
        'hr',
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'data/sequence_data.xml',
        'reports/material_pass_report.xml',
        'reports/visitor_pass_report.xml',
        'reports/vehicle_pass_report.xml',
        'views/material_pass_views.xml',
        'views/visitor_pass_views.xml',
        'views/vehicle_pass_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gate_pass/static/src/css/gate_pass.css',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'price': 25.00,
    'currency': 'USD',
}
