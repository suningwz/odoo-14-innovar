from odoo import models, fields, api

class SkillsTeachers(models.Model):
    _name = "em.skills.teachers"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'teachers_id'

    date_from = fields.Date('Date From', required=True, readonly=False,
        default=fields.Date.today())
    date_to = fields.Date('Date To', required=True, readonly=False,
        default=fields.Date.today())
    batch_id = fields.Many2one('em.batch', 'Batch', required=True, track_visibility='onchange')
    teachers_id = fields.Many2one('em.teachers', 'Teachers', required=True, track_visibility='onchange')
    teaching_role = fields.Selection([
        ('assistant','Assistant Teacher'), ('titular','Titular Teacher')],
        string="Teaching Role", default='titular', required=True)

