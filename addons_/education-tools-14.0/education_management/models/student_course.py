from odoo import models, fields

class StudentCourse(models.Model):
    _name = "em.student.course"
    _description = "Student Course Details"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('em.student', 'Student', ondelete="cascade")
    course_id = fields.Many2one('em.course', 'Course', required=True)
    batch_id = fields.Many2one('em.batch', 'Batch', required=True)
    course_detail_ids = fields.One2many('em.payments.students', 'student_course_id',
                                        'Payment Details',
                                        readonly=True)

    _sql_constraints = [
        ('unique_name_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]