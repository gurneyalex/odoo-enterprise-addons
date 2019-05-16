# Author: Iryna Vyshnevska
# Copyright 2019 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class Sheet(models.Model):
    _inherit = 'hr_timesheet.sheet'

    @api.multi
    def action_timesheet_done(self):
        timesheets = self.env['hr_timesheet.sheet']
        for rec in self:
            timesheets |= self.search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', 'in', ['new', 'draft']),
                ('date_end', '<=', rec.date_start)
            ])
        if timesheets:
            raise UserError(
                _('Employees {} have opened timesheets for previous period '
                  'you should validate them first'
                  ).format(timesheets.mapped('employee_id.name'))
            )
        res = super().action_timesheet_done()
        for rec in self:
            # each timesheet has own date end
            rec.employee_id.write({'timesheet_validated': rec.date_end})
        return res

    @api.multi
    def action_timesheet_draft(self):

        timesheets = self.env['hr_timesheet.sheet']
        for rec in self:
            timesheets |= self.search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', 'in', ['done']),
                ('date_start', '>=', rec.date_end)
            ])
            if timesheets:
                raise UserError(
                    _('Employees {} have approved timesheets for later period '
                      'you should unvalidate them first').
                      format(timesheets.mapped('employee_id.name'))
                )

        res = super().action_timesheet_draft()
        for rec in self:
            date = self.search([
                ('date_end', '<', rec.date_start),
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'done'),
            ], order='date_end desc', limit=1).date_end
            if rec.employee_id.timesheet_validated != date:
                rec.employee_id.write({'timesheet_validated': date})
        return res
