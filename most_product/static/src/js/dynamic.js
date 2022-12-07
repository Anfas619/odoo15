odoo.define('most_product.dynamic', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet_blog',
       start: function () {
           var self = this;
           rpc.query({
               route: '/product_sold',
               params: {},
           }).then(function (result) {
               self.$target.empty().append(result);
           });
           console.log("worked!!!!1")
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});