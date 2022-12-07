odoo.define('point_of_sale.custom_due_limit', function (require) {
"use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    var models = require('point_of_sale.models');
    const { Gui } = require('point_of_sale.Gui');
    var Registries = require('point_of_sale.Registries');
    models.load_fields('res.partner', 'limit');


    const custom_due_limit = (ProductScreen) =>
        class extends ProductScreen {
            async _onClickPay() {
                var customer = this.currentOrder.get_client();
                var amount = this.currentOrder.get_total_with_tax();
                console.log("amount---",amount)
//                console.log("test",customer.limit)
                console.log("customer",customer)

                if (!customer){
                    Gui.showPopup('ErrorPopup',{
                         'title': ('Error: Customer Selection Error'),
                         'body': ('Must Select a Customer')
                          });
                    }
                    else{
                        if (customer.limit < amount){
//                        console.log("12345",customer.limit)
//                        console.log("5667",amount)
                          Gui.showPopup('ErrorPopup',{
                              'title': ('Error: Payment Limit Error'),
                              'body': ('Your Account Due Limit is' + customer.limit)
                          });
                        }
//                        if (customer.limit == 0){
//                        Gui.showPopup('ErrorPopup',{
//                            'title': ('Error : Payment Limit Error'),
//                              'body' : ('Your Account Due Limit Hasnt Set')})
//
//                        }
                        else{
                        await super._onClickPay()}
                        }

}
}
    Registries.Component.extend(ProductScreen, custom_due_limit);

    return ProductScreen;
});
