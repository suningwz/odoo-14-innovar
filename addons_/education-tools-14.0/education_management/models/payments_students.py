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
        ('quota12', 'Quota XII')], string="Reference", default='quota1', required=True)
    total_amount = fields.Float(string="Total Amount", required=True, readonly=True)
    total_paid = fields.Float(string="Total Paid", required=True, readonly=True)
    total_balance = fields.Float(string="Total Balance", required=True, readonly=True)
    observations = fields.Text(string="Observations")
    invoice_status = fields.Selection([
        ('pending', 'Pending Billing'),
        ('invoiced', 'Invoiced')
    ], default='pending', required=True)
    student_id = fields.Many2one('em.student', "Student", required=True)
    partner_id = fields.Many2one('res.partner', "Customer", readonly=True)
    student_course_id = fields.Many2one('em.student.course', "Details")
    active = fields.Boolean(string="Is Active", default=True)

    @api.onchange('student_id')
    def onchange_student_id(self):
        for data in self:
            partner_id = self.env['res.partner'].search([
                ('vat', '=', data.student_id.identification_number_student),
                ('email', '=', data.student_id.email_student),
                ('name', '=', data.student_id.name_student)
            ], limit=1).id
            data.partner_id = partner_id

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