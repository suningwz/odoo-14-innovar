from odoo import models, fields, api


class PaymentsStudents(models.Model):
    _name = 'em.payments.students'
    _description = "Payments Students"
    _rec_name = 'payment_sequence'

    payment_sequence = fields.Char(string="Receipt", readonly=True, required=True, copy=False, default=lambda self:
    self.env['ir.sequence'].next_by_code('em.payments.students'))
    date_of_issue = fields.Date(string="Date Of Issue", default=fields.Date.today(), required=True)
    due_date = fields.Date(string="Due Date", required=True)
    ref_name = fields.Char(string="Reference")
    total_amount = fields.Float(string="Total Amount", required=True)
    observations = fields.Text(string="Observations")
    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('mp', 'MercadoPago'),
        ('exchange', 'Exchange'),
        ('card', 'Card')], string="Payment Type", default='cash', required=True)
    payment_status = fields.Selection([
        ('draft', 'Draft'),
        ('in_pay', 'In Payment'),
        ('paid', 'Paid')
    ], string="Payment Status", default='draft', required=True)
    invoice_status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Billing'),
        ('invoiced', 'Invoiced')
    ], default='draft', required=True)
    partner_id = fields.Many2one('res.partner', "Customer", required=True)
    pay_lines_id = fields.One2many('em.payment.students.line', 'receipt_id', "Details")


class PaymentsStudentsLine(models.Model):
    _name = 'em.payment.students.line'
    _description = "Payments Students Line"

    quantity = fields.Integer(string="Quantity", default=1)
    discount = fields.Integer(string="Discount", default=0)
    product_template_id = fields.Many2one('product.template', 'Line', required=True)
    receipt_id = fields. Many2one('em.payments.students', "Receipt")