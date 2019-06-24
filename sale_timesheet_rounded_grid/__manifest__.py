# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
{
    "name": "Sale Timesheet Rounded Grid",
    "summary": "Round timesheet entries from the grid view",
    "version": "12.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/camptocamp/odoo-enterprise-addons",
    "author": "Camptocamp",
    "license": "LGPL-3",
    "depends": [
        "sale_timesheet_rounded",
        "timesheet_grid",
    ],
    "data": [
        "views/account_analytic_line.xml",
    ],
    "installable": True,
    "auto-install": True,
}
