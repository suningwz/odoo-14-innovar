# Authors: See README.RST for Contributors
# Copyright 2015-2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unidecode import unidecode

from odoo import _, api, exceptions, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _format_template_name(self, text):
        text = unidecode(text)
        text.lower()
        return text

    def _prepare_qweb_view_data(self, qweb_name, arch):
        return {
            "name": qweb_name,
            "mode": "primary",
            "type": "qweb",
            "arch": arch,
        }

    def _prepare_model_data_data(self, qweb_name, module, qweb_view):
        return {
            "module": module,
            "name": qweb_name,
            "res_id": qweb_view.id,
            "model": "ir.ui.view",
        }

    def _create_qweb(self, name, qweb_name, module, model, arch):
        qweb_view_data = self._prepare_qweb_view_data(qweb_name, arch)
        qweb_view = self.env["ir.ui.view"].create(qweb_view_data)
        model_data_data = self._prepare_model_data_data(qweb_name, module, qweb_view)
        self.env["ir.model.data"].create(model_data_data)

    @api.model
    def create(self, values):
        values["report_name"] = self._format_template_name(
            values.get("report_name", "")
        )
        if (
            values.get("report_type") in ["qweb-pdf", "qweb-html"]
            and values.get("report_name")
            and values["report_name"].find(".") == -1
        ):
            raise exceptions.UserError(
                _("Template Name must contain at least a dot in it's name")
            )
        if not self.env.context.get("enable_duplication", False):
            return super(IrActionsReport, self).create(values)
        report_xml = super(IrActionsReport, self).create(values)
        if values.get("report_type") in ["qweb-pdf", "qweb-html"]:
            report_view_ids = self.env.context.get("report_views", False)
            suffix = self.env.context.get("suffix") or "copy"
            name = values["name"]
            model = values["model"]
            report = values["report_name"]
            module = report.split(".")[0]
            report_name = report.split(".")[1]
            for report_view in self.env["ir.ui.view"].browse(report_view_ids):
                origin_name = report_name.replace(("_%s" % suffix), "")
                origin_module = module.replace(("_%s" % suffix), "")
                new_report_name = "{}_{}".format(origin_name, suffix)
                qweb_name = report_view.name.replace(origin_name, new_report_name)
                arch = report_view.arch.replace(origin_name, new_report_name).replace(
                    origin_module + ".", module + "."
                )
                report_xml._create_qweb(name, qweb_name, module, model, arch)
            if not report_view_ids:
                arch = '<?xml version="1.0"?>\n' '<t t-name="%s">\n</t>' % report_name
                report_xml._create_qweb(name, report_name, module, model, arch)
        return report_xml

    def copy(self, default=None):
        if not self.env.context.get("enable_duplication", False):
            return super(IrActionsReport, self).copy(default=default)
        if default is None:
            default = {}
        suffix = self.env.context.get("suffix") or "copy"
        default["name"] = "{} ({})".format(self.name, suffix)
        module = "{}_{}".format(self.report_name.split(".")[0], suffix.lower())
        report = "{}_{}".format(self.report_name.split(".")[1], suffix.lower())
        default["report_name"] = "{}.{}".format(module, report)
        report_views_domain = self.associated_view()["domain"]
        report_views = self.env["ir.ui.view"].search(report_views_domain)
        return super(
            IrActionsReport,
            self.with_context(report_views=report_views.ids, suffix=suffix.lower()),
        ).copy(default=default)

    def button_create_qweb(self):
        self.ensure_one()
        module = self.report_name.split(".")[0]
        report_name = self.report_name.split(".")[1]
        arch = '<?xml version="1.0"?>\n' '<t t-name="%s">\n</t>' % self.report_name
        self._create_qweb(self.name, report_name, module, self.model, arch)
        self.associated_view()
