from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Vehicle(models.Model):
    _name = "vehicle"
    _description = "vehicle"

    registration_no = fields.Char(string="Registration No")
    _sql_constraints = [
        ('ref_unique', 'unique(registration_no)', 'Registration No. should be unique.'),
    ]
    vehicle_type = fields.Selection([
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('other', 'Other')
    ], string='Vehicle',
        copy=False, index=True, tracking=3)

    name = fields.Char(compute='_compute_name', store="True")

    no_of_seats = fields.Integer("Number of Seats", default=1)

    facilities_ids = fields.Many2many('facilities')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    service_ids = fields.One2many('service.page', 'vehicle_id', string='service')

    @api.constrains('registration_no')
    def _check_registration_no(self):
        for rec in self:
            domain = [('registration_no', '=', rec.registration_no)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError("The Registration No should be unique")

    @api.depends('registration_no', 'vehicle_type')
    def _compute_name(self):
        for record in self:
            record.name = str(record.registration_no) + ' ' + str(record.vehicle_type)


#
class ServicePage(models.Model):
    _name = "service.page"
    _description = "service"

    service = fields.Char('Service')
    quantity = fields.Integer('Quantity', default=1)
    unit = fields.Integer('Unit')
    amount = fields.Integer('Amount')
    vehicle_id = fields.Many2one('vehicle', string='vehicle')
