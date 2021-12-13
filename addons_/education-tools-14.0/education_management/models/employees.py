from odoo import models, fields, api

class Employees(models.Model):
    _name = "em.employees"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_employee'

    name_employee = fields.Char(string="Name", required=True)
    phone_employee = fields.Char(string="Phone")
    work_position = fields.Selection([
        ('secre','Secretary'),
        ('secre_teach','Secretary/Teacher'),
        ('teach', 'Teacher'),
    ], string="Work Position", default='secre' ,required=True)