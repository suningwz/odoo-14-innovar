from odoo import models, fields

class Classrooms(models.Model):
    _name = "em.classrooms"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_classroom'

    name_classroom = fields.Char(string="Name Classroom", required=True)
    active = fields.Boolean(string="Active", default=True)
