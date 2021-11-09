from dateutil.relativedelta import relativedelta
from odoo import models, fields

class Batch(models.Model):
    _name = 'em.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_batch'

    name_batch = fields.Char(string="Name", required=True)
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today())
    end_date = fields.Date(string="End Date", required=True)
    course_id = fields.Many2one('em.course', 'Course', required=True)
    classrooms_id = fields.Many2one('em.classrooms', "Classrooms", required=True)
    active = fields.Boolean(default=True)
    create_admission = fields.Boolean(default=True)
    admission_id = fields.Many2one('em.admission', 'Admission')
    skills_teachers_id = fields.One2many('em.skills.teachers', 'batch_id',
                                        'Teachers Detail', readonly=True)

    def get_admission_vals(self):
        vals = {
            'name_admission': 'Enrollments ' + self.name_batch,
            'start_date_admission': self.start_date - relativedelta(days=30),
            'end_date_admission': self.start_date + relativedelta(days=15)
        }
        return vals

    def create_batch_admission(self):
        for data in self:
            if data.create_admission:
                batch_id = self.env['em.batch'].search([], order='create_date desc', limit=1)[0].id
                vals = data.get_admission_vals()
                admission_id = self.env['em.admission'].create({
                    'name_admission': vals.get('name_admission'),
                    'start_date_admission': vals.get('start_date_admission'),
                    'end_date_admission': vals.get('end_date_admission'),
                    'batch_id': batch_id
                }).id
                data.admission_id = admission_id
