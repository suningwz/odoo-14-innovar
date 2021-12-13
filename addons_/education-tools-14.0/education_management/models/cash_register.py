from odoo import models, fields, api


class CashRegister(models.Model):
    _name = 'em.cash.register'
    _rec_name = 'cash_register_sequence'

    cash_register_sequence = fields.Char(string="Cash Register", readonly=True, required=True, copy=False,
                                         default=lambda self: self.env['ir.sequence'].next_by_code('em.cash.register'))
    opening_date_and_time = fields.Datetime(string="Opening Date And Time")
    closing_date_and_time = fields.Datetime(string="Closing Date And Time")
    total_amount = fields.Float(string="Total Amount")
    employee_id = fields.Many2one('em.employees', "Employee", required=True)
    payments_lines = fields.One2many('em.payments.students.line', 'cash_register_id',
                                     'Payments Lines',
                                     readonly=True)
    active = fields.Boolean(string="Is Active", required=True, default=True)
