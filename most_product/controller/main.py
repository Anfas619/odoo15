from collections import Counter

from odoo import http
from odoo.http import request


class Sales(http.Controller):
    @http.route('/product_sold', type="json", auth="public")
    def sold_total(self, products_per_slide =3):
        web_obj = request.env['website.track'].sudo().search([
            ('product_id', '!=', False)
        ]),
        print(32527453274)
        product_list = []
        lista = []
        lista.clear()
        for i in web_obj:
            # print(i," web obh")
            # print(2)
            for j in i:

                lista.append(j.product_id.id)
                # print(lista)
                count = Counter(lista).most_common()
                # print(count)
        for k in range(6):
            product = request.env['product.product'].sudo().search([('id', '=',count[k][0])])
            # print(product)


            for i in product:
                data = {
                    'name': i.name,
                    'image': i.image_1920,
                    'url': i.website_url

                }
                product_list.append(data)


            product_group=[]
            product_test=[]
            for index, record in enumerate(product_list, 1):
                product_test.append(record)
                if index % products_per_slide == 0:
                    product_group.append(product_test)
                    product_test = []
            if any(product_test):
                product_group.append(product_test)
                # print(product_group)

            li = {
                'values': product_list,
                'product_group': product_group
            }


        value_list=[]

        sale_obj=request.env['product.template'].sudo().search([]).sorted("sales_count", reverse=True)
        # print(sale_obj)
        for x in range(6):
            # print(sale_obj[x][0])
            test = sale_obj[x][0]
            # print(test.name)

            data_two = {
                'name': test.name,
                'image': test.image_1920,
                'url': test.website_url

            }
            value_list.append(data_two)

            product_group1=[]
            product_test1=[]
            for index, record in enumerate(value_list, 1):
                product_test1.append(record)
                if index % products_per_slide == 0:
                    product_group1.append(product_test1)
                    product_test1 = []
            if any(product_test1):
                product_group1.append(product_test1)
                print(product_group1)
            li.update({
                'rest' : value_list,
                'product_group1': product_group1
            })






        res = http.Response(template='most_product.basic_snippet', qcontext=li)
        return res.render()

























