# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo import models, api


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    @api.multi
    def adjust_grid(self, row_domain, column_field, column_value, cell_field,
                    change):
        self = self.with_context(force_compute=True)
        return super().adjust_grid(
            row_domain, column_field, column_value, cell_field, change
        )
