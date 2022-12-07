from random import randint

from odoo import fields, models


class Config(models.Model):
    _name = "config.desk"
    _rec_name = "help_name"

    help_name = fields.Char("Helpdesk Team")
    company_id = fields.Many2one(
        'res.company', 'Company', index=True,
        default=lambda self: self.env.company)


class Tags(models.Model):
    _name = "tag.desk"
    _rec_name = "tag_name"
    def _get_default_color(self):
        return randint(1, 11)

    tag_name = fields.Char("Tags")
    color = fields.Integer('Color', default=_get_default_color)








