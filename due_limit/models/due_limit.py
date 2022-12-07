from odoo import fields, models


class Limit(models.Model):
    _inherit = 'res.partner'

    limit = fields.Float(string="Limit")











