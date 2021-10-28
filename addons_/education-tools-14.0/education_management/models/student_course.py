from odoo import models, fields

class StudentCourse(models.Model):
    _name = "em.student.course"
    _description = "Student Course Details"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('em.student', 'Student', ondelete="cascade", track_visibility='onchange')
    course_id = fields.Many2one('em.course', 'Course', required=True, track_visibility='onchange')
    batch_id = fields.Many2one('em.batch', 'Batch', required=True, track_visibility='onchange')

    _sql_constraints = [
        ('unique_name_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]