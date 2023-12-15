odoo.define('pragmatic_odoo_whatsapp_integration.pos', function (require) {
'use strict';


var models = require('point_of_sale.models');
var gui = require('point_of_sale.gui');
var core = require('web.core');
var screens = require('point_of_sale.screens');
var Widget = require('web.Widget');

var ajax = require('web.ajax');


var qweb = core.qweb;
screens.ReceiptScreenWidget.include({

    renderElement: function() {
        var self = this;
        this._super();
        this.$('.js_custom_print').click(function(){
            self.click_custom_print();


        });
    },
    click_custom_print: function(){

        var order = this.pos.get_order();
        var order_list = this.pos.get_order_list();
        var client = order.get_client();
        var self = this
        // Render receipt screen and can print function
        if (client){
            var value = {
                'order': order.name,
                'formatted_validation_date': order.formatted_validation_date,
                'company_name': this.pos.company.name,
                'company_phone': this.pos.company.phone,
                'user_name': this.pos.user.name,
    //            'order_lines': order_list[0].orderlines.models
            }

             $.ajax({
                url : '/whatsapp/send/message',
                data : value,
                type: "POST",

                success: function (data) {
                    if (data == 'Send Message successfully'){
                        self.gui.show_popup('confirm', {
                            title: 'Message',
                            body: data,
                            'confirm': function() {
//                                this.close_popup();
                                this.gui.show_screen('receipt');
//                                self._close();
                            },
                        });
                    }
                    else{
                        self.gui.show_popup('error', {
                            title: 'Message',
                            body: data,
                        });
                    }
                }
            });
        }
        else{
             alert("You have not selected customer for this transaction")
        }

    }
});

});