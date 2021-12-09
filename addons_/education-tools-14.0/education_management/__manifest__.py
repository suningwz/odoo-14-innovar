{
    'name': 'Education Management',
    'version': '1.1',
    'category': 'Accounting',
    'sequence': 35,
    'summary': 'Manage financial, analytical and educational accounting.',
    'description': """""",
    'depends': ['account'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/attendance_sheet_sequence.xml',
        'data/payments_students_sequence.xml',
        'data/employee_data.xml',
        'data/category_course_data.xml',
        'views/education_management_view.xml',
        'views/education_management_tutor_view.xml',
        'views/education_management_employees_view.xml',
        'views/education_management_admission_view.xml',
        'views/education_management_admission_register_view.xml',
        'views/education_management_payments_students_view.xml',
        # 'views/education_management_payments_students_line_view.xml',
        'views/education_management_batch_view.xml',
        'views/education_management_course_category_view.xml',
        'views/education_management_course_view.xml',
        'views/education_management_teachers_view.xml',
        'views/education_management_classrooms_view.xml',
        'views/education_management_skills_teachers_view.xml',
        'views/education_management_attendance_teachers_view.xml',
        'views/education_management_attendances_students_register_view.xml',
        'views/education_management_attendances_students_sheet_view.xml',
        'views/education_management_attendances_students_line_view.xml',
        'views/res_config_settings.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
