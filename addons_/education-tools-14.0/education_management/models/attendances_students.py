from odoo import models, fields, api

class AttendancesStudentes (models.Model):
    _name = "em.attendances.students"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_record'
    _order = "id DESC"

    name_record = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    employee_id = fields.Many2one('em.employees', 'Attendant', required=True)
    batch_id = fields.Many2one('em.batch', 'Batch', required=True, tracking=True)
    active = fields.Boolean(default=True)