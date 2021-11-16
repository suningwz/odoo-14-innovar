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
    total_amount = fields.Float(string="Total Amount", compute='compute_total_amount', required=True)
    total_paid = fields.Float(string="Total Paid", required=True, readonly=False)
    total_balance = fields.Float(string="Total Balance", required=True)
    observations = fields.Text(string="Observations")
    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('mp', 'MercadoPago'),
        ('exchange', 'Exchange'),
        ('card', 'Card')], string="Payment Type", default='cash', required=True)
    invoice_status = fields.Selection([
        ('pending', 'Pending Billing'),
        ('invoiced', 'Invoiced')
    ], default='pending', required=True)
    partner_id = fields.Many2one('res.partner', "Customer", required=True)
    pay_lines_id = fields.One2many('em.payment.students.line', 'receipt_id', "Details")

    @api.depends('pay_lines_id.product_template_id')
    def compute_total_amount(self):
        for line in self:
            line.total_amount = sum(line.pay_lines_id.product_template_id.mapped('list_price'))

    @api.onchange('total_amount')
    def onchange_total_amount(self):
        for data in self:
            data.total_paid = data.total_amount

    @api.onchange('total_paid')
    def onchange_total_paid(self):
        for data in self:
            data.total_balance = data.total_amount - data.total_paid

    def payment_invoice_status_pending(self):
        self.invoice_status = 'pending'

    def payment_invoice_status_invoiced(self):
        self.invoice_status = 'invoiced'

class PaymentsStudentsLine(models.Model):
    _name = 'em.payment.students.line'
    _description = "Payments Students Line"

    quantity = fields.Integer(string="Quantity", default=1)
    discount = fields.Integer(string="Discount", default=0)
    product_template_id = fields.Many2one('product.template', 'Line', required=True)
    receipt_id = fields. Many2one('em.payments.students', "Receipt")