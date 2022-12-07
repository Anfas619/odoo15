from odoo import fields, models, api


class Tourpackage(models.Model):
    _name = "tour.package"
    _description = "tour package"
    _rec_name = "customer_id"

    customer_id = fields.Many2one("res.partner")
    quotations_date = fields.Date("Quotation Date")
    source_location_id = fields.Many2one("source.location")
    destination_location_id = fields.Many2one("source.location")
    start_date = fields.Date("Start Date")
    end_date = fields.Date('End Date')
    no_of_travellers = fields.Integer('Number of Travellers')
    facilities_ids = fields.Many2many('facilities')
    total = fields.Float(string="Total", compute="compute_test", store=True)

    tour_ids = fields.One2many('service.page.two', 'package_id', string='test')
    # estimation_amount_ids = fields.One2many('service.page.two', 'estimation_amount_id', string = 'XD')

    vehicle_type = fields.Selection([
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('other', 'Other')
    ], string='Vehicle',
        copy=False, index=True, tracking=3)
    vehicle_list = fields.Many2one('vehicle')
    # domain="[('vehicle_type', '=', vehicle_type),"
    #        "('facilities_ids', '=', Facilities_ids,),"
    #        "('start_date', '=', start_date,),"
    #        "('end_date', '=', end_date,),"
    #        "('no_of_seats', '=', no_of_travellers,)]", )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='State',
        copy=False, index=True, default='draft')

    # -->total calculation
    @api.depends('tour_ids.subtotal')
    def compute_test(self):
        for record in self:
            record.total = sum(record.mapped('tour_ids').mapped('subtotal'))

    # -->vehicle list value changing
    @api.onchange('vehicle_list')
    def _onchange_vehicle_list(self):
        for rec in self:
            print(self)
            lines = [(5, 0, 0)]
            print('self.vehicle_list', self.vehicle_list)
            for line in self.vehicle_list.service_ids:
                val = {
                    'service': line.service,
                    'quantity': line.quantity,
                    'amount': line.amount
                }
                lines.append((0, 0, val))
                print('lines', lines)
                rec.tour_ids = lines

    # cofirm button in tourpackage
    def action_confirm_booking(self):
        self.env['travel.management'].create([{
            'customer_id': self.customer_id.id,
            'travel_date': self.start_date,
            'source_location_id': self.source_location_id.id,
            'destination_location_id': self.destination_location_id.id,
            'vehicle_type': self.vehicle_type,
            'vehicle_list': self.vehicle_list.id,
            'check_ids': self.tour_ids

        }])


class ServicePageTwo(models.Model):
    _name = "service.page.two"
    _description = "service.two"

    service = fields.Char('Service')
    quantity = fields.Integer('Quantity', default=1)
    amount = fields.Integer('Amount')
    subtotal = fields.Float(compute='_compute_value', store="True")

    package_id = fields.Many2one('tour.package', string='vehicle')
    booking_id = fields.Many2one('travel.management', string="book")

    # estimation_amount_id = fields.Many2one('tour.package', string = "")

    @api.onchange('quantity', 'amount')
    def _compute_value(self):
        for record in self:
            record.subtotal = record.quantity * record.amount
    #
    # def action_confirm_booking(self):
    #     test = self.env['travel.management'].create([{
    #         'service': self.service,
    #         'quatity': self.quantity,
    #         'amount': self.amount,
    #         'subtotal': self.subtotal,
    #
    #
    #     }])
    #
    #
