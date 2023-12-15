odoo.define("rp_hide_create_tree_v13.HideCreateImportExportBtnList", function(require) {
    "use strict";

    var ListController = require('web.ListController');
    var session = require('web.session');

    ListController.include({
        
        willStart: function () {
            var self = this;
            var def_create = session.user_has_group('rp_hide_create_tree_v13.group_create_btn_access').then(function (has_create_group) {
                self.has_create_group = has_create_group;
            });
            var def_import = session.user_has_group('rp_hide_create_tree_v13.group_import_btn_access').then(function (has_import_group) {
                self.has_import_group = has_import_group;
            });
            var def_export = session.user_has_group('rp_hide_create_tree_v13.group_export_btn_access').then(function (has_export_group) {
                self.has_export_group = has_export_group;
            });
            return Promise.all([this._super.apply(this, arguments), def_create, def_import, def_export]);
        },
    })
});

odoo.define("rp_hide_create_tree_v13.HideCreateEditBtnList", function(require) {
    "use strict";

    var FormController = require('web.FormController');
    var session = require('web.session');

    FormController.include({
        
        willStart: function () {
            var self = this;
            var def_create = session.user_has_group('rp_hide_create_tree_v13.group_create_btn_access').then(function (has_create_group) {
                self.has_create_group = has_create_group;
            });
            var def_edit = session.user_has_group('rp_hide_create_tree_v13.group_edit_form_btn_access').then(function (has_edit_group) {
                self.has_edit_group = has_edit_group;
            });
            return Promise.all([this._super.apply(this, arguments), def_create, def_edit]);
        },
    })
});

odoo.define("rp_hide_create_tree_v13.HideCreateImportBtnKanban", function(require) {
    "use strict";

    var KanbanController = require('web.KanbanController');
    var session = require('web.session');

    KanbanController.include({
        
        willStart: function () {
            var self = this;
            var def_create = session.user_has_group('rp_hide_create_tree_v13.group_create_btn_access').then(function (has_create_group) {
                self.has_create_group = has_create_group;
            });
            var def_import = session.user_has_group('rp_hide_create_tree_v13.group_import_btn_access').then(function (has_import_group) {
                self.has_import_group = has_import_group;
            });
            return Promise.all([this._super.apply(this, arguments), def_create, def_import]);
        },
    })
});
