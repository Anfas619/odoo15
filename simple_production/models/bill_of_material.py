from odoo import fields, models, api


class Bill(models.Model):
    _name = "bill.material"
    _rec_name = "product_id"
    _inherit = "mail.thread"

    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_variant = fields.Many2one('product.product', string="Product Variant", domain="[('id', '=', product_id)]")

    product_qty = fields.Float(string="Quantity", default=1)
    reference = fields.Char('Reference')
    company_id = fields.Many2one(
        'res.company', 'Company', index=True,
        default=lambda self: self.env.company)
    component_ids = fields.One2many("component.value", "bill_id")


class Component(models.Model):
    _name = "component.value"

    product_id = fields.Many2one("product.product", string="Product")
    comp_product_qty = fields.Float(string="Quantity", default=1)

    bill_id = fields.Many2one("bill.material")
