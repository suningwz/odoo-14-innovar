from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = "em.student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_student'

    name_student = fields.Char(string="Name", required=True)
    email_student = fields.Char(string="Email", required=True, default="default@gmail.com")
    street_student = fields.Char(string="Street", required=True, default="S/D")
    phone_student = fields.Char(string="Phone", required=True, default="111111111")

    name_city = fields.Char("Name City", required=True, translate=True)
    zipcode = fields.Char("Zip")
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one(
        'res.country.state', 'State', domain="[('country_id', '=', country_id)]")

    date_of_birth_student = fields.Date(string="Date of Birth", required=True)
    years_old_student = fields.Char(string="Age", required=True)
    identification_type_student = fields.Selection([
        ('4','CUIT'), ('5','DNI'), ('6','CUIL'), ('3','Foreign ID'),
        ('2','Passport'), ('8','CPF'), ('9','CBA'), ('10','CCat'),
        ('11','CCor'), ('12','CCorr'), ('13','CIER'), ('14','CIJ'),
        ('15','CIMen'), ('16','CILR'), ('17','CIS'), ('18','CISJ'),
        ('19','CISL'), ('20','CISF'), ('21','CISdE'), ('22','CIT'),
        ('23','CICha'), ('24','CIChu'), ('25','CIF'), ('26','CIMis'),
        ('27','CIN'), ('28','CILP'), ('29','CIRN'), ('30','CISC'),
        ('31','CITdF'), ('32','CDI'), ('33','LE'), ('34','LC'),
        ('35','ET'), ('36','AN'), ('37','CIBAR'), ('38','CdM'),
        ('39','UpApP'), ('7','Sigd')
    ], string="Identification Type", default='5' ,required=True)
    identification_number_student = fields.Char(string="Identification Number", required=True)
    responsibility_type_student = fields.Selection([
        ('1','IVA Responsable Inscripto'),
        ('2','IVA Responsable no Inscripto'),
        ('3','IVA no Responsable'),
        ('4','IVA Sujeto Exento'),
        ('5','Consumidor Final'),
        ('6','Responsable Monotributo'),
        ('7','Sujeto no Categorizado'),
        ('8','Cliente / Proveedo del Exterior'),
        ('9','IVA Liberado – Ley Nº 19.640'),
        ('10','IVA Responsable Inscripto – Agente de Percepción'),
        ('11','Pequeño Contribuyente Eventual'),
        ('12','Monotributista Social'),
        ('13','Pequeño Contribuyente Eventual Social'),
        ('14','IVA No Alcanzado')
    ], string="Responsibility Type", default='5', required=True)
    educational_establishment = fields.Char(string="Educational Establishment", required=True)
    educational_establishment_schedule = fields.Selection([
        ('m','Morning'), ('a','Afternoon'), ('n','Nights')
    ], string="Educational Schedule", default='m', required=True)
    contains_tutor = fields.Boolean(string="Contains Tutor?", required=True)
    parent_id = fields.Many2one('em.tutor', "Tutor")
    course_detail_ids = fields.One2many('em.student.course', 'student_id',
                                        'Course Details',
                                        track_visibility='onchange', readonly=True)

    @api.onchange('date_of_birth_student')
    def get_years_old(self):
        years_old = relativedelta(datetime.now(), self.date_of_birth_student)
        self.years_old_student = years_old.years


    def get_parent_vals(self):
        for parent in self:
            details = {
                'name_tutor': parent.parent_id.name_tutor,
                'email_tutor': parent.parent_id.email_tutor,
                'street_tutor': parent.parent_id.street_tutor,
                'phone_tutor': parent.parent_id.phone_tutor,
                'identification_type_tutor': parent.parent_id.identification_type_tutor,
                'identification_number_tutor': parent.parent_id.identification_number_tutor,
                'responsibility_type_tutor': parent.parent_id.responsibility_type_tutor,
            }

        return details

    def create_partner(self):
        for data in self:
            vals = data.get_parent_vals()
            self.env['res.partner'].create({
                    'name': vals.get('name_tutor'),
                    'street': vals.get('street_tutor'),
                    'phone': vals.get('phone_tutor'),
                    'email': vals.get('email_tutor'),
                    'l10n_latam_identification_type_id': int(vals.get('identification_type_tutor')),
                    'vat': vals.get('identification_number_tutor'),
                    'l10n_ar_afip_responsibility_type_id': int(vals.get('responsibility_type_tutor'))
                })