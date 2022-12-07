from odoo import fields, models


class Absent(models.Model):
    _name = 'absent.list'

    employee_id = fields.Many2one('hr.employee')
    date = fields.Date(string="Date", default=fields.Date.today())

    # action
    def cron_action(self):

        exp_rec = self.env['hr.employee'].search([])
        for rec in exp_rec:
            employee_checkin = rec.last_check_in
            if employee_checkin != False:
                date = employee_checkin
                checkin_date = date.date()
                # print(checkin_date)
                if checkin_date != fields.date.today():
                    print(rec.name)
                    self.env['absent.list'].create([{
                        'employee_id': rec.id,

                    }])
        # the  checkin date which is in False value
        exp_false = self.env['hr.employee'].search([('last_check_in', '=', False)])
        # print(exp_false)
        for false in exp_false:
            # print(false.name)
            self.env['absent.list'].create([{
                'employee_id': false.id,

            }])
