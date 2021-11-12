from odoo import models, fields, api

class AttendacesStudentsSheet(models.Model):
    _name = "em.attendances.students.sheet"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Attendance Sheet"
    _order = "attendance_date desc"

    name_sheet = fields.Char(string="Name Sheet", readonly=True, required=True, copy=False, default=lambda self:
    self.env['ir.sequence'].next_by_code('em.attendances.students.sheet'))
    attendance_register_id = fields.Many2one('em.attendances.students', 'Attendace Register', required=True)
    attendance_date = fields.Date(
        'Date', required=True, default=fields.Date.today(),
        tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('start', 'Attendance Start'),
         ('done', 'Attendance Taken'), ('cancel', 'Cancelled')],
        'Status', default='draft', tracking=True)
    course_id = fields.Many2one(
        'em.course', 'Course',
        related='attendance_register_id.batch_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'em.batch', 'Batch',
        related='attendance_register_id.batch_id', store=True,
        readonly=True)
    attendance_line_id = fields.One2many(
        'em.attendances.students.line', 'attendance_id', 'Attendance Line')
    active = fields.Boolean(default=True)

    def attendance_draft(self):
        self.state = 'draft'

    def attendance_start(self):
        self.state = 'start'

    def attendance_done(self):
        self.state = 'done'

    def attendance_cancel(self):
        self.state = 'cancel'