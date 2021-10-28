from dateutil.relativedelta import relativedelta
from odoo import models, fields

class Admission(models.Model):
    _name = 'em.admission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_admission'

    name_admission = fields.Char(string="Name", required=True)
    start_date_admission = fields.Date(
        'Start Date Admission', required=True, readonly=False,
        default=fields.Date.today())
    end_date_admission = fields.Date(
        'End Date Admission', required=True, readonly=False,
        default=(fields.Date.today() + relativedelta(days=30)))
    batch_id = fields.Many2one('em.batch', "Course Batch", required=True,
                               domain=[('active', '=', 'true')])
    admission_register_id = fields.One2many('em.admission.register', 'admission_id', readonly=True)
