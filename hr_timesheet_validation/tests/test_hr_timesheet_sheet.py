# Author: Iryna Vyshnevska
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo.tests.common import SavepointCase
from odoo.exceptions import UserError


class TestTimesheetSheet(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(
            cls.env.context,
            tracking_disable=True,
        ))
        cls.user = cls.env.ref('base.user_root')
        cls.employee = cls.env.ref('hr.employee_admin')
        cls.ts_model = cls.env['hr_timesheet.sheet']
        cls.project = cls.env.ref('project.project_project_1')
        cls.ts_1 = cls.ts_model.create({
            'user_id': cls.user.id,
            'employee_id': cls.employee.id,
            'date_start': '2019-02-25',
            'date_end': '2019-03-03',
        })
        cls.ts_2 = cls.ts_model.create({
            'user_id': cls.user.id,
            'employee_id': cls.employee.id,
            'date_start': '2019-03-04',
            'date_end': '2019-03-11',
        })
        cls.ts_3 = cls.ts_model.create({
            'user_id': cls.user.id,
            'employee_id': cls.employee.id,
            'date_start': '2019-03-25',
            'date_end': '2019-04-02',
        })

    @classmethod
    def create_lines(cls, ts):
        ts.write({
            'timesheet_ids': [
                (0, 0, {'name': 'test',
                        'unit_amount': 1.0,
                        'project_id': cls.project.id,
                        'user_id': cls.user.id,
                        'date': ts.date_start,
                        'employee_id': ts.employee_id.id,
                        }),
                (0, 0, {'name': 'test',
                        'unit_amount': 1.0,
                        'project_id': cls.project.id,
                        'user_id': cls.user.id,
                        'date': ts.date_end,
                        'employee_id': ts.employee_id.id,
                        }),
            ]
        })

    def full_confirm(self, ts):
        ts.action_timesheet_confirm()
        ts.action_timesheet_done()

    def test_ts_validation(self):
        self.create_lines(self.ts_1)
        self.create_lines(self.ts_2)
        self.assertEqual(self.employee.timesheet_validated, False)
        self.ts_2.action_timesheet_confirm()
        with self.assertRaises(UserError):
            self.ts_2.action_timesheet_done()
        self.full_confirm(self.ts_1)
        self.full_confirm(self.ts_2)
        with self.assertRaises(UserError):
            self.ts_1.action_timesheet_refuse()

    def test_line_validation(self):
        self.create_lines(self.ts_1)
        self.create_lines(self.ts_2)
        self.assertEqual(self.employee.timesheet_validated, False)
        self.full_confirm(self.ts_1)
        self.assertEqual(
            self.employee.timesheet_validated.strftime('%Y-%m-%d'),
            '2019-03-03'
        )
        self.full_confirm(self.ts_2)
        self.assertEqual(
            self.employee.timesheet_validated.strftime('%Y-%m-%d'),
            '2019-03-11'
        )
        self.ts_2.action_timesheet_refuse()
        self.assertEqual(
            self.employee.timesheet_validated.strftime('%Y-%m-%d'),
            '2019-03-03'
        )

    def test_timesheet_validation_wizard(self):
        self.create_lines(self.ts_1)
        self.create_lines(self.ts_2)
        self.create_lines(self.ts_3)
        self.ts_2.action_timesheet_confirm()
        self.assertEqual(self.ts_1.state, 'draft')
        timesheet_to_validate = \
            self.ts_1.timesheet_ids | self.ts_2.timesheet_ids
        validate_action = timesheet_to_validate.with_context(
            grid_anchor='2019-03-01',
            grid_range='month',
        ).action_validate_timesheet()
        wizard = self.env['timesheet.validation'].\
            browse(validate_action['res_id'])
        wizard.action_validate()
        self.assertEqual(self.ts_1.state, 'done')
        self.assertEqual(
            self.employee.timesheet_validated.strftime('%Y-%m-%d'),
            '2019-03-31'
        )
        # timesheet in between month are not validated yet even part of lines
        # was validated
        self.assertEqual(self.ts_3.state, 'draft')
        # can do it via standard approving
        self.full_confirm(self.ts_3)
        self.assertEqual(self.ts_3.state, 'done')
        self.assertEqual(
            self.employee.timesheet_validated.strftime('%Y-%m-%d'),
            '2019-04-02'
        )
