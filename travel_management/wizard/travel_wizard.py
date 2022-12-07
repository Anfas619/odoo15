from odoo import fields, models
import json
import io
import xlsxwriter


class Wizard(models.Model):
    _name = 'travel.wizard'

    date_from = fields.Datetime("Date from")
    date_to = fields.Date("Date to")
    customer_id = fields.Many2one('res.partner')

    def action_done(self):
        query = """Select  a.location,b.location as loc2,vehicle_type, state,travel_date,booking_expiration_date,customer_id from travel_management join source_location a on source_location_id=a.id join source_location b on destination_location_id=b.id """
        if self.customer_id:
            partner=""" where customer_id ='%s' """% self.customer_id.id
            query+=partner
        if self.date_from:
            date_compare= """ and travel_date >= '%s '"""% self.date_from
            query+=date_compare
        if self.date_to:
            date_compare_two = """ and booking_expiration_date >= '%s '"""% self.date_to
            query+=date_compare_two
        self.env.cr.execute(query)
        pdf_fetch = self.env.cr.dictfetchall()
        data = {
            'model_id': self.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer_id': self.customer_id.name,
            'data_pdf': pdf_fetch
        }
        return self.env.ref('travel_management.action_travel_report').report_action(None, data=data)

    def excel_done(self):
        query = """Select  a.location,b.location as loc2,vehicle_type, state,travel_date,booking_expiration_date,customer_id from travel_management join source_location a on source_location_id=a.id join source_location b on destination_location_id=b.id """
        if self.customer_id:
            partner=""" where customer_id ='%s' """% self.customer_id.id
            query+=partner
        if self.date_from:
            date_compare= """ and travel_date >= '%s '"""% self.date_from
            query+=date_compare
        if self.date_to:
            date_compare_two = """ and booking_expiration_date >= '%s '"""% self.date_to
            query+=date_compare_two
        self.env.cr.execute(query)
        pdf_fetch = self.env.cr.dictfetchall()
        print(pdf_fetch)
        data = {
            'model_id': self.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer_id': self.customer_id.name,
            'data_pdf': pdf_fetch

        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'travel.wizard',
                     'options': json.dumps(data, default=fields.date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Travel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print(1234567)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        sheet.merge_range('A1:F2', 'Travel Management Report', head)
        header = workbook.add_format({'align': 'cent', 'bold': True, 'font_size': '10px'})
        date = workbook.add_format({'bold': True})
        customer = workbook.add_format({'bold':True})
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        if data['date_from']:
            sheet.write(4, 0, 'From', date)
            sheet.write(4, 1, data['date_from'])
        if data['date_to']:
            sheet.write(5, 0, 'To', date)
            sheet.write(5, 1, data['date_to'])
        if data['customer_id']:
            sheet.write(6,0, 'Customer',  customer)
            sheet.write(6,1, data['customer_id'])
        row = 7
        col = 0
        sheet.write(row, col, 'SL.No', header)
        sheet.write(row, col + 1, 'Source Location', header)
        sheet.write(row, col + 2, 'Destination Location', header)
        sheet.write(row, col + 3, 'Vehicle Name', header)
        sheet.write(row, col + 4, 'State', header)
        rows = 7
        cols = 0
        sl_no = 0
        values = data.get('data_pdf')
        for rec in values:
            rows = rows + 1
            sl_no = sl_no + 1
            sheet.write(rows, cols, sl_no)
            sheet.write(rows, cols + 1, rec.get('location'))
            sheet.write(rows, cols + 2, rec.get('loc2'))
            sheet.write(rows, cols + 3, rec.get('vehicle_type'))
            sheet.write(rows, cols + 4, rec.get('state'))
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

