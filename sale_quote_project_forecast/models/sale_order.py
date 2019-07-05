# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api, _, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_sync(self):
        self.mapped('order_line').sudo().with_context(
            default_company_id=self.company_id.id,
            force_company=self.company_id.id,
        )._timesheet_service_generation()
        milestone_tasks = self.get_milestone_tasks()
        rate_order_lines = self.get_rate_tasks()
        for order_line in rate_order_lines:
            for task in milestone_tasks:
                employee = order_line.product_id.forecast_employee_id
                sen_level = order_line.product_id.seniority_level_id
                if not employee:
                    employee = self.env['hr.employee'].search(
                        [('seniority_level_id', '=', sen_level)], limit=1)
                if not employee:
                    raise UserError(
                        _("No Employee available for Seniority level \
                        {}").format(sen_level.name)
                    )
                self.env['project.forecast'].create({
                    'project_id': task.project_id.id,
                    'task_id': task.id,
                    'employee_id': employee.id
                })
            employee = order_line.product_id.forecast_employee_id
            project = self.mapped('tasks_ids.project_id')
            if len(project) == 1:
                self.env['project.sale.line.employee.map'].create({
                    'project_id': project.id,
                    'sale_line_id': order_line.id,
                    'employee_id': employee.id,
                })

    @api.multi
    def get_milestone_tasks(self):
        order_lines = self.order_line.filtered(
            lambda r: r.product_id.type == 'service' and
            r.product_id.service_policy == 'delivered_manual' and
            r.product_id.service_tracking == 'task_new_project'
        )
        return order_lines.mapped('task_id')

    @api.multi
    def get_rate_tasks(self):
        order_lines = self.order_line.filtered(
            lambda r: r.product_id.type == 'service' and
            r.product_id.service_policy == 'delivered_timesheet' and
            r.product_id.service_tracking in ('no', 'project_only')
        )
        return order_lines


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    service_policy = fields.Selection(
        'Service Policy',
        related='product_id.service_policy',
        readonly=True,
    )
