import base64

from odoo import fields, models, api



class StockEmail(models.Model):
    _name = "stock.email"


    def cron_action(self):
        query = """Select stock_quant.id,stock_quant.product_id,stock_quant.company_id,stock_quant.quantity,pd.name,ld.name as t2,cn.name as t3 FROM stock_quant
INNER JOIN product_template as pd ON stock_quant.product_id = pd.id
INNER JOIN stock_location as ld ON stock_quant.location_id = ld.id
INNER JOIN res_company as cn ON stock_quant.company_id = cn.id
ORDER BY stock_quant.id;"""
        self.env.cr.execute(query)
        pdf_fetch = self.env.cr.dictfetchall()
        data = {
            'data_pdf': pdf_fetch,
            'date': fields.Date.today().strftime("%d/%m/%Y")

        }
        template_id = self.env.ref('stock_email.action_stock_report')._render_qweb_pdf(self, data=data)
        # print(template_id)
        data_record = base64.b64encode(template_id[0])
        ir_values = {
            'name': 'Stock Report',
            'type': 'binary',
            'datas': data_record,
            'res_model': 'stock.quant',
            'mimetype': 'application/x-pdf'
        }
        data_id = self.env['ir.attachment'].create(ir_values)
        admin = self.env['res.users'].search([]).filtered(lambda ml: ml.has_group("stock.group_stock_manager"))
        email_values = {
            "email_to": admin.email,
            "subject": "Daily Stock Report",
            "attachment_ids": data_id,
        }
        email = self.env['mail.mail'].sudo().create(email_values)
        email.send()


