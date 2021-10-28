from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AdmissionRegister(models.Model):
    _name = 'em.admission.register'
    _inherit = 'em.student'
    _rec_name = 'name_student'
    _table = 'em_admission_register'

    is_student = fields.Boolean(string="Is Student", default=False)
    enrollment_date = fields.Date(string="Enrollment Date", default=fields.Date.today(), required=True, readonly=True)
    student_id = fields.Many2one('em.student', 'Student')
    partner_id = fields.Many2one('res.partner', 'Partner')
    admission_id = fields.Many2one('em.admission', "Admission", required=True)

    @api.onchange('student_id', 'is_student')
    def onchange_student(self):
        if self.is_student and self.student_id:
            student = self.student_id
            self.name_student = student.name_student
            self.email_student = student.email_student
            self.street_student = student.street_student
            self.phone_student = student.phone_student
            self.date_of_birth_student = student.date_of_birth_student
            self.years_old_student = student.years_old_student
            self.identification_type_student = student.identification_type_student
            self.identification_number_student = student.identification_number_student
            self.responsibility_type_student = student.responsibility_type_student
            self.educational_establishment = student.educational_establishment
            self.educational_establishment_schedule = student.educational_establishment_schedule
            self.name_city = student.name_city
            self.zipcode = student.zipcode
            self.state_id = student.state_id.id
            self.country_id = student.country_id.id
            self.parent_id = student.parent_id.id
        else:
            self.name_student = ''
            self.email_student = 'default@gmail.com'
            self.street_student = 'S/D'
            self.phone_student = '111111111'
            self.date_of_birth_student = ''
            self.years_old_student = '0'
            self.identification_type_student = '5'
            self.identification_number_student = ''
            self.responsibility_type_student = '5'
            self.educational_establishment = ''
            self.educational_establishment_schedule = 'm'
            self.name_city = ''
            self.zipcode = ''
            self.state_id = ''
            self.country_id = ''
            self.parent_id = ''

    def get_student_vals(self):
        for student in self:
            details = {
                'name_student': student.name_student,
                'email_student': student.email_student,
                'street_student': student.street_student,
                'date_of_birth_student': student.date_of_birth_student,
                'years_old_student': student.years_old_student,
                'phone_student': student.phone_student,
                'identification_type_student': student.identification_type_student,
                'identification_number_student': student.identification_number_student,
                'responsibility_type_student': student.responsibility_type_student,
                'educational_establishment': student.educational_establishment,
                'educational_establishment_schedule': student.educational_establishment_schedule,
                'name_city': student.name_city,
                'zipcode': student.zipcode,
                'state_id': student.state_id.id,
                'country_id': student.country_id.id,
                'parent_id': student.parent_id.id
            }

        return details

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

    def enroll_student(self):
        for record in self:
            if not record.is_student:
                vals_student = record.get_student_vals()
                vals_parent = record.get_parent_vals()
                student_id = self.env['em.student'].create(vals_student).id
                record.student_id = student_id
                partner_id = self.env['res.partner'].create({
                    'name': vals_parent.get('name_tutor'),
                    'street': vals_parent.get('street_tutor'),
                    'phone': vals_parent.get('phone_tutor'),
                    'email': vals_parent.get('email_tutor'),
                    'l10n_latam_identification_type_id': int(vals_parent.get('identification_type_tutor')),
                    'vat': vals_parent.get('identification_number_tutor'),
                    'l10n_ar_afip_responsibility_type_id': int(vals_parent.get('responsibility_type_tutor'))
                }).id
                record.partner_id = partner_id
                self.env['em.student.course'].create({
                    'student_id': record.student_id.id,
                    'course_id': record.admission_id.batch_id.course_id.id,
                    'batch_id': record.admission_id.batch_id.id
                })
            else:
                vals_parent = record.get_parent_vals()
                partner_id = self.env['res.partner'].search([
                    ('vat', '=', vals_parent.get('identification_number_tutor')),
                    ('email', '=', vals_parent.get('email_tutor')),
                    ('name', '=', vals_parent.get('name_tutor'))
                ], limit=1).id
                if partner_id:
                    record.partner_id = partner_id
                    self.env['em.student.course'].create({
                        'student_id': record.student_id.id,
                        'course_id': record.admission_id.batch_id.course_id.id,
                        'batch_id': record.admission_id.batch_id.id
                    })
                else:
                    raise ValidationError("The res.partner Of em.parent Don't Exist")