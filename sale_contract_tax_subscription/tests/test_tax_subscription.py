# -*- coding: utf-8 -*-
# Author: Iryna Vyshnevska
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.tests.common as common

from odoo.addons.sale_contract.tests.common_sale_contract import \
    TestContractCommon


class TestTaxSubscription(TestContractCommon):

    def setUp(self):
        super(TestTaxSubscription, self).setUp()

        self.env = self.env(context=dict(self.env.context,
                                         tracking_disable=True))
        line_model = self.env['sale.subscription.line']
        uom = self.env.ref('product.product_uom_hour')
        tax_15 = self.env.ref('sale_contract_tax_subscription.sale_tax_15')
        tax_25 = self.env.ref('sale_contract_tax_subscription.sale_tax_25')
        product_1 = self.env.ref('product.product_product_1')
        product_2 = self.env.ref('product.product_product_2')
        product_2.write({'taxes_id': [(6, 0, [tax_15.id])]})

        line_model.create({
            'name': 'Subscription',
            'product_id': product_1.id,
            'uom_id': uom.id,
            'price_unit': 100,
            'analytic_account_id': self.contract.id,
        })

        line_model.create({
            'name': 'Subscription',
            'product_id': product_1.id,
            'uom_id': uom.id,
            'price_unit': 200,
            'additional_tax_ids': [(6, 0, [
                tax_15.id, tax_25.id
            ])],
            'analytic_account_id': self.contract.id,
        })

        line_model.create({
            'name': 'Subscription',
            'product_id': product_2.id,
            'uom_id': uom.id,
            'price_unit': 300,
            'analytic_account_id': self.contract.id,
        })


    def test_tax_applying(self):

        inv_id = self.contract.recurring_invoice()['domain'][0][2]
        invoice = self.env['account.invoice'].browse(inv_id)
        tax = self.env.ref('sale_contract_tax_subscription.sale_tax_15')
        inv_lines = invoice.invoice_line_ids

        self.assertEqual(invoice.amount_total, 675)
        self.assertEqual(invoice.amount_tax, 75)
        self.assertFalse(inv_lines[0]['invoice_line_tax_ids'])
        # only one tax applied, other belong to other company should be cut
        self.assertEqual(inv_lines[1]['invoice_line_tax_ids'].id, tax.id)
        # tax applied from product settings
        self.assertEqual(inv_lines[2]['invoice_line_tax_ids'].id, tax.id)
