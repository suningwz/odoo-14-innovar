from odoo import fields, models, api


class AttendancesTeachers(models.Model):
    _name = 'em.attendances.teachers'
    _description = 'Attendances Teachers'

    date_attendance = fields.Date('Date Attendance', required=True, readonly=False,
                                  default=fields.Date.today())
    batch_id = fields.Many2one('em.batch', 'Batch', required=True, track_visibility='onchange')
    teachers_id = fields.Many2one('em.employees', 'Teacher',
                                  domain="['|', ('work_position', '=', 'teach'), ('work_position', '=', 'secre_teach')]",
                                  required=True)
