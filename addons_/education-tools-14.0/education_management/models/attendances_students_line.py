from odoo import models, fields, api


class AttendancesStudentsLine(models.Model):
    _name = 'em.attendances.students.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('em.student', 'Student', required=True)
    attendance_id = fields.Many2one(
        'em.attendances.students.sheet', 'Attendance Sheet', required=True, ondelete="cascade")
    attendance_date = fields.Date(
        'Date', related='attendance_id.attendance_date', store=True,
        readonly=True)
    present = fields.Boolean('Present', default=True)
    excused = fields.Boolean('Absent Excused')
    absent = fields.Boolean('Absent Unexcused')
    late = fields.Boolean('Late')
    course_id = fields.Many2one(
        'em.course', 'Course',
        related='attendance_id.attendance_register_id.batch_id.course_id', store=True,
        readonly=True)
    batch_id = fields.Many2one(
        'em.batch', 'Batch',
        related='attendance_id.attendance_register_id.batch_id', store=True,
        readonly=True)