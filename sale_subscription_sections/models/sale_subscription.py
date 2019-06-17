# Author: Iryna Vyshnevska
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class SaleSubscription(models.Model):

    _inherit = "sale.subscription"

    def _prepare_invoice_line(self, line, fiscal_position):
        """
        Override to add specific behavior if line just section line
        """
        if not line.display_type:
            inv = super()._prepare_invoice_line(line, fiscal_position)
            inv['sequence'] = line.sequence
            inv['display_type'] = line.display_type
            return inv
        else:
            # as sale_subscription expect product_id as required we should
            # handle preparing lines separately
            return {
                'name': line.name,
                'display_type': line.display_type,
                'sequence': line.sequence,
                'price_unit': 0.0,
            }

class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    sequence = fields.Integer(required=True, default=10)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False,
        help="Technical field for UX purpose.")
    product_id = fields.Many2one(required=False)
