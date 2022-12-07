from odoo import fields, models


class facilities(models.Model):
    _name = "facilities"
    _description = "Facilities"
    _rec_name = "facilities"

    facilities = fields.Char("facilities")
