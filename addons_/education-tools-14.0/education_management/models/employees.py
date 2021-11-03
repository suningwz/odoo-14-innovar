from odoo import models, fields, api

class Employees(models.Model):
    _name = "em.employees"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_employee'

    name_employee = fields.Char(string="Name", required=True)
    surname_employee = fields.Char(string="Surname", required=True)
    phone_employee = fields.Char(string="Phone")
    work_position = fields.Char(string="Work Position", required=True)