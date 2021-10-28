from odoo import models, fields

class Teachers(models.Model):
    _name = "em.teachers"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'first_name_teacher'

    first_name_teacher = fields.Char(string="First Name Teacher", required=True)
    last_name_teacher = fields.Char(string="Last Name Teacher", required=True)
