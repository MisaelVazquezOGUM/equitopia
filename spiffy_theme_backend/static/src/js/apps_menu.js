odoo.define('spiffy_theme_backend.appsMenuJs', function (require) {
    'use strict';

    var AppsMenu = require("web.AppsMenu");
    var core = require('web.core');
    var qweb = core.qweb;
    var ajax = require('web.ajax');

    function AppDrawerfindNames(memo, menu) {
        if (menu.action) {
            var key = menu.parent_id ? menu.parent_id[1] + "/" : "";
            memo[key + menu.name] = menu;
        }
        if (menu.children.length) {
            _.reduce(menu.children, AppDrawerfindNames, memo);
        }
        return memo;
    }

    // inherited this for app drawer and favourite apps
    var AppsMenuInherit = AppsMenu.include({
        events: _.extend({
            "keydown #app_menu_search": "_AppsearchResultsNavigate",
            'input #app_menu_search': '_searchAppDrawerTimeout',
            'click #search_result .search_list_content a': '_ToggleDrawer',
            'click .fav_app_select': '_AddRemoveFavApps',
        },AppsMenu.prototype.events),

        init: function (parent, menuData) {
            this._super.apply(this, arguments);
            this._searchableMenus = _.reduce(menuData.children, AppDrawerfindNames, {});
            this._search_def = false;
        },

        start: function () {
            this._super.apply(this, arguments);
            this._GetFavouriteApps()
            this._AppdrawerIcons()
            this._FavouriteAppsIsland()
            
            $('.favorite_apps_section').scroll(function(){
                if ($('.favorite_apps_section').scrollTop() > 20) {
                    $('.favorite_apps_section').css( { height: `calc(100vh - ${sidebar_systray_height}px)` } );
                } else {
                    $('.favorite_apps_section').css( { height: `calc(100vh - ${sidebar_systray_height}px)` } );
                }
            });
        },

        _ToggleDrawer: function (ev) {
            $('.o_main_navbar').toggleClass('appdrawer-toggle')
            $('.appdrawer_section').toggleClass('toggle')
            $('.o_app_drawer a').toggleClass('toggle')

            // reset app drawer search details on drawer close
            if (!$('.appdrawer_section').hasClass('toggle')) {
                $("input[id='app_menu_search']").val("")
                $(".appdrawer_section #search_result").empty()
                $('.appdrawer_section .apps-list .row').removeClass('d-none');
                $('#searched_main_apps').empty().addClass('d-none').removeClass('d-flex');
            }
        },

        _onAppsMenuItemClicked: function (ev){
            this._super.apply(this, arguments);
            this._ToggleDrawer()
        },

        _FavouriteAppsIsland: function (ev){
            ajax.rpc('/get-favorite-apps').then(function(rec) {
                if (rec.app_list.length) {
                    $('.fav_app_island .fav_apps').empty();
                    $.each(rec.app_list, function( index, value ) {
                        var app_name = value['name'].replace(/\s/g, '');
                        var favapps = $(qweb.render("FavoriteApps", {
                            app_name: app_name,
                            app_id: value['app_id'],
                            app_xmlid: value['app_xmlid'],
                            app_actionid: value['app_actionid'],
                            use_icon: value['use_icon'],
                            icon_class_name: value['icon_class_name'],
                            icon_img: value['icon_img'],
                        }))
                        $('.fav_app_island .fav_apps').append(favapps)
                    });
                    $('.fav_app_island').removeClass('d-none')
                } else {
                    $('.fav_app_island').addClass('d-none')
                }
            });
        },

        _GetFavouriteApps: function() {
            var apps = this._apps;
            ajax.rpc('/get-favorite-apps').then(function(rec) {
                if (rec) {
                    $.each(rec.app_list, function( index, value ) {
                        $.each(apps, function( ind, val ) {
                            if (value['app_id'] == val.menuID) {
                                var target = ".o_app[data-menu-id="+val.menuID+"]";
                                var $target = $(target);
                                $target.parent().find('.fav_app_select .ri').addClass('active');
                            }
                        });
                    });
                }
            });
        },

        get_user_data: function (ev) {
            var self = this
            var session = this.getSession();
            var $avatar = $('.user_image img');
            var avatar_src = session.url('/web/image', {
                model:'res.users',
                field: 'image_128',
                id: session.uid,
            });
            var current_time_hr = new Date().getHours().toLocaleString("en-US", { timeZone: session.user_context.tz });
            if (parseInt(current_time_hr) < 12){
                var greeting = "Good Morning"
            } else if ((parseInt(current_time_hr) >= 12) && parseInt(current_time_hr) <= 17) {
                var greeting = "Good Afternoon"
            } else if (parseInt(current_time_hr) >= 17){
                var greeting = "Good Evening"
            }
            var value = {
                'avatar_src': avatar_src,
                'user_id': session.uid,
                'user_name': session.name,
                'greeting': greeting,
            }
            $avatar.attr('src', avatar_src);
            return value
        },

        _AddRemoveFavApps: function (ev) {
            var self = this
            var app_id = $(ev.currentTarget).parent().find('.o_app').attr('data-menu-id')
            var app_name = $(ev.currentTarget).parent().find('.app-name').text()
            if ($(ev.currentTarget).find('.ri.active').length) {
                ajax.jsonRpc('/remove-user-fav-apps','call', {
                    'app_id':app_id,
                }).then(function(rec) {
                    $(ev.currentTarget).find('.ri').removeClass('active');
                    self._FavouriteAppsIsland()
                });
            } else {
                ajax.jsonRpc('/update-user-fav-apps','call', {
                    'app_name':app_name,
                    'app_id':app_id,
                }).then(function(rec) {
                    $(ev.currentTarget).find('.ri').addClass('active');
                    self._FavouriteAppsIsland()
                });
            }
        },

        _getsearchedapps: function(searchvals) {
            var self = this
            var apps = this._apps
            if (searchvals === "") {
                $('#searched_main_apps').empty().addClass('d-none').removeClass('d-flex');
                return;
            }
            $('#searched_main_apps').empty().addClass('d-flex').removeClass('d-none');
            $.each(apps, function( index, value ) {
                if(value['name'].toLowerCase().indexOf(searchvals.toLowerCase()) != -1){
                    var searchapps = $(qweb.render("SearchedApps", {
                        app_name:value['name'],
                        app_id:value['menuID'],
                        app_xmlid:value['xmlID'],
                        app_actionid:value['actionID'],
                    }))
                    if (value['use_icon']) {
                        if (value['icon_class_name']) {
                            var icon_span = "<span class='ri "+value['icon_class_name']+"'/>"
                            $(searchapps).find('.app-image').append($(icon_span))
                        } else if (value['icon_img']) {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value['id']+"/icon_img' />"
                            $(searchapps).find('.app-image').append($(icon_image))
                        } else {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value['id']+"/web_icon_data' />"
                            $(searchapps).find('.app-image').append($(icon_image))
                        }
                    } else {
                        if (value['icon_img']) {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value['id']+"/icon_img' />"
                            $(searchapps).find('.app-image').append($(icon_image))
                        } else {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+value['id']+"/web_icon_data' />"
                            $(searchapps).find('.app-image').append($(icon_image))
                        }
                    }
                    $('.apps-list #searched_main_apps').append(searchapps);
                }
            });
            this._GetFavouriteApps();
        },

        _AppsearchResultsNavigate: function(ev) {
            // Find current results and active element (1st by default)
            const all = $(".appdrawer_section #search_result").find(".search_list_content"),
                pre_focused = all.filter(".navigate_active") || $(all[0]);
            let offset = all.index(pre_focused),
                key = ev.key;
            // Keyboard navigation only supports search results
            if (!all.length) {
                return;
            }
            // Transform tab presses in arrow presses
            if (key === "Tab") {
                ev.preventDefault();
                key = ev.shiftKey ? "ArrowUp" : "ArrowDown";
            }
            switch (key) {
                // Pressing enter is the same as clicking on the active element
                case "Enter":
                    // $(pre_focused).find('.autoComplete_highlighted').click();
                    var target = $(pre_focused).find('.autoComplete_highlighted')
                    this.trigger_up('app_clicked', {
                        action_id: $(target).data('action-id'),
                        menu_id: $(target).data('menu-id'),
                    });
                    $('.o_app_drawer .appDrawerToggle').click();
                    break;
                // Navigate up or down
                case "ArrowUp":
                    offset--;
                    break;
                case "ArrowDown":
                    offset++;
                    break;
                default:
                    // Other keys are useless in this event
                    return;
            }
            // Allow looping on results
            if (offset < 0) {
                offset = all.length + offset;
            } else if (offset >= all.length) {
                offset -= all.length;
            }
            // Switch active element
            const new_focused = $(all[offset]);
            pre_focused.removeClass("navigate_active");
            new_focused.addClass("navigate_active");
            $(".appdrawer_section #search_result").scrollTo(new_focused, {
                offset: {
                    top: $(".appdrawer_section #search_result").height() * -0.5,
                },
            });
        },

        _menuInfo: function (key) {
            const original = this._searchableMenus[key];
            return _.extend(
                {
                    action_id: parseInt(original.action.split(",")[1], 10),
                },
                original
            );
        },

        _searchAppDrawerTimeout: function (ev) {
            this._search_def = new Promise((resolve) => {
                setTimeout(resolve, 100);
            });
            this._search_def.then(this._searchMenuItems.bind(this));
        },
       
        _searchMenuItems: function(){
            var searchvals = $("input[id='app_menu_search']").val()
            this._getsearchedapps(searchvals);
            $(".appdrawer_section .apps-list .row").toggleClass('d-none',Boolean(searchvals.length));
            if (searchvals === "") {
                $(".appdrawer_section #search_result").empty();
                $(".appdrawer_section #searched_main_apps").empty().removeClass('d-flex').addClass('d-none');
                return;
            }
            var results = fuzzy.filter(searchvals, _.keys(this._searchableMenus), {
                pre: "<b>",
                post: "</b>",
            });
            $(".appdrawer_section #search_result").html(
                core.qweb.render("spiffy_theme_backend.MenuSearchResults", {
                    results: results,
                    widget: this,
                })
            );
        },

        _AppdrawerIcons: function() {
            var self = this
            var apps = this._apps
            $.each(apps, function( key, value ) {
                ajax.jsonRpc('/get/irmenu/icondata','call', {
                    'menu_id':value.menuID,
                }).then(function(rec) {
                    var target_tag = '.appdrawer_section a.o_app[data-menu-id='+rec[0].id+']'
                    var $tagtarget = $(target_tag)
                    $tagtarget.find('.app-image').empty()

                    value.id = rec[0].id
                    value.use_icon = rec[0].use_icon
                    value.icon_class_name = rec[0].icon_class_name
                    value.icon_img = rec[0].icon_img

                    if (rec[0].use_icon) {
                        if (rec[0].icon_class_name) {
                            var icon_span = "<span class='ri "+rec[0].icon_class_name+"'/>"
                            $tagtarget.find('.app-image').append($(icon_span))
                        } else if (rec[0].icon_img) {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/icon_img' />"
                            $tagtarget.find('.app-image').append($(icon_image))
                        } else {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/web_icon_data' />"
                            $tagtarget.find('.app-image').append($(icon_image))
                        }
                    } else {
                        if (rec[0].icon_img) {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/icon_img' />"
                            $tagtarget.find('.app-image').append($(icon_image))
                        } else {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/web_icon_data' />"
                            $tagtarget.find('.app-image').append($(icon_image))
                        }
                    }
                })
            });
        },
    });
});