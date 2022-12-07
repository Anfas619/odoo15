from odoo import fields, models


class Service(models.Model):
    _name = "service.types"
    _description = "service_types"

    name = fields.Char("name")
    expiration_period = fields.Integer('expiration period')


