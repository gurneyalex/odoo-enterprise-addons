# Author: Iryna Vyshnevska
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields

# In the module, we want to:
#
# add the display_type field on sale subscription lines with the same definition
# as the same field on sale order lines
# change the method of sale.order which are responsible for the creation of the
# creation of the subscription lines:
# the lines with a display_type of "note" or "section" must be included too (not
# only the lines with a subscription product)
# however empty sections must be skipped (if you find two consecutive
# "sections", without a product line in between the first one
# must be removed. Same if the last section has no products: remove it)
# the display_type of the line must be passed to the newly created subscription
# line change the way invoices are generated from a subscription:
# in the _prepare_invoice_line method of the subscription, pass the value of
# the display_type of the subscription line
# in the form view of the contract, just display the display_type field
# of the lines in a new column of the tree view (1st column).


class SaleSubscription(models.Model):

    _inherit = "sale.subscription"

    display_type = fields.Boolean(
        string="",
        help="Copy sections definition to new invoice"
    )

    # on creating invoice copy note
    # on creating lines pass by sections

    def _prepare_invoice_line(self, line, fiscal_position):
        inv_line = super()._prepare_invoice_line(line, fiscal_position)
        print(line)
        inv_line.update(
            {'sequence': line.sequence,
             'display_type': line.display_type,
             }
        )
        return inv_line


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"
    _order = 'analytic_account_id, sequence, id'

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    sequence = fields.Integer()
    product_id = fields.Many2one(required=False)




# sale.layout_category
