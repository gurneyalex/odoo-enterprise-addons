# -*- coding: utf-8 -*-
# Author: Iryna Vyshnevska
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class SaleSubscription(models.Model):

    _inherit = "sale.subscription"

    def _prepare_invoice_line(self, line, fiscal_position):

        inv_line = super(SaleSubscription, self). \
            _prepare_invoice_line(line, fiscal_position)

        if line.additional_tax_ids:
            if 'force_company' in self.env.context:
                company = self.env['res.company'].browse(
                    self.env.context['force_company'])
            else:
                company = line.analytic_account_id.company_id
                line = line.with_context(force_company=company.id,
                                         company_id=company.id)
            tax = line.tax_ids.filtered(lambda r: r.company_id == company)
            # if no applicable taxes leave in default state
            if tax:
                inv_line['invoice_line_tax_ids'] = [(6, 0, tax.ids)]

        return inv_line


class AccountAnalyticAccount(models.Model):
    _inherit = "sale.subscription.line"

    additional_tax_ids = fields.Many2many(
        string="Tax",
        comodel_name="account.tax",
        help="This taxes will apply to line on next invoice, if empty use "
             "standard settings",
        domain="[('type_tax_use','!=','purchase')]"
    )
