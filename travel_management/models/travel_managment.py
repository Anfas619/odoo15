from odoo import fields, models, api


class Travel(models.Model):
    _name = "travel.management"
    _description = "Travel_Model"
    _rec_name = "bookingreference"

    bookingreference = fields.Char(string='booking reference', required=True,
                                   readonly=True, default=lambda self: 'New')
    customer_id = fields.Many2one('res.partner')
    No_of_passengers = fields.Integer("No of passengers", default=1)
    service = fields.Selection([('flight', 'FLIGHT'), ('train', 'TRAIN'), ('bus', 'BUS')])
    booking_date = fields.Date("Booking Date", default=fields.Date.today())
    booking_expiration_date = fields.Date("Expiration Date", )
    source_location_id = fields.Many2one('source.location')
    destination_location_id = fields.Many2one("source.location")
    travel_date = fields.Datetime("Travelling Date")
    service_type_id = fields.Many2one("service.types")
    total = fields.Float(string="Total", compute="compute_total", store=True)
    invoice_id = fields.Many2one('account.move')

    check_ids = fields.One2many('service.page.two', 'booking_id', string='test')
    vehicle_type = fields.Selection([
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('other', 'Other')
    ], string='Vehicle',
        copy=False, index=True, tracking=3)
    vehicle_list = fields.Many2one('vehicle')
    fees = fields.Integer('Fees')

    # test = fields.Date.today()
    # dd = travel_date.Date()

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('expired', 'Expired'),
    ], string='State',
        copy=False, index=True, tracking=3, default='draft')

    # button action
    def action_do_something(self):
        self.write({'state': 'confirmed'})
        return True

    def action_do_invoice(self):
        lst = []
        lst.clear()
        print(self.service_type_id.id)
        for rec in self:
            print(rec)
            # print(self)
            if self.service_type_id:
                for i in rec.check_ids:
                    test123 = {
                        "name": i.service,
                        "quantity": i.quantity,
                        'price_unit': i.amount,
                        'price_subtotal': i.subtotal
                    }
                    print(test123)
                    lst.append(test123)
                    print(lst)
            else:
                test123 = {
                    "name": str(self.bookingreference) + ' ' + str(self.service)
                }
                print(test123)
                lst.append(test123)
                print(lst)

        self.invoice_id = self.env['account.move'].create([
            {
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.context_today(self),
                'partner_id': self.customer_id.id,
                # 'currency_id': self.currency_id.id,
                'amount_total': self.total,
                'invoice_line_ids': lst

            }
        ])
        return {
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window'
        }

    @api.model
    def create(self, vals):
        if vals.get('bookingreference', 'New') == 'New':
            vals['bookingreference'] = self.env['ir.sequence'].next_by_code(
                'travel.management') or 'New'
        res = super(Travel, self).create(vals)
        return res

    @api.onchange('service_type_id', 'booking_date')
    def _onchange_service_types(self):
        period = int(self.service_type_id.expiration_period)

        booking_dates = self.booking_date
        if booking_dates:
            exp_date = fields.Date.add(
                booking_dates, days=period
            )

            self.booking_expiration_date = exp_date
            print(exp_date)

    def cron_action(self):

        exp_rec = self.env['travel.management'].search([])

        # state1 = exp_rec.mapped('state')
        for rec in exp_rec:
            if rec.booking_expiration_date < fields.date.today():
                rec.state = 'expired'
                print(self.env['travel.management'])

    @api.depends('check_ids.subtotal')
    def compute_total(self):
        for record in self:
            record.total = sum(record.mapped('check_ids').mapped('subtotal'))

