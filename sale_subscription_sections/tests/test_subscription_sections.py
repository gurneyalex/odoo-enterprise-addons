# -*- coding: utf-8 -*-
from odoo.addons.sale_subscription.tests.common_sale_subscription import TestSubscriptionCommon
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestSubscriptionSections(TestSubscriptionCommon):

    def setUp(self):
        super().setUp()
        self.env = self.env(context=dict(self.env.context, tracking_disable=True))

    def test_sale_order(self):

        subscription = self.subscription
        subscription.write({
            'recurring_invoice_line_ids': [
                (0, 0, {'name': self.product.name,
                        'product_id': self.product.id,
                        'product_uom_qty': 1.0,
                        'product_uom': self.product.uom_id.id,
                        'price_unit': self.product.list_price,
                        'sequence': 1,
                        }),
                (0, 0, {'name': 'Subscription',
                        'display_type': 'line_section',
                        'sequence': 2,
                        'price_unit': 0,
                        }),
                (0, 0, {'name': self.product3.name,
                        'product_id': self.product.id,
                        'product_uom_qty': 1.0,
                        'product_uom': self.product.uom_id.id,
                        'price_unit': self.product.list_price,
                        'sequence': 3,
                        }),
                (0, 0, {'name': 'Note',
                        'display_type': 'line_note',
                        'sequence': 5,
                        'price_unit': 0,
                        }),
                (0, 0, {'name': self.product2.name,
                        'product_id': self.product.id,
                        'product_uom_qty': 1.0,
                        'product_uom': self.product.uom_id.id,
                        'price_unit': self.product.list_price,
                        }),
            ],
        })
        subscription.recurring_invoice()
        invoice = self.env['account.invoice'].search([
            ('invoice_line_ids.subscription_id', '=', subscription.id)
        ])
        expected_res = [
            (1, 'TestProduct'),
            (2, 'Subscription'),
            (3, 'TestProduct3'),
            (5, 'Note'),
            (10, 'TestProduct2'),
        ]

        res = invoice.invoice_line_ids.mapped(lambda x: (x.sequence, x.name))
        self.assertEqual(res, expected_res)
