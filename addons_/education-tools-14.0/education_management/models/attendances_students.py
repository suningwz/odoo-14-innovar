from odoo import models, fields, api

class AttendancesStudentes (models.Model):
    _name = "em.attendances.students"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_record'
    _order = "id DESC"

    name_record = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", readonly=True, required=True, copy=False, default=lambda self:
    self.env['ir.sequence'].next_by_code('em.attendances.students'))
    employee_id = fields.Many2one('em.employees', 'Attendant', required=True)
    batch_id = fields.Many2one('em.batch', 'Batch', required=True, tracking=True)
    active = fields.Boolean(default=True)