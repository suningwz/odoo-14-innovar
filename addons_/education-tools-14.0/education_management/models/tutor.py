from odoo import models, fields

class Tutor(models.Model):
    _name = 'em.tutor'
    _rec_name = 'name_tutor'

    name_tutor = fields.Char(string="Name", required=True)
    email_tutor = fields.Char(string="Email", required=True, default="default@gmail.com")
    street_tutor = fields.Char(string="Street", required=True, default="S/D")
    phone_tutor = fields.Char(string="Phone", required=True, default="111111111")
    identification_type_tutor = fields.Selection([
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
    identification_number_tutor = fields.Char(string="Identification Number", required=True)
    responsibility_type_tutor = fields.Selection([
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
    student_id = fields.One2many('em.student', 'parent_id', "Student Tutor", readonly=True)