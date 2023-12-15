odoo.define('p_hide_show_buttons.hide_buttons', function (require) {
"use strict";

var ListController = require("web.ListController");
var FormController = require('web.FormController');
var GraphController = require('web.GraphController');
var KanbanController = require('web.KanbanController');
var PivotController = require('web.PivotController');
var rpc = require('web.rpc');
var Sidebar = require('web.Sidebar');
var core = require('web.core');
var _t = core._t;

    var includeDict = {
        renderButtons: async function () {
            this._super.apply(this, arguments);
            const hide_button_result = await this._rpc({
                "model": "res.users",
                "method": "hide_buttons",
                "args": ['import',this.modelName,this.viewType],
            }).then(function(output) {
                return output;
            });
            if (hide_button_result['import'] == true) {
                this.$buttons.find('button.o_button_import').hide();
            }
        }
    };

    ListController = ListController.include({
        _updateButtons: async function (mode) {
            this._super(mode)
            const hide_button_result = await this._rpc({
                "model": "res.users",
                "method": "hide_buttons",
                "args": [this.activeActions,this.modelName,this.viewType],
            }).then(function(output) {
                return output;
            });
            if (hide_button_result['save'] == true) {
                this.$('.o_list_button_save').toggleClass('o_hidden', hide_button_result['save']);
            }
            if (hide_button_result['discard'] == true) {
                this.$('.o_list_button_discard').toggleClass('o_hidden', hide_button_result['discard']);
            }
            if (hide_button_result['create'] == true) {
                this.$('.o_list_button_add').toggleClass('o_hidden', hide_button_result['create']);
            }
            if (hide_button_result['export'] == true) {
                this.$('.o_list_export_xlsx').toggleClass('o_hidden', hide_button_result['export']);
            }
        }
    });

    FormController = FormController.include({
        _updateButtons: async function () {
            this._super();
            const hide_button_result = await this._rpc({
                "model": "res.users",
                "method": "hide_buttons",
                "args": [this.activeActions,this.modelName,this.viewType],
            }).then(function(output) {
                return output;
            });
            if (hide_button_result['save'] == true) {
                this.$('.o_form_button_save').toggleClass('o_hidden', hide_button_result['save']);
            }
            if (hide_button_result['discard'] == true) {
                this.$('.o_form_button_cancel').toggleClass('o_hidden', hide_button_result['discard']);
            }
            if (hide_button_result['create'] == true) {
                this.$('.o_form_button_create').toggleClass('o_hidden', hide_button_result['create']);
            }
            if (hide_button_result['edit'] == true) {
                this.$('.o_form_button_edit').toggleClass('o_hidden', hide_button_result['edit']);
            }
        }
    });

    KanbanController = KanbanController.include({
        _updateButtons: async function () {
            this._super()
            const hide_button_result = await this._rpc({
                "model": "res.users",
                "method": "hide_buttons",
                "args": [this.activeActions,this.modelName,this.viewType],
            }).then(function(output) {
                return output;
            });
            if (hide_button_result['create'] == true) {
                this.$('.o-kanban-button-new').toggleClass('o_hidden', hide_button_result['create']);
            }
        }
    });

    PivotController = PivotController.include({
        _updateButtons: async function () {
            this._super()
            const hide_button_result = await this._rpc({
                "model": "res.users",
                "method": "hide_buttons",
                "args": [this.activeActions,this.modelName,this.viewType],
            }).then(function(output) {
                return output;
            });
            if (hide_button_result['export'] == true) {
                this.$buttons.find('.o_pivot_download').toggleClass('o_hidden', hide_button_result['export']);
            }
        }
    });

    // Hide Export option
 	Sidebar.include({

		init: function (parent, options) {
 			this.modelName = parent.modelName;
	    	this.viewType = parent.viewType;
	    	this._super(parent, options)
 		},

		start: function () {
 			var self = this;
		    var export_text = _t("Export");
		    var button = 'export';
	        var model_name = this.modelName;
	        var view_type = this.viewType;
		    var def = rpc.query({
                "model": "res.users",
                "method": "hide_buttons",
                "args": [button,model_name,view_type],
                "kwargs": {}
                }, {async: false}).then(function(output) {
                    if (output['export'] == true) {
                        self.items['other'] = $.grep(self.items['other'], function(i){
                            return i && i.label && i.label != export_text;
                        });
                    }
                });
		    return Promise.resolve(def).then(this._super.bind(this));
		},
 	});

    KanbanController.include(includeDict);
    ListController.include(includeDict);
});
