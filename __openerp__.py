# -*- coding: utf-8 -*-
{
    'name': 'Gestusa3',
    'version': '1.0',
    'category': 'InfoSaône',
    'description': """
Gestusa3
""",
    'author': 'Tony GALMICHE',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': [
    ],
    'data': [
        'security/gestusa3_security.xml',
        'security/gestusa3_access_data.xml',
        'security/res.groups.csv',
        'security/ir.model.access.csv',
        'g3_etablissement_view.xml',
        'g3_profil_metier_view.xml',
        'g3_usager_view.xml',
        'g3_dossier_usager_view.xml',
        'g3_config_champ_view.xml',
        'res_users_view.xml',
        'menu.xml',
        'gestusa3_data.xml',
        'assets.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

