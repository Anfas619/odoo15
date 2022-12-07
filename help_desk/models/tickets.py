from odoo import fields, models, api

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class HelpDesk(models.Model):
    _name = "help.desk"
    _rec_name = "subject_name"
    _inherit = "mail.thread"


    subject_name = fields.Char("Subject")
    help_id = fields.Many2one("config.desk",string="HelpDesk Team")
    user_id = fields.Many2one('res.users', string="Assigned to", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("tag.desk")
    company_id = fields.Many2one(
        'res.company', 'Company', index=True,
        default=lambda self: self.env.company)

    set_priority = fields.Selection(AVAILABLE_PRIORITIES, select=True, string="Priority")
    customer_id = fields.Many2one("res.partner")
    customer_name = fields.Char("Customer Name")
    email = fields.Char(string='Email',readonly=False)
    phone = fields.Char(string='Phone',readonly=False)
    state = fields.Selection([
        ('new', 'NEW'),
        ('inprogress', 'INPROGRESS'),
        ('done', 'DONE'),
        ('cancelled', 'Cancelled')
    ], string='Vehicle',
        copy=False, index=True, tracking=3, default='new')



    def action_to_work(self):
        self.write({'state': 'inprogress'})
        return True

    def action_to_done(self):
        self.write({'state': 'done'})
        return True
    def action_to_cancel(self):
        self.write({'state': 'cancelled'})
        return True





