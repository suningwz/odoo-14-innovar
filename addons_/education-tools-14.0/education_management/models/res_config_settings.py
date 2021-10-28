from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    url = fields.Char(string="Moodle Site URL")
    token = fields.Char(string="Token", password=True)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('education_management.url', self.url)
        self.env['ir.config_parameter'].set_param('education_management.token', self.token)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config_paramenter_sudo = self.env['ir.config_parameter'].sudo()
        url = ir_config_paramenter_sudo.get_param('education_management.url')
        token = ir_config_paramenter_sudo.get_param('education_management.token')
        res.update(
            url=url,
            token=token
        )
        return res