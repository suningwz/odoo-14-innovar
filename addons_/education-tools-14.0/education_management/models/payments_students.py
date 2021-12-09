from odoo import models, fields, api


class PaymentsStudents(models.Model):
    _name = 'em.payments.students'
    _description = "Payments Students"
    _rec_name = 'payment_sequence'

    payment_sequence = fields.Char(string="Receipt", readonly=True, required=True, copy=False, default=lambda self:
    self.env['ir.sequence'].next_by_code('em.payments.students'))
    date_of_issue = fields.Date(string="Date Of Issue", default=fields.Date.today(), required=True)
    due_date = fields.Date(string="Due Date", required=True)
    ref_name = fields.Selection([
        ('enrollment', 'Enrollment'),
        ('quota1', 'Quota I'),
        ('quota2', 'Quota II'),
        ('quota3', 'Quota III'),
        ('quota4', 'Quota IV'),
        ('quota5', 'Quota V'),
        ('quota6', 'Quota VI'),
        ('quota7', 'Quota VII'),
        ('quota8', 'Quota VIII'),
        ('quota9', 'Quota IX'),
        ('quota10', 'Quota X'),
        ('quota11', 'Quota XI'),
        ('quota11', 'Quota XII')], string="Reference", default='quota1', required=True)
    total_amount = fields.Float(string="Total Amount", required=True)
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
    student_id = fields.Many2one('em.student', "Student", required=True)
    partner_id = fields.Many2one('res.partner', "Customer", readonly=True)
    student_course_id = fields.Many2one('em.student.course', "Details")
    # pay_lines_id = fields.One2many('em.payment.students.line', 'receipt_id', "Details")

    @api.onchange('student_id')
    def onchange_student_id(self):
        for data in self:
            partner_id = self.env['res.partner'].search([
                ('vat', '=', data.student_id.identification_number_student),
                ('email', '=', data.student_id.email_student),
                ('name', '=', data.student_id.name_student)
            ], limit=1).id
            data.partner_id = partner_id

    # @api.depends('pay_lines_id')
    # def compute_total_amount(self):
    #     for line in self:
    #         sum_amount = sum(line.pay_lines_id.product_template_id.mapped('list_price'))
    #         line.total_amount = sum_amount * line.pay_lines_id.quantity - line.pay_lines_id.discount

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


# class PaymentsStudentsLine(models.Model):
#     _name = 'em.payment.students.line'
#     _description = "Payments Students Line"
#
#     quantity = fields.Integer(string="Quantity", default=1)
#     discount = fields.Integer(string="Discount", default=0,
#                               help="The value of this field must be interpreted as an amount over the price of the product ")
#     product_template_id = fields.Many2one('product.template', 'Line', required=True)
#     receipt_id = fields.Many2one('em.payments.students', "Receipt")
