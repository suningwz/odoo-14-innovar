from odoo import models, fields, api


class AttendancesStudentsLine(models.Model):
    _name = 'em.attendances.students.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('em.student', 'Student', required=True, tracking=True)
    attendance_id = fields.Many2one(
        'em.attendances.students.sheet', 'Attendance Sheet', required=True,
        tracking=True, ondelete="cascade")
    attendance_date = fields.Date(
        'Date', related='attendance_id.attendance_date', store=True,
        readonly=True, tracking=True)
    present = fields.Boolean('Present', default=True, tracking=True)
    excused = fields.Boolean('Absent Excused', tracking=True)
    absent = fields.Boolean('Absent Unexcused', tracking=True)
    late = fields.Boolean('Late', tracking=True)
    course_id = fields.Many2one(
        'em.course', 'Course',
        related='attendance_id.attendance_register_id.batch_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'em.batch', 'Batch',
        related='attendance_id.attendance_register_id.batch_id', store=True,
        readonly=True)
