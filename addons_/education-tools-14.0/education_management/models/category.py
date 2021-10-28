from odoo import models, fields
import requests

class Category(models.Model):
    _name = 'em.category'
    _rec_name = 'name_category'

    moodle_category_id = fields.Integer(string="Moodle ID", readonly=True)
    name_category = fields.Char(string="Category", required=True)
    description_category = fields.Text(string="Description")

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
            'create':'core_course_create_categories',
            'update':'core_course_update_categories',
            'delete':'core_course_delete_categories',
            'get':'core_course_get_categories'
        }

        return moodle_functions

    def get_categories_courses_moodle(self):

        config_parameter = self.get_moodle_parameters()
        function = self.helper_functions_moodle_courses_category()
        url = config_parameter.get('url')
        token = 'wstoken='+config_parameter.get('token')
        wsfunction = '&wsfunction='+function.get('get')
        rest_format = '&moodlewsrestformat='+'json'

        mainUrl = url + '/webservice/rest/server.php?' + token + wsfunction + rest_format

        payload = {}
        files = []
        headers = {}

        response = requests.request("GET", mainUrl, headers=headers, data=payload, files=files)
        """
            Display Json Response in Console 
        """
        """     
        response_j = response.json()
        for data in response_j:
            category_id = data.get('id')
            category_name = data.get('name')
            print('ID: '+str(category_id)+' '+'Name: '+category_name)
        """
        return response

    def delete_categories_courses_moodle(self):

        """
            Estructura General

            list of (object {
                id int   //Category Id to Delete
                newparent int  Opcional //The Parent Category To Move The Contents To, If Specified
                recursive int  Valor por Defecto"0" //1: Recursively Delete All Contents Inside This
                                Category, 0 (Default): Move Contents To newparent Or Current Parent Category
                                 (Except If Parent Is Root)
                }
            )

            REST (Parámetros POST)

            categories[0][id]= int
            categories[0][newparent]= int
            categories[0][recursive]= int
        """

        config_parameter = self.get_moodle_parameters()
        function = self.helper_functions_moodle_courses_category()
        url = config_parameter.get('url')
        token = 'wstoken='+config_parameter.get('token')
        wsfunction = '&wsfunction='+function.get('get')
        rest_format = '&moodlewsrestformat='+'json'

        mainUrl = url + '/webservice/rest/server.php?' + token + wsfunction + rest_format

        payload = {
            'categories[0][id]' : self.moodle_category_id,
            'categories[0][recursive]': 0
        }
        files = []
        headers = {}

        requests.request("POST", mainUrl, headers=headers, data=payload, files=files)

    def update_categories_courses_moodle(self):

        """
            Estructura General

            list of (object {
                id int   //Course Id
                name string  Opcional //Category Name
                idnumber string  Opcional //Category Id Number
                parent int  Opcional //Parent Category Id
                description string  Opcional //Category Description
                descriptionformat int  Valor por Defecto "1" //Description Format (1 = HTML, 0 = MOODLE, 2 = PLAIN or 4 = MARKDOWN)
                theme string  Opcional //The Category Theme.
                }
            )

            REST (Parámetros POST)

            categories[0][id]= int
            categories[0][name]= string
            categories[0][idnumber]= string
            categories[0][parent]= int
            categories[0][description]= string
            categories[0][descriptionformat]= int
            categories[0][theme]= string
        """

        config_parameter = self.get_moodle_parameters()
        function = self.helper_functions_moodle_courses_category()
        url = config_parameter.get('url')
        token = 'wstoken='+config_parameter.get('token')
        wsfunction = '&wsfunction='+function.get('update')
        rest_format = '&moodlewsrestformat='+'json'

        mainUrl = url + '/webservice/rest/server.php?' + token + wsfunction + rest_format

        payload = {
            'categories[0][id]': self.moodle_category_id,
            'categories[0][name]': self.name_category,
            'categories[0][description]': self.description_category
        }
        files = []
        headers = {}

        requests.request("POST", mainUrl, headers=headers, data=payload, files=files)

    def create_categories_courses_moodle(self):

        """
            Estructura General

            list of (object {
                name string  Opcional //Category Name
                idnumber string  Opcional //Category Id Number
                parent int   Valor por Defecto "0" //The Parent Category Id Inside Which The New Category Will Be Created
                                         - Set To 0 For a Root Category
                description string  Opcional //Category Description
                descriptionformat int  Valor por Defecto "1" //Description Format (1 = HTML, 0 = MOODLE, 2 = PLAIN or 4 = MARKDOWN)
                theme string  Opcional //The Category Theme.
                }
            )

            REST (Parámetros POST)

            categories[0][name]= string
            categories[0][idnumber]= string
            categories[0][parent]= int
            categories[0][description]= string
            categories[0][descriptionformat]= int
            categories[0][theme]= string
        """

        config_parameter = self.get_moodle_parameters()
        function = self.helper_functions_moodle_courses_category()
        url = config_parameter.get('url')
        token = 'wstoken='+config_parameter.get('token')
        wsfunction = '&wsfunction='+function.get('create')
        rest_format = '&moodlewsrestformat='+'json'

        mainUrl = url + '/webservice/rest/server.php?' + token + wsfunction + rest_format

        payload = {
            'categories[0][name]': self.name_category,
            'categories[0][description]': self.description_category
        }
        files = []
        headers = {}
        response = requests.request("POST", mainUrl, headers=headers, data=payload, files=files)

        response_j = response.json()
        for data in response_j:
            self.moodle_category_id = data.get('id')

    def sync_categories_courses_moodle(self):
        pass