from odoo import http
from odoo.http import request


class PartnerForm(http.Controller):
    # mention class name
    @http.route(['/customer/form'], type='http', auth="public", website=True)
    def partner_form(self):
        team_rec = request.env['config.desk'].sudo().search([])
        values = {}
        values.update({
            'team': team_rec
        })
        return request.render("help_desk.tmp_ticket_form", values)

    @http.route(['/customer/form/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        partner = request.env['help.desk'].sudo().create({
            'subject_name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'customer_name': post.get('customer'),
            'help_id': post.get('help')
        })
        vals = {
            'partner': partner,
        }
        # inherited the model to pass the values to the model from the form#
        return request.render("help_desk.tmp_customer_form_success", vals)
        # finally send a request to render the thank you page#
