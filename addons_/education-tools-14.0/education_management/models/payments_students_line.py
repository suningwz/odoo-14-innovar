from odoo import models, fields, api

class PaymentsStudentsLine(models.Model):
    _name = 'em.payments.students.line'
    _description = "Payments Lines"
    _rec_name = 'payment_line_sequence'

    payment_line_sequence = fields.Char(string="Payment Line Receipt", readonly=True, required=True, copy=False, default=lambda self:
    self.env['ir.sequence'].next_by_code('em.payments.students.line'))
    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('mp', 'MercadoPago'),
        ('exchange', 'Exchange'),
        ('card', 'Card')], string="Payment Type", default='cash', required=True)
    payment_date = fields.Date(string="Payment Date", default=fields.Date.today(), required=True)
    payments_students_id = fields.Many2one('em.payments.students', "Payment Student", domain="[('active', '=', True)]", required=True)
    total_paid = fields.Float(string="Total Paid", required=True, readonly=False)
    cash_register_id = fields.Many2one('em.cash.register', "Cash Register", domain="[('active', '=', True)]")
    observations = fields.Text(string="Observations")
    active = fields.Boolean(string="Is Active", required=True, default=True)