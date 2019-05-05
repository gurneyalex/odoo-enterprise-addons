# Author: Iryna Vyshnevska
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ValidationWizard(models.TransientModel):
    _inherit = 'timesheet.validation'

    def action_validate(self):
        # validate all ts till validation date
        employees = self.validation_line_ids.filtered('validate')\
            .mapped('employee_id')
        timesheets = self.env['hr_timesheet.sheet'].search([
            ('employee_id', 'in', employees.ids),
            ('state', 'in', ['new', 'draft']),
            ('date_end', '<=', fields.Date.to_string(self.validation_date)),
        ])
        timesheets.action_timesheet_confirm()
        timesheets.action_timesheet_done()

        employees.write({'timesheet_validated': self.validation_date})
        return {'type': 'ir.actions.act_window_close'}
