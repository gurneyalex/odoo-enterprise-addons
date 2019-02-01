# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Sale Contract Tax Management',
    'description': 'Allow taxes mngm directly in sale contract',
    'author': 'camptocamp',
    'website': 'https://camptocamp.com',
    'license': 'LGPL-3.0',
    'depends': [
        'sale_contract',
    ],
    'data': [
        'views/sale_subscription.xml',
    ],
    'demo': [
        'data/tax.xml',
    ],
    'application': False,
}
