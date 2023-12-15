odoo.define('spiffy_theme_backend.SpiffyPageTitle', function (require) {
"use strict";

    var AbstractWebClient = require('web.AbstractWebClient');
    var ajax = require('web.ajax');

    var SpiffyAbstractWebClient = AbstractWebClient.include({
        start: function () {
            this._super.apply(this, arguments);
            self = this
            ajax.rpc('/get/tab/title/').then(function(rec) {
                var new_title = rec
                self.set('title_part', {"zopenerp": new_title});
            })
        },
    });
});