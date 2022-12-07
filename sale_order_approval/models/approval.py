from odoo import fields, models, api


class SalesOrderApproval(models.Model):
    _inherit = 'sale.order'

    # state = fields.Selection([
    #     ('waiting', 'Waiting For Approval'),
    #
    # ])
    state = fields.Selection(selection_add=[('waiting', "Waiting for Approval")])

    test_button = fields.Boolean()

    def need_to_approve(self):
        self.write({'state': 'waiting'})
        return True

    def approve_quotation(self):
        self.write({'state': 'sale'})
        return True

    def reject_quotation(self):
        self.write({'state': 'draft'})
        return True

    @api.onchange("order_line")
    def on_change_price_unit(self):
        a = self.order_line.product_id.list_price
        b = self.order_line.price_unit
        print(b)
        print(a)
        if a > b:
            self.test_button = False

            return {'warning': {
                'title': 'Warning ',
                'message': 'When changing the Unit Price U need approval from manager.'

            }
            }

        if a < b:
            self.test_button = False

            return {'warning': {
                'title': 'Warning ',
                'message': 'When changing the Unit Price U need approval from manager.'
            }
            }

        else:
            self.test_button = True
            print(self.test_button)
