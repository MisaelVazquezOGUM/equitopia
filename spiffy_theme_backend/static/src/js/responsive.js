odoo.define("spiffy_theme_backend.responsive", function (require) {
    var AbstractController = require('web.AbstractController');
    var ajax = require('web.ajax');
    var concurrency = require('web.concurrency');
    var config = require('web.config');
    var core = require('web.core');
    var QWeb = core.qweb;

    AbstractController.include({
        /**
         * Renders the switch buttons and binds listeners on them.
         *
         * @private
         * @returns {jQuery}
         */
        _renderSwitchButtons: function () {
            var self = this;
            var views = _.filter(this.actionViews, {multiRecord: this.isMultiRecord});

            if (views.length <= 1) {
                return $();
            }

            var size = $(window).width();
            var upTo1200 = size <= 1200

            var template = upTo1200 ? 'ControlPanel.SwitchButtons.Mobile' : 'ControlPanel.SwitchButtons';
            var $switchButtons = $(QWeb.render(template, {
                viewType: this.viewType,
                views: views,
            }));
            // create bootstrap tooltips
            _.each(views, function (view) {
                $switchButtons.filter('.o_cp_switch_' + view.type).tooltip();
            });
            // add onclick event listener
            var $switchButtonsFiltered = upTo1200 ? $switchButtons.find('button') : $switchButtons.filter('button');
            $switchButtonsFiltered.click(_.debounce(function (event) {
                var viewType = $(event.target).data('view-type');
                self.trigger_up('switch_view', {view_type: viewType});
            }, 200, true));

            // set active view's icon as view switcher button's icon in mobile
            if (upTo1200) {
                var activeView = _.findWhere(views, {type: this.viewType});
                $switchButtons.find('.o_switch_view_button_icon').addClass('fa fa-lg ' + activeView.icon);
            }

            return $switchButtons;
        },
    });
});