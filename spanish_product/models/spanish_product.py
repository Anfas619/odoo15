from odoo import fields, models


class Spanish(models.Model):
    _inherit = 'product.template'

    product_spanish = fields.Char(string="Spanish Name")
