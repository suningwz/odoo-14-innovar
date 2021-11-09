from odoo import models, fields, api

class SkillsTeachers(models.Model):
    _name = "em.skills.teachers"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'teachers_id'

    date_from = fields.Date('Date From', required=True, readonly=False)
    date_to = fields.Date('Date To', required=True, readonly=False)
    batch_id = fields.Many2one('em.batch', 'Batch', required=True, track_visibility='onchange')
    teachers_id = fields.Many2one('em.teachers', 'Teachers', required=True, track_visibility='onchange')
    teaching_role = fields.Selection([
        ('assistant','Assistant Teacher'), ('titular','Titular Teacher')],
        string="Teaching Role", default='titular', required=True)

    @api.onchange('batch_id')
    def ochange_batch(self):
        for record in self:
            self.date_from = self.batch_id.start_date
            self.date_to = self.batch_id.end_date