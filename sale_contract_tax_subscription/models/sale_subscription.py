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
            tax = line.additional_tax_ids.filtered(lambda r: r.company_id == company)
            # if no applicable taxes leave in default state
            if tax:
                inv_line['invoice_line_tax_ids'] = [(6, 0, tax.ids)]

        return inv_line


class AccountAnalyticAccount(models.Model):
    _inherit = "sale.subscription.line"

    additional_tax_ids = fields.Many2many(
        string="Manual taxes",
        comodel_name="account.tax",
        help="Taxes to change default fiscal politics",
        domain="[('type_tax_use','=','sale')]"
    )
    applied_tax_desc = fields.Char(
        string="Applied taxes",
        help="Taxes which will be applied to current line",
        compute="_get_applied_taxes",
    )

    def _get_applied_taxes(self):
        """
        Compute names of applied tax to aware user which taxes would be applied
        to line in invoice, this data applicable only to the current moment
        here we don't care about future fiscal politics
        """

        contract = self[0].analytic_account_id
        fiscal_position = self.env['account.fiscal.position']\
            .get_fiscal_position(contract.partner_id.id)
        fiscal_position = self.env['account.fiscal.position']\
            .browse(fiscal_position)
        for rec in self:
            res = contract._prepare_invoice_line(rec, fiscal_position)
            if res['invoice_line_tax_ids'] and \
                    res['invoice_line_tax_ids'][0][2]:
                taxes = self.env['account.tax'].\
                    browse(res['invoice_line_tax_ids'][0][2])
                rec.applied_tax_desc = ', '.join(taxes.mapped('name'))
