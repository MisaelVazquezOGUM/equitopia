odoo.define('spiffy_theme_backend.split_viewjs', function(require) {
    "use strict";

    var core = require('web.core');
    var dom = require('web.dom');
    var ActionManager = require('web.ActionManager');
    const config = require("web.config");

    ActionManager.include({
        _pushController: function(controller) {
            var self = this;

            if (!$('body').hasClass('tree_form_split_view') || controller.viewType != 'form' || !this.getCurrentController() || self.getCurrentController()['viewType'] != 'list' || (this.actions[controller['actionID']].res_model != this.actions[this.getCurrentController()['actionID']].res_model)) {
                //default call
                this.$el.removeClass('tree_form_split')
                $('.o_list_view').attr('style','')
                $('.tree-form-viewer').remove()
                this._super.apply(this, arguments);

                if (this.controllerStack.length > 2) {
                    $('.split-screen-tree-viewer').remove()
                }

            } else {
                var size = $(window).width();
                if (size <= 1200) {
                    this.$el.removeClass('tree_form_split')
                    $('.o_list_view').attr('style','')
                    $('.tree-form-viewer').remove()
                    this._super.apply(this, arguments);

                    if (this.controllerStack.length > 2) {
                        $('.split-screen-tree-viewer').remove()
                    }
                } else {
                    $('#separator').remove()
                    $('.close_form_view').remove()
                    this.$el.addClass('tree_form_split')

                    $(this.$el.find('.o_action > .o_content > .o_list_view')[0]).after('<div id="separator" class="split_view_separator"></div>');
                    $(this.$el.find('.o_action > .o_content > .o_list_view')[0]).before('<div class="close_form_view">X</div>')
                    
                    $('.close_form_view').unbind().click(function(e) {
                        self._removeTreeFormView()
                    })

                    // this.controllerStack.push(controller.jsID);
                    this._appendController(controller, $(this.$el.find('.o_action > .o_content')[0]));

                    this.trigger_up('current_action_updated', {
                        action: this.getCurrentAction(),
                        controller: controller,
                    });
                    core.bus.trigger('close_dialogs');
                    this._toggleFullscreen();
                }
            }
        },

        _appendController: function(controller, custom_ele_=false) {
            if (custom_ele_ && custom_ele_.length) {
                dom.append(custom_ele_, controller.widget.$el, {
                    in_DOM: this.isInDOM,
                    callbacks: [{
                        widget: controller.widget
                    }],
                });
                var options = {
                    containment: 'parent',
                    helper: 'clone'
                }
                Object.assign(options, {
                    axis: 'x',
                    start: function(event, ui) {
                        $(this).attr('start_offset', $(this).offset().left);
                        $(this).attr('start_next_height', $(this).next().width());
                    },
                    drag: function(event, ui) {
                        var prev_element = $(this).prev();
                        prev_element.width(ui.offset.left - prev_element.offset().left);
                    }
                })
                $('#separator').draggable(options);
                $('#separator').on("dragstop", function(event, ui) {
                    $('.custom_seperator').css({
                        'opacity': '1'
                    })
                });
                if (controller.scrollPosition) {
                    this.trigger_up('scrollTo', controller.scrollPosition);
                }
                $('.tree_form_split > .o_view_controller > .o_content > #separator').addClass('tree-form-viewer')
                $('.tree_form_split > .o_view_controller > .o_content > .o_view_controller').addClass('tree-form-viewer')
                $('.tree_form_split > .o_view_controller > .o_content > .close_form_view').addClass('tree-form-viewer')
                $('.tree_form_split > .o_view_controller').addClass('split-screen-tree-viewer')
            } else {
                this._super.apply(this, arguments);
            }
        },

        _removeTreeFormView: function() {
            $('.tree_form_split > .o_view_controller > .o_content > #separator').remove()
            $('.tree_form_split > .o_view_controller > .o_content > .o_view_controller').remove()
            $('.tree_form_split > .o_view_controller > .o_content > .close_form_view').remove()
            $('.o_action_manager.tree_form_split').removeClass('tree_form_split')
            $('.o_list_view').attr('style','')
            $('.reload_view').click()
        },
    });
});