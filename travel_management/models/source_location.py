from odoo import fields, models


class Location(models.Model):
    _name = "source.location"
    _description = "location"
    _rec_name = "location"

    location = fields.Char("Location")
