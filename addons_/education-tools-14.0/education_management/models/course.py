from odoo import models, fields
import requests

class Course(models.Model):
    _name = "em.course"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_course'

    moodle_course_id = fields.Integer(string="Moodle ID", readonly=True)
    name_course = fields.Char(string="Name", required=True)
    short_name_course = fields.Char(string="Short Name", required=True)
    requires_enrollment_price = fields.Boolean(string="Requires Enrollment Price", default=False)
    type_of_course = fields.Selection([
        ('classroom','Classroom Course'), ('distance','Distance Course')],
        string="Type Of Course", default='classroom', required=True)
    description_course = fields.Text(string="Description")
    category_id = fields.Many2one('em.category', "Category")
    price_per_month = fields.Float(string="Price Per Month", required=True)
    enrollment_price = fields.Float(string="Enrollment Price", required=True)
    product_template_id = fields.Many2one('product.template', "Product")
    active = fields.Boolean(default=True)

    def get_moodle_parameters(self):
        config = self.env['ir.config_parameter']
        siteUrl = config.sudo().get_param("education_management.url")
        tokenSite = config.sudo().get_param("education_management.token")
        parameters = {
            'url': siteUrl,
            'token': tokenSite
        }
        return parameters

    def helper_functions_moodle_courses_category(self):

        moodle_functions = {
            'create':'core_course_create_courses',
            'update':'core_course_update_courses',
            'delete':'core_course_delete_courses',
            'get_by': 'core_course_get_courses_by_field',
            'get':'core_course_get_courses'
        }

        return moodle_functions

    def create_courses_moodle(self):
        """
            Estructura General

            list of(object{
                fullname string   //Full Name
                shortname string   //Course Short Name
                categoryid int   //Category Id
                idnumber string  Opcional //Id Number
                summary string  Opcional //Summary
                summaryformat int  Valor por Defecto "1" //Summary Format (1 = HTML, 0 = MOODLE,
                                                            2 = PLAIN or 4 = MARKDOWN)
                format string  Valor por Defecto "topics" //Course Format: weeks, topics, social, site
                showgrades int  Valor por Defecto "1" //1 If Grades Are Shown, Otherwise 0
                newsitems int  Valor por Defecto "5" //Number Of Recent Items Appearing On The Course Page
                startdate int  Opcional //Timestamp When The Course Start
                enddate int  Opcional //Timestamp When The Course End
                numsections int  Opcional //(Deprecated, Use courseformatoptions) Number Of Weeks/Topics
                maxbytes int  Valor por Defecto "0" //Largest Size Of File That Can Be Uploaded Into The Course
                showreports int  Valor por Defecto "0" //Are Activity Report Shown (Yes = 1, No =0)
                visible int  Opcional //1: Available To Student, 0:Not Available
                hiddensections int  Opcional //(Deprecated, Use courseformatoptions) How The Hidden Sections
                                                    In The Course Are Displayed To Students
                groupmode int  Valor por Defecto "0" //No Group, Separate, Visible
                groupmodeforce int  Valor por Defecto "0" //1: Yes, 0: No
                defaultgroupingid int  Valor por Defecto "0" //Default Grouping Id
                enablecompletion int  Opcional //Enabled, Control Via Completion And Activity Settings. Disabled,
                                                    Not Shown In Activity Settings.
                completionnotify int  Opcional //1: Yes 0: No
                lang string  Opcional //Forced Course Language
                forcetheme string  Opcional //Name Of The Force Theme
                courseformatoptions  Opcional //Additional Options For Particular Course Format
                    list of(object{
                        name string   //Course Format Option Name
                        value string   //Course Format Option Value
                    })
                customfields  Opcional //Custom Fields For The Course
                    list of(object{
                        shortname string   //The Shortname Of The Custom Field
                        value string   //The Value Of The Custom Field
                    }
                )}
            )

            REST (Parámetros POST)

            courses[0][fullname]= string
            courses[0][shortname]= string
            courses[0][categoryid]= int
            courses[0][idnumber]= string
            courses[0][summary]= string
            courses[0][summaryformat]= int
            courses[0][format]= string
            courses[0][showgrades]= int
            courses[0][newsitems]= int
            courses[0][startdate]= int
            courses[0][enddate]= int
            courses[0][numsections]= int
            courses[0][maxbytes]= int
            courses[0][showreports]= int
            courses[0][visible]= int
            courses[0][hiddensections]= int
            courses[0][groupmode]= int
            courses[0][groupmodeforce]= int
            courses[0][defaultgroupingid]= int
            courses[0][enablecompletion]= int
            courses[0][completionnotify]= int
            courses[0][lang]= string
            courses[0][forcetheme]= string
            courses[0][courseformatoptions][0][name]= string
            courses[0][courseformatoptions][0][value]= string
            courses[0][customfields][0][shortname]= string
            courses[0][customfields][0][value]= string
        """

        config_parameter = self.get_moodle_parameters()
        function = self.helper_functions_moodle_courses_category()
        url = config_parameter.get('url')
        token = 'wstoken='+config_parameter.get('token')
        wsfunction = '&wsfunction='+function.get('create')
        rest_format = '&moodlewsrestformat='+'json'

        mainUrl = url + '/webservice/rest/server.php?' + token + wsfunction + rest_format

        payload = {
            'courses[0][fullname]': self.name_course,
            'courses[0][shortname]': self.shor_name_course,
            'courses[0][categoryid]': self.category_id.moodle_category_id.id,
            'courses[0][idnumber]': 0,
            'courses[0][summary]': self.description_course,
            'courses[0][summaryformat]': 1,
            'courses[0][format]': "topics",
            'courses[0][newsitems]': 1,
            'courses[0][startdate]': 0,
            'courses[0][enddate]': 0,
            'courses[0][maxbytes]': 0,
            'courses[0][showreports]': 0,
            'courses[0][visible]' : 1,
            'courses[0][groupmode]': 0,
            'courses[0][groupmodeforce]' : 0,
            'courses[0][defaultgroupingid]': 0,
            'courses[0][enablecompletion]': 0,
            'courses[0][completionnotify]': 0
        }
        files = []
        headers = {}
        response = requests.request("POST", mainUrl, headers=headers, data=payload, files=files)

        response_j = response.json()
        for data in response_j:
            self.moodle_course_id = data.get('id')

    def update_courses_moodle(self):
        """
            Estructura General

            list of(object{
                id int // ID Of Course
                fullname string   //Full Name
                shortname string   //Course Short Name
                categoryid int   //Category Id
                idnumber string  Opcional //Id Number
                summary string  Opcional //Summary
                summaryformat int  Valor por Defecto "1" //Summary Format (1 = HTML, 0 = MOODLE,
                                                            2 = PLAIN or 4 = MARKDOWN)
                format string  Valor por Defecto "topics" //Course Format: weeks, topics, social, site
                showgrades int  Valor por Defecto "1" //1 If Grades Are Shown, Otherwise 0
                newsitems int  Valor por Defecto "5" //Number Of Recent Items Appearing On The Course Page
                startdate int  Opcional //Timestamp When The Course Start
                enddate int  Opcional //Timestamp When The Course End
                numsections int  Opcional //(Deprecated, Use courseformatoptions) Number Of Weeks/Topics
                maxbytes int  Valor por Defecto "0" //Largest Size Of File That Can Be Uploaded Into The Course
                showreports int  Valor por Defecto "0" //Are Activity Report Shown (Yes = 1, No =0)
                visible int  Opcional //1: Available To Student, 0:Not Available
                hiddensections int  Opcional //(Deprecated, Use courseformatoptions) How The Hidden Sections In
                                                The Course Are Displayed To Students
                groupmode int  Valor por Defecto "0" //No Group, Separate, Visible
                groupmodeforce int  Valor por Defecto "0" //1: Yes, 0: No
                defaultgroupingid int  Valor por Defecto "0" //Default Grouping Id
                enablecompletion int  Opcional //Enabled, Control Via Completion And Activity Settings. Disabled,
                                                    Not Shown In Activity Settings.
                completionnotify int  Opcional //1: Yes 0: No
                lang string  Opcional //Forced Course Language
                forcetheme string  Opcional //Name Of The Force Theme
                courseformatoptions  Opcional //Additional Options For Particular Course Format
                    list of(object{
                        name string   //Course Format Option Name
                        value string   //Course Format Option Value
                    })
                customfields  Opcional //Custom Fields For The Course
                    list of(object{
                        shortname string   //The Shortname Of The Custom Field
                        value string   //The Value Of The Custom Field
                    }
                )}
            )

            REST (Parámetros POST)

            courses[0][id]= int
            courses[0][fullname]= string
            courses[0][shortname]= string
            courses[0][categoryid]= int
            courses[0][idnumber]= string
            courses[0][summary]= string
            courses[0][summaryformat]= int
            courses[0][format]= string
            courses[0][showgrades]= int
            courses[0][newsitems]= int
            courses[0][startdate]= int
            courses[0][enddate]= int
            courses[0][numsections]= int
            courses[0][maxbytes]= int
            courses[0][showreports]= int
            courses[0][visible]= int
            courses[0][hiddensections]= int
            courses[0][groupmode]= int
            courses[0][groupmodeforce]= int
            courses[0][defaultgroupingid]= int
            courses[0][enablecompletion]= int
            courses[0][completionnotify]= int
            courses[0][lang]= string
            courses[0][forcetheme]= string
            courses[0][courseformatoptions][0][name]= string
            courses[0][courseformatoptions][0][value]= string
            courses[0][customfields][0][shortname]= string
            courses[0][customfields][0][value]= string
        """

    def delete_courses_moodle(self):
        """
            Estructura General

            list of(
                id int   //Course ID
            )

            REST (Parámetros POST)

            courseids[0]= int
        """

    def get_by_courses_moodle(self):
        """
            Estructura General

            field string  Valor por Defecto ""
                //The Field To Search Can Be Left Empty For All Courses Or:
                    id: Course Id
                    ids: Comma Separated Course Ids
                    shortname: Course Short Name
                    idnumber: Course Id Number
                    category: Category Id The Course Belongs To

            REST (Parámetros POST)

            field= string
        """

    def get_courses_moodle(self):
        """
            Estructura General

            Valor por defecto para "Array()" //Options - Operator OR Is Used
            options object{
                ids  Opcional //List Of Course Id. If Empty Return All Courses Except Front Page Course.
                list of(
                    ids int //Course Id
                )
            }

            REST (Parámetros POST)

            options[ids][0]= int
        """

    def sync_courses_moodle(self):
        pass

    def create_product_template(self):
        for record in self:
            self.env['product.template'].create({
                'name': "Enrollement " + self.name_course,
                'sale_ok': True,
                'purchase_ok': False,
                'type': 'consu',
                'categ_id': 1,
                'default_code': "Enroll " + self.short_name_course,
                'list_price': self.enrollement_price
            })
            product_id = self.env['product.template'].create({
                'name': self.name_course,
                'sale_ok': True,
                'purchase_ok': False,
                'type': 'consu',
                'categ_id': 1,
                'default_code': self.short_name_course,
                'list_price': self.price_per_month
            }).id
            record.product_template_id = product_id