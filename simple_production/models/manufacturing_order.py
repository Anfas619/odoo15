from odoo import fields, models, api


class Manufacturing(models.Model):
    _name = "manufacture.order"
    _inherit = "mail.thread"
    _rec_name = "product_id"

    product_id = fields.Many2one('product.product', string="Product", tracking=True, required=True)
    bom_id = fields.Many2one("bill.material", string="Bill of Material", domain="[('product_id', '=', product_id)]",
                             required=True)
    product_qty = fields.Float(string="Quantity", tracking=True, required=True)
    scheduled_date = fields.Datetime('Scheduled Date', default=fields.Datetime.today())
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)
    orginal_quantity = fields.Float(related='bom_id.product_qty')
    ratio = fields.Float()
    move_date = fields.Datetime()

    company_id = fields.Many2one(
        'res.company', 'Company', index=True,
        default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),

    ], string='State',
        copy=False, index=True, tracking=True, default='draft')

    consume_ids = fields.One2many("consume.order", "manufacture_id", string="Component")

    @api.onchange('bom_id')
    def _onchange_bom_id(self):

        self.product_qty = self.bom_id.product_qty
        lines = [(5, 0, 0)]

        for line in self.bom_id.component_ids:
            val = {
                'product_id': line.product_id,
                'consume_qty': line.comp_product_qty,
                'origin_qty': line.comp_product_qty,

            }
            lines.append((0, 0, val))
            # print('lines', lines)
            self.consume_ids = lines

    def confirm_action(self):
        self.move_date = fields.Datetime.now()
        self.write({'state': 'confirmed'})
        s_location = self.env['stock.location'].search(
            [('usage', '=', 'production'), ('company_id', '=', self.company_id.id), ('name', '=', 'Production')])
        d_location = self.env['stock.location'].search(
            [('company_id', '=', self.company_id.id), ('name', '=', 'Stock')])
        # print("src", s_location)
        # print("dest", d_location)
        # print(self.product_id)
        # print(self.product_id.product_tmpl_id.uom_id.id)
        # print(self.product_qty)

        move = self.env['stock.move'].create({
            'name': 'Use on MyLocation',
            'location_id': s_location.id,
            'location_dest_id': d_location.id,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.product_tmpl_id.uom_id.id,
            'product_uom_qty': self.product_qty,
        })
        move._action_confirm()
        move._action_assign()
        move.move_line_ids.write(
            {'qty_done': self.product_qty})  # This creates a stock.move.line record. You could also do it manually
        move._action_done()

        if self.consume_ids:
            for rec in self.consume_ids:
                print(self.consume_ids)
                print(rec)

                move = self.env['stock.move'].create({
                    'name': 'Use on MyLocation',
                    'location_id': d_location.id,
                    'location_dest_id': s_location.id,
                    'product_id': rec.product_id.id,
                    'product_uom': rec.product_id.product_tmpl_id.uom_id.id,
                    'product_uom_qty': rec.consume_qty,
                })
            move._action_confirm()
            move._action_assign()
            move.move_line_ids.write(
                {
                    'qty_done': rec.consume_qty})  # This creates a stock.move.line record. You could also do it manually
            move._action_done()

    @api.onchange("product_qty")
    def action_product_quantity_change(self):
        if self.bom_id:
            self.ratio = self.product_qty / self.orginal_quantity
            print(self.ratio)
            for rec in self.consume_ids:
                print(rec.origin_qty)
                rec.consume_qty = self.ratio * rec.origin_qty
                print(rec.consume_qty)

    def product_moves(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Moves',
            'view_mode': 'tree',
            'res_model': 'stock.move.line',
            'domain': [('product_id', '=', self.product_id.id), ('reference', '=', 'Use on MyLocation'),
                       ('date', '=', self.move_date)],
            'context': "{'create': False}"

        }


class Consume(models.Model):
    _name = "consume.order"

    product_id = fields.Many2one("product.product", string="Product")
    consume_qty = fields.Float(string="To Consume", default=1)
    origin_qty = fields.Float(string="To consume")
    manufacture_id = fields.Many2one("manufacture.order")
