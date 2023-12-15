odoo.define('spiffy_theme_backend.SwitchCompanyMenu', function (require) {
    'use strict';

    var config = require('web.config');
    var core = require('web.core');
    var session = require('web.session');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var SwitchCompanyMenu = require('web.SwitchCompanyMenu');

    var _t = core._t;

    var CustomSwitchCompanyMenu = SwitchCompanyMenu.include({
        init: function () {
            this._super.apply(this, arguments);
            this.isDebug = config.isDebug();
            this.isAssets = config.isDebug("assets");
            this.isTests = config.isDebug("tests");
        },
    });
});