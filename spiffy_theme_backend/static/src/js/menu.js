odoo.define('spiffy_theme_backend.MenuJs', function (require) {
    'use strict';

    var Menu = require("web.Menu");
    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var ColorPallet = require('spiffy_theme_backend.ColorPalletJS')
    var config = require('web.config');

    function findNames(memo, menu) {
        if (menu.action) {
            var key = menu.parent_id ? menu.parent_id[1] + "/" : "";
            memo[key + menu.name] = menu;
        }
        if (menu.children.length) {
            _.reduce(menu.children, findNames, memo);
        }
        return memo;
    }

    var NewMenu = Menu.include({
        events: _.extend({
            'click .bookmark_section .dropdown-toggle': '_getCurrentPageName',
            'click .bookmark_section .add_bookmark': '_saveBookmarkPage',
            'contextmenu .bookmark_list .bookmark_tag': '_showbookmarkoptions',
            'click .magnifier_section .minus': '_magnifierZoomOut',
            'click .magnifier_section .plus': '_magnifierZoomIn',
            'click .magnifier_section .reset': '_magnifierZoomReset',
            'click .fullscreen_section > a.full_screen': '_FullScreenMode',
            'click .theme_selector > a': '_openConfigModal',
            'click #dark_mod': '_ChangeThemeModeCLicked',
            'click .pin_sidebar': '_ChangeSidebarBehaviour',
            // 'click .lang_selector': '_GetLanguages',

            'click .o_menu_apps .main_link': '_ShowCurrentMenus',
            'click .o_menu_apps .child_menus': '_ClickChildMenu',
            'click .search_bar, .close-search-bar': '_showSearchbarModal',
            "shown.bs.modal #search_bar_modal": "_searchModalFocus",
            "hidden.bs.modal #search_bar_modal": "_searchModalReset",

            "keydown #searchPagesInput": "_searchResultsNavigate",
            'input #searchPagesInput': '_searchMenuTimeout',
            "click #searchPagesResults .autoComplete_highlighted": "_searchResultChosen",

            'click .o_app_drawer a': '_OpenAppdrawer',
            'click .mobile-header-toggle #mobileMenuToggleBtn': '_mobileHeaderToggle',
            'click .o_menu_sections #mobileMenuclose': '_mobileHeaderClose',
            'click .fav_app_drawer .fav_app_drawer_btn': '_OpenFavAppdrawer',
            'click .appdrawer_section .close_fav_app_btn': '_CloseAppdrawer',

            'click .debug_activator .activate_debug': '_DebugToggler',
            
        },Menu.prototype.events),

        init: function (parent, menuData) {
            this._super.apply(this, arguments);
            this._searchableMenus = _.reduce(menuData.children, findNames, {});
            this._search_def = false;
        },

        start: function () {
            this._super.apply(this, arguments);
            // on reload get mode color
            this._getModeData();
            // on reload add backend theme class
            this.addconfiguratorclass()
            // on reload add bookmark tags in menu
            this.addbookmarktags()
            // get all apps menu data
            this._all_apps_menu_data()
            this._GetLanguages()

            this.$search_modal_popup = this.$("#search_bar_modal");
            this.$search_modal_input = this.$("#search_bar_modal input");
            this.$search_modal_select = this.$("#search_bar_modal select");
            this.$search_modal_results = this.$("#search_bar_modal #searchPagesResults");
            this.$search_modal_Noresults = this.$("#search_bar_modal .searchNoResult");

            //company logo
            var session = this.getSession();
            var company_logo_src = session.url('/web/image', {
                model:'res.company',
                field: 'backend_menubar_logo',
                id: session.company_id,
            });
            var company_logo_icon_src = session.url('/web/image', {
                model:'res.company',
                field: 'backend_menubar_logo_icon',
                id: session.company_id,
            });
            var company_logo = "<img class='img img-fluid company_logo' src='"+company_logo_src+"'/>"
            var company_logo_icon = "<img class='img img-fluid company_logo_icon d-none' src='"+company_logo_icon_src+"'/>"
            $('.o_company_logo').append(company_logo)
            $('.o_company_logo').append(company_logo_icon)

            ajax.rpc('/get/model/record').then(function(data) {
                if (!data.show_edit_mode){
                    self.$el.find('.theme_selector').remove()
                }
                if (!data.is_admin) {
                    self.$el.find('.debug_activator').remove()
                }
                var pallet_name = data.record_dict[0].color_pallet
                var apply_color = new ColorPallet(this)
                if (data.record_dict[0].use_custom_colors) {
                    apply_color['custom_color_pallet'](data.record_dict[0])
                } else {
                    apply_color[pallet_name]()
                }

                var app_drawer_pallet_name = data.record_dict[0].drawer_color_pallet
                var app_drawer_apply_color = new ColorPallet(this)
                if (data.record_dict[0].use_custom_drawer_color) {
                    app_drawer_apply_color['custom_app_drawer_color_pallet'](data.record_dict[0])
                }
                $('.o_main_navbar').removeClass('d-none');
            });
            
            // close magnifier when clicked outside the magnifer div
            $(document).on("click", function(e) {
			    if (!$(e.target).closest('.magnifier_section').length) {
                    $('#magnifier').collapse("hide")
			    }
		  	});

            /* EVENTS FOR WINDOW FULLSCREEN WITH ESC BUTTON TRIGGER */
            document.addEventListener("fullscreenchange", function() {
                if (!document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement){
                    var fullScreenBtn = $('.fullscreen_section .full_screen');
                    if($(fullScreenBtn).hasClass('fullscreen-exit')){
                        $(fullScreenBtn).removeClass('fullscreen-exit')
                    }
                }
            });
            document.addEventListener("mozfullscreenchange", function() {
                if (!document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement){
                    var fullScreenBtn = $('.fullscreen_section .full_screen');
                    if($(fullScreenBtn).hasClass('fullscreen-exit')){
                        $(fullScreenBtn).removeClass('fullscreen-exit')
                    }
                }
            });
            document.addEventListener("webkitfullscreenchange", function() {
                if (!document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement){
                    var fullScreenBtn = $('.fullscreen_section .full_screen');
                    if($(fullScreenBtn).hasClass('fullscreen-exit')){
                        $(fullScreenBtn).removeClass('fullscreen-exit')
                    }
                }
            });
            document.addEventListener("msfullscreenchange", function() {
                if (!document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement){
                    var fullScreenBtn = $('.fullscreen_section .full_screen');
                    if($(fullScreenBtn).hasClass('fullscreen-exit')){
                        $(fullScreenBtn).removeClass('fullscreen-exit')
                    }
                }
            });
            
        },

        _DebugToggler: function (ev) {
            $(ev.currentTarget).toggleClass('toggle');
            if ($(ev.currentTarget).hasClass('toggle')) {
                var current_href = window.location.href;
                window.location.search = "?debug=1"
            } else {
                window.location.search = "?debug="
            }
        },

        _on_secondary_menu_click: function (menu_id, action_id) {
            this._super.apply(this, arguments);
            $('.o_menu_sections').removeClass('toggle');
            $('body').removeClass('backdrop');
        },

        _mobileHeaderToggle: function (ev) {
            var menu_brand = $('.o_main_navbar > a.o_menu_brand').clone()
            $('.o_menu_sections > a.o_menu_brand').remove()
            $('#mobileMenuclose').before(menu_brand)
            $('.o_menu_sections').addClass('toggle');
            $('body').addClass('backdrop');
        },

        _mobileHeaderClose: function (ev) {
            $('.o_menu_sections').removeClass('toggle');
            $('body').removeClass('backdrop');
        },

        _OpenAppdrawer: function (ev) {
            $('.o_main_navbar').toggleClass('appdrawer-toggle')
            $('.appdrawer_section').toggleClass('toggle')

            if ($(".appdrawer_section").hasClass('toggle')) {
                var size = $(window).width();
                if (size > 992){
                    setTimeout(() => $(".appdrawer_section input").focus(), 100);
                }
            } else {
                $(".appdrawer_section input").val("");
                $(".appdrawer_section #search_result").empty();
                $('#searched_main_apps').empty().addClass('d-none').removeClass('d-flex');
                $('.appdrawer_section .apps-list .row').removeClass('d-none');
            }
        },

        _OpenFavAppdrawer: function (ev) {
            this._OpenAppdrawer(ev)
            $('.appdrawer_section').toggleClass('show_favourite_apps')
        },

        _CloseAppdrawer: function (ev) {
            $('.o_main_navbar').removeClass('appdrawer-toggle')
            $('.appdrawer_section').removeClass('show_favourite_apps')
            $('.appdrawer_section').removeClass('toggle')
            $(".appdrawer_section input").val("");
            $(".appdrawer_section #search_result").empty();
            $('#searched_main_apps').empty().addClass('d-none').removeClass('d-flex');
            $('.appdrawer_section .apps-list .row').removeClass('d-none');
        },

        _all_apps_menu_data: function () {
            var menu_data = this.menu_data
            var session = this.getSession();
            var allappsmenu = $(qweb.render("AllAppsMenus", {
                menu_data:menu_data,
            }))
            $('.o_menu_apps').append(allappsmenu)

            $.each(menu_data.children, function( key, value ) {
                ajax.jsonRpc('/get/irmenu/icondata','call', {
                    'menu_id':value.id,
                }).then(function(rec) {
                    var target_tag = '.o_menu_apps a.main_link[data-menu='+rec[0].id+']'
                    var $tagtarget = $(target_tag)

                    if (rec[0].use_icon) {
                        if (rec[0].icon_class_name) {
                            var icon_span = "<span class='ri "+rec[0].icon_class_name+"'/>"
                            $tagtarget.find('.app_icon').append($(icon_span))
                        } else if (rec[0].icon_img) {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/icon_img' />"
                            $tagtarget.find('.app_icon').append($(icon_image))
                        } else {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/web_icon_data' />"
                            $tagtarget.find('.app_icon').append($(icon_image))
                        }
                    } else {
                        if (rec[0].icon_img) {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/icon_img' />"
                            $tagtarget.find('.app_icon').append($(icon_image))
                        } else {
                            var icon_image = "<img class='img img-fluid' src='/web/image/ir.ui.menu/"+rec[0].id+"/web_icon_data' />"
                            $tagtarget.find('.app_icon').append($(icon_image))
                        }
                    }
                });
            })
            var selectorActiveMenu = $(qweb.render("seletor-acvtive-menu-items", {
                menu_data:menu_data.children,
            }))
            $(".load-active-menu-selector").append(selectorActiveMenu)
        },

        _ShowCurrentMenus: function (ev) {
            $(ev.currentTarget).parent().parent().find('ul').removeClass('show')
            $(ev.currentTarget).parent().parent().find('a.main_link').removeClass('active')
            $(ev.currentTarget).parent().find('ul').addClass('show')
        },

        _ClickChildMenu: function (ev) {
            var data_menu = $(ev.currentTarget).attr('data-menu')
            $(ev.currentTarget).parents('#accordion').find('.child_menus').removeClass('active')
            $(ev.currentTarget).addClass('active')
            var target_tag = '.o_menu_sections a[data-menu='+data_menu+']'
            var $tagtarget = $(target_tag)
            $(ev.currentTarget).parents('.o_main_navbar').find(target_tag).click()
            if (!$('#mobileMenuclose').hasClass('d-none')) {
                $('#mobileMenuclose').click();
            }
        },

        change_menu_section: function (primary_menu_id) {
            this._super.apply(this, arguments);
            var target_tag = '.o_menu_apps a.main_link[data-menu='+primary_menu_id+']'
            var $tagtarget = $(target_tag)
            $tagtarget.parent().find('ul').addClass('show')
            $tagtarget.addClass('active')
        },

        _getModeData: function() {
            var self = this
            ajax.rpc('/get/dark/mode/data').then(function(rec) {
                var dark_mode = rec
                self._ChangeThemeMode(dark_mode)
            })
        },
        addconfiguratorclass: function (){
            ajax.rpc('/get/model/record').then(function(rec) {
                $("body").addClass(rec.record_dict[0].separator);
                $("body").addClass(rec.record_dict[0].tab);
                $("body").addClass(rec.record_dict[0].checkbox);
                $("body").addClass(rec.record_dict[0].button);
                $("body").addClass(rec.record_dict[0].radio);
                $("body").addClass(rec.record_dict[0].popup);
                $("body").addClass(rec.record_dict[0].font_size);
                $("body").addClass(rec.record_dict[0].chatter_position);

                // Load Font size file based on selected option
                if(rec.record_dict[0].font_size){
                    ajax.loadCSS(`/spiffy_theme_backend/static/src/scss/font_sizes/${rec.record_dict[0].font_size}.css`);
                }

                var size = $(window).width();
                if (size <= 992){
                    $("body").addClass('top_menu_horizontal');
                    $("html").attr('data-menu-position','top_menu_horizontal')
                    $("html").attr('data-view-type','mobile')
                } else {
                    $("body").addClass(rec.record_dict[0].top_menu_position);
                    $("html").attr('data-menu-position',rec.record_dict[0].top_menu_position)
                    $("html").attr('data-view-type','desktop')
                }

                $("body").addClass(rec.record_dict[0].theme_style);
                $("body").addClass(rec.record_dict[0].loader_style);
                $("body").addClass('font_family_'+rec.record_dict[0].font_family);

                $("html").attr('data-font-size',rec.record_dict[0].font_size)
                $("html").attr('data-theme-style',rec.record_dict[0].theme_style)
                
                if (rec.record_dict[0].use_custom_drawer_color) {
                    $("body").addClass('custom_drawer_color');
                } else {
                    $("body").addClass(rec.record_dict[0].drawer_color_pallet);
                }
                
                if (rec.record_dict[0].attachment_in_tree_view) {
                    $("body").addClass("show_attachment");
                }
                if (rec.darkmode) {
                    $("body").addClass(rec.darkmode);
                }
                if (rec.pinned_sidebar) {
                    $("body").addClass(rec.pinned_sidebar);
                    $("header .pin_sidebar").addClass('pinned');
                }
                if (rec.record_dict[0].tree_form_split_view) {
                    $("body").addClass("tree_form_split_view");
                }
                if (rec.record_dict[0].apply_light_bg_img){
                    if (rec.record_dict[0].light_bg_image){
                        $(".appdrawer_section").attr("style", "background-image: url('/web/image/backend.config/"+rec.record_dict[0].id+"/light_bg_image')");
                    }
                }
            })
        },

        addbookmarktags: function(){
            ajax.jsonRpc('/get/bookmark/link','call', {
            }).then(function(rec) {
                $('.bookmark_list').empty()
                $.each(rec, function( key, value ) {
                    var anchor_tag = '<div class="d-inline-block bookmark_div"><a href="'+ value.url +'"'+' class="bookmark_tag btn-light btn demo_btn" bookmark-id="'+value.id+'" bookmark-name="'+value.name+'" title="'+value.name+'">'+value.title+'</a></div>'
                    $('.bookmark_list').append(anchor_tag)
                })
            });
        },

        _getCurrentPageName: function(){
            var breadcrumbs = $('.o_control_panel ol.breadcrumb li')
            var bookmark_name = ""
            $(breadcrumbs).each(function( index ) {
                if (index > 0) {
                    bookmark_name = bookmark_name + ' | ' + $(this).text()
                } else {
                    bookmark_name = $(this).text()
                }
            });

            $('input#bookmark_page_name').val(bookmark_name)
        },

        _saveBookmarkPage: function(){
            var self = this
            var pathname = window.location.pathname
            var hash = window.location.hash
            var url = pathname + '?' + hash
            var name = $('input#bookmark_page_name').val()
            var title = $('input#bookmark_page_name').val().substr(0, 2)
            ajax.jsonRpc('/add/bookmark/link','call', {
                'name':name,
                'url':url,
                'title':title,
            }).then(function(rec) {
                self.addbookmarktags()
            });
        },

        _showbookmarkoptions: function(ev) {
            var self = this
            var bookmark_id = $(ev.currentTarget).attr('bookmark-id')
            var bookmark_name = $(ev.currentTarget).attr('bookmark-name')
            $('.bookmark_list .bookmark_options').remove()
            $('.bookmark_list .bookmark_rename_section').remove()
            var bookmark_options = $(qweb.render("BookmarkOptions", {
                bookmark_id:bookmark_id,
            }))
            $(ev.currentTarget).parent().append(bookmark_options)
            $('.bookmark_list .rename_bookmark').on("click", function(e) {
                self._RenameBookmark(ev.currentTarget,bookmark_id,bookmark_name);
            });

            $('.bookmark_list .remove_bookmark').on("click", function(e) {
                self._RemoveBookmark(bookmark_id);
            });
            document.addEventListener("click", function(){
                $('.bookmark_list .bookmark_options').remove()
            });
            ev.preventDefault();
        },

        _RenameBookmark: function(elem,bookmark_id,bookmark_name) {
            var self = this
            var bookmark_rename = $(qweb.render("BookmarkRename", {
                bookmark_id:bookmark_id,
                bookmark_name:bookmark_name,
            }))
            $(elem).parent().append(bookmark_rename)

            $('.bookmark_list .bookmark_rename_cancel').on("click", function(e) {
                $('.bookmark_list .bookmark_rename_section').remove()
            });
            $('.bookmark_list .bookmark_rename').on("click", function(e) {
                var new_bookmark_name = $('input#bookmark_rename').val()
                self._UpdateBookmark(bookmark_id,new_bookmark_name);
            });
        },

        _RemoveBookmark: function(bookmark_id) {
            var self = this
            ajax.jsonRpc('/remove/bookmark/link','call', {
                'bookmark_id':bookmark_id,
            }).then(function(rec) {
                self.addbookmarktags()
            });
        },

        _UpdateBookmark: function(bookmark_id,bookmark_name) {
            var self = this
            var title = bookmark_name.substr(0, 2)
            ajax.jsonRpc('/update/bookmark/link','call', {
                'bookmark_id':bookmark_id,
                'bookmark_name':bookmark_name,
                'bookmark_title':title,
            }).then(function(rec) {
                self.addbookmarktags()
            });
        },

        _magnifierZoomOut: function(){
            var current_zoom = parseInt($('.zoom_value').text())
            var current_zoom = current_zoom - 10
            if (current_zoom > 20) {
                $('.zoom_value').text(current_zoom)
                var scale_value = current_zoom/100
                var width_value = ((100/current_zoom)*100).toFixed(4)
                if ($('.o_content > div').length > 1) {
                    var target = $('.o_action_manager > .o_view_controller > .o_content')
                } else {
                    var target = $('.o_content > div')
                }
                $(target).css({
                    'width': width_value+'%',
                    'transform-origin': 'left top',
                    'transform': 'scale('+scale_value+')',
                })
            }
        },

        _magnifierZoomIn: function(){
            var current_zoom = parseInt($('.zoom_value').text())
            var current_zoom = current_zoom + 10
            if (current_zoom < 210) {
                $('.zoom_value').text(current_zoom)
                var scale_value = current_zoom/100
                var width_value = ((100/current_zoom)*100).toFixed(4)
                if ($('.o_content > div').length > 1) {
                    var target = $('.o_action_manager > .o_view_controller > .o_content')
                } else {
                    var target = $('.o_content > div')
                }
                $(target).css({
                    'width': width_value+'%',
                    'transform-origin': 'left top',
                    'transform': 'scale('+scale_value+')',
                })
            }
        },

        _magnifierZoomReset: function(){
            $('.zoom_value').text('100')
            if ($('.o_content > div').length > 1) {
                var target = $('.o_action_manager > .o_view_controller > .o_content')
            } else {
                var target = $('.o_content > div')
            }
            $(target).css({
                'width': '100%',
                'transform-origin': 'left top',
                'transform': 'scale(1)',
            })
        },

        _FullScreenMode: function(ev) {
            var elem = document.documentElement;
            if ($(ev.currentTarget).hasClass('fullscreen-exit')) {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                    $(ev.currentTarget).removeClass('fullscreen-exit')
                } else if (document.webkitExitFullscreen) { /* Safari */
                    document.webkitExitFullscreen();
                    $(ev.currentTarget).removeClass('fullscreen-exit')
                } else if (document.msExitFullscreen) { /* IE11 */
                    document.msExitFullscreen();
                    $(ev.currentTarget).removeClass('fullscreen-exit')
                }
            } else {
                if (elem.requestFullscreen) {
                    elem.requestFullscreen();
                    $(ev.currentTarget).addClass('fullscreen-exit')
                } else if (elem.webkitRequestFullscreen) { /* Safari */
                    elem.webkitRequestFullscreen();
                    $(ev.currentTarget).addClass('fullscreen-exit')
                } else if (elem.msRequestFullscreen) { /* IE11 */
                    elem.msRequestFullscreen();
                    $(ev.currentTarget).addClass('fullscreen-exit')
                }
            }
        },

        _openConfigModal: function() {
            var self = this
            self.showeditmodal();
            $('.dynamic_data').toggleClass('visible')
            $('body.o_web_client').toggleClass('backdrop')
        },
        showeditmodal: function (ev) {
            $.get('/color/pallet/data/', 'call', {}).then(function(data) {
          
                $(".dynamic_data").empty()
                $(".dynamic_data").append(data)

                $('#theme_color_pallets #use_custom_color_config').unbind().on('change', function(e) {
                    if($(this).prop("checked") == true){
                        $('#theme_color_pallets .custom_color_config').removeClass('d-none')
                        $('#theme_color_pallets .predefined_color_pallets').addClass('d-none')
                    } else {
                        $('#theme_color_pallets .custom_color_config').addClass('d-none')
                        $('#theme_color_pallets .predefined_color_pallets').removeClass('d-none')
                    }
                });

                $('#app_drawer #use_custom_drawer_color').unbind().on('change', function(e) {
                    if($(this).prop("checked") == true){
                        $('#app_drawer .custom_color_config').removeClass('d-none')
                        $('#app_drawer .predefined_color_pallets').addClass('d-none')
                    } else {
                        $('#app_drawer .custom_color_config').addClass('d-none')
                        $('#app_drawer .predefined_color_pallets').removeClass('d-none')
                    }
                });

                $('#app_drawer #apply_light_bg').unbind().on('change', function(e) {
                    if($(this).prop("checked") == true){
                        $('#app_drawer .app-drawer-bg-image-content').removeClass('d-none')
                    } else {
                        $('#app_drawer .app-drawer-bg-image-content').addClass('d-none')
                    }
                });

                $('.app_bg_img_light').unbind().on('change', function(e) {
                    var upload_image = document.querySelector('#light_bg_image').files[0];
                        var reader1 = new FileReader();
                        var bg_data = reader1.readAsDataURL(upload_image);
                        reader1.onload = function(e){
                        var selected_bg_image = e.target.result;
                        window.app_light_bg_image =  selected_bg_image
                    }
                    var fileName = $(this).val().split("\\").pop();
                    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
                });

                $('#separator').unbind().on('change', function(){
                    $("#theme_separator_style .preview").removeClass("separator_style_4 separator_style_3 separator_style_2 separator_style_1");
                    var current_separator_style = $('#separator').val()
                    $("#theme_separator_style .preview").addClass(current_separator_style);
                });

                $('#tab').unbind().on('change', function(){
                    $("#theme_tab_style .preview").removeClass("tab_style_4 tab_style_3 tab_style_2 tab_style_1");
                    var current_tab_style = $('#tab').val()
                    $("#theme_tab_style .preview").addClass(current_tab_style);
                });

                $('#checkbox').unbind().on('change', function(){
                    $("#theme_checkbox_style .preview").removeClass("checkbox_style_4 checkbox_style_3 checkbox_style_2 checkbox_style_1");
                    var current_checkbox_style = $('#checkbox').val()
                    $("#theme_checkbox_style .preview").addClass(current_checkbox_style);
                });

                $('#radio').unbind().on('change', function(){
                    $("#theme_radio_style .preview").removeClass("radio_style_4 radio_style_3 radio_style_2 radio_style_1");
                    var current_radio_style = $('#radio').val()
                    $("#theme_radio_style .preview").addClass(current_radio_style);
                });
                $('#button').unbind().on('change', function(){
                    $("#theme_buttons_style .preview").removeClass("button_style_4 button_style_3 button_style_2 button_style_1");
                    var current_button_style = $('#button').val()
                    $("#theme_buttons_style .preview").addClass(current_button_style);
                });

                $('#popup').unbind().on('change', function(){
                    $("#theme_popup_style .preview").removeClass("popup_style_4 popup_style_3 popup_style_2 popup_style_1");
                    var current_popup_style = $('#popup').val()
                    $("#theme_popup_style .preview").addClass(current_popup_style);
                });

                $(".selected_value").on('click', function(){
                    var light_primary_bg_color = $("input[id='primary_bg']").val()
                    var light_primary_text_color = $("input[id='primary_text']").val()
                    var custom_color_pallet = $("input[id='use_custom_color_config']").is(':checked')
                    var selected_color_pallet = $("input[name='color_pallets']:checked").val()
                    var custom_drawer_bg = $("input[id='custom_drawer_bg']").val()
                    var custom_drawer_text = $("input[id='custom_drawer_text']").val()
                    var custom_drawer_color_pallet = $("input[id='use_custom_drawer_color']").is(':checked')
                    var selected_drawer_color_pallet = $("input[name='drawer_color_pallets']:checked").val()
                    var apply_light_bg_img = $("input[id='apply_light_bg']").is(':checked')
                    var tree_form_split_view = $("input[id='tree_form_split_view']").is(':checked')
                    var attachment_in_tree_view = $("input[id='attachment_in_tree_view']").is(':checked')

                    if (window.app_light_bg_image) {
                        var app_light_bg_img = window.app_light_bg_image
                    } else if ($("input[id='light_bg_image']").attr('value')){
                        var app_light_bg_img = $("input[id='light_bg_image']").attr('value')
                    }
                    else {
                        var app_light_bg_img = false
                    }

                    var selected_separator = $("input[name='separator']:checked").val()
                    var selected_tab = $("input[name='tab']:checked").val()
                    var selected_checkbox = $("input[name='checkbox']:checked").val()
                    var selected_radio = $("input[name='radio']:checked").val()
                    var selected_popup = $("input[name='popup']:checked").val()
                    var selected_loader = $("input[name='loader_style']:checked").val()
                    var selected_fonts = $("input[name='font_family']:checked").val()
                    var selected_fontsize = $("input[name='font_size']:checked").val()
                    var selected_chatter_position = $("input[name='chatter_position']:checked").val()
                    var selected_top_menu_position = $("input[name='top_menu_position']:checked").val()
                    var selected_theme_style = $("input[name='theme_style']:checked").val()
                    
                    ajax.rpc('/color/pallet/', {
                        'light_primary_bg_color': light_primary_bg_color,
                        'light_primary_text_color': light_primary_text_color,
                        'apply_light_bg_img': apply_light_bg_img,
                        'app_light_bg_image': app_light_bg_img,
                        'tree_form_split_view': tree_form_split_view,
                        'attachment_in_tree_view': attachment_in_tree_view,
                        'selected_separator':selected_separator,
                        'selected_tab':selected_tab,
                        'selected_checkbox':selected_checkbox,
                        'selected_radio': selected_radio,
                        'selected_popup': selected_popup,
                        'custom_color_pallet': custom_color_pallet,
                        'selected_color_pallet': selected_color_pallet,
                        'custom_drawer_bg': custom_drawer_bg,
                        'custom_drawer_text': custom_drawer_text,
                        'custom_drawer_color_pallet': custom_drawer_color_pallet,
                        'selected_drawer_color_pallet': selected_drawer_color_pallet,
                        'selected_loader': selected_loader,
                        'selected_fonts': selected_fonts,
                        'selected_fontsize': selected_fontsize,
                        'selected_chatter_position': selected_chatter_position,
                        'selected_top_menu_position': selected_top_menu_position,
                        'selected_theme_style': selected_theme_style,

                    }).then(function (data) {
                        window.location.reload()
                    })
                });
                $('.backend_configurator_close').unbind().click(function(e) {
                    $('.dynamic_data').toggleClass('visible')
                    $('body.o_web_client').toggleClass('backdrop')
                });
            })
            $('#myModal').modal("show")
        },

        _ChangeThemeModeCLicked :function (ev) {
            $('body').toggleClass('dark_mode')
            if ($('body').hasClass('dark_mode')) {
                var darkmode = true 
            } else {
                var darkmode = false 
            }
            this._ChangeThemeMode(darkmode)
         },

        _ChangeThemeMode: function (darkmode) {
            if (darkmode){
                ajax.rpc('/active/dark/mode', {'dark_mode': 'on'})
                    .then(function(data){
                        if (data){
                        }
                })
                $('body').addClass('dark_mode')
                $(':root').css('--biz-theme-primary-color','var(--dark-theme-primary-color)');
                $(':root').css('--biz-theme-primary-text-color','var(--dark-theme-primary-text-color)');
                $(':root').css('--biz-theme-secondary-color','var(--dark-theme-secondary-color)');
                $(':root').css('--biz-theme-secondary-text-color','var(--dark-theme-secondary-text-color)');
                $(':root').css('--biz-theme-body-color','var(--dark-theme-body-color)');
                $(':root').css('--biz-theme-body-text-color','var(--dark-theme-body-text-color)');
                $(':root').css('--biz-theme-primary-rgba','var(--primary-rgba)');
            }
            else{
                ajax.rpc('/active/dark/mode', {'dark_mode': 'off'})
                    .then(function(data){
                        if (data){
                        }
                })
                $('body').removeClass('dark_mode')
                $(':root').css('--biz-theme-primary-color','var(--light-theme-primary-color)');
                $(':root').css('--biz-theme-primary-text-color','var(--light-theme-primary-text-color)');
                $(':root').css('--biz-theme-secondary-color','var(--light-theme-secondary-color)');
                $(':root').css('--biz-theme-secondary-text-color','var(--light-theme-secondary-text-color)');
                $(':root').css('--biz-theme-body-color','var(--light-theme-body-color)');
                $(':root').css('--biz-theme-body-text-color','var(--light-theme-body-text-color)');
                $(':root').css('--biz-theme-primary-rgba','var(--primary-rgba)');
            }
        },

        _ChangeSidebarBehaviour: function (ev) {
            $(ev.currentTarget).toggleClass('pinned')
            $('body').toggleClass('pinned')
            if ($(ev.currentTarget).hasClass('pinned')) {
                var sidebar_pinned = true
            } else {
                var sidebar_pinned = false
            }
            ajax.rpc('/sidebar/behavior/update', {
                'sidebar_pinned': sidebar_pinned,
            }).then(function(data){
                if (data){
                }
            })
        },

        _GetLanguages: function() {
            var self = this
            var session = this.getSession();
            ajax.rpc('/get/active/lang').then(function(data){
                var lang_list = data
               if (data && data.length > 1){
                   $('.active_lang').empty()
                   $.each(lang_list, function( index, value ) {
                       var searchedlang = $(qweb.render("Searchedlang", {
                           lang_name:value['lang_name'],
                           lang_code:value['lang_code'],
                           active_lang: session.user_context.lang
                       }))
                       $('.active_lang').append(searchedlang)
                       $('.biz_lang_btn').unbind().on('click', function(ev){
                           var lang = $(ev.currentTarget)[0].lang
                           self.LangSelect(lang)
                       })
                   });
                   $('.o_user_lang').removeClass('d-none')
               }
               else {
                   $('.o_user_lang').addClass('d-none')
               }
            })
        },
        
        LangSelect: function (lang) {
            var self = this;
            var session = this.getSession();
            var user_id = session.uid
            return self._rpc({
                model: 'res.users',
                method: 'write',
                args: [user_id, {'lang': lang}],
            }).then(function (result) {
                self.do_action({
                    type: 'ir.actions.client',
                    res_model: 'res.users',
                    tag: 'reload_context',
                    target: 'current',
                });
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

        _searchModalFocus: function () {
            if (!config.device.isMobile) {
                // This timeout is necessary since the menu has a 100ms fading animation
                setTimeout(() => this.$search_modal_input.focus(), 100);
            }
        },
        _searchModalReset: function () {
            this.$search_modal_results.empty();
            this.$search_modal_input.val("");
            this.$search_modal_select.val("all");
        },

        _showSearchbarModal: function(ev){
            if (!this.$search_modal_popup.hasClass('show')){
                this.$search_modal_popup.modal({keyboard: false});
                this.$search_modal_popup.modal('show');
            } else {
                this.$search_modal_popup.modal('hide');
            }
        },

        _searchResultChosen: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            const $result = $(ev.currentTarget),
                text = $result.text().trim(),
                data = $result.data(),
                suffix = ~text.indexOf("/") ? "/" : "";
            // Load the menu view
            this.trigger_up("menu_clicked", {
                action_id: data.actionId,
                id: data.menuId,
                previous_menu_id: data.parentId,
            });
            this.$search_modal_popup.modal('hide');

            // Find app that owns the chosen menu
            const app = _.find(this._apps, function (_app) {
                return text.indexOf(_app.name + suffix) === 0;
            });

            // NOTE: Need to check below trigger_up because app.menuId is not found!
            // Update navbar menus
            // core.bus.trigger("change_menu_section", app.menuID);
        },

        _searchResultsNavigate: function(ev) {
            const all = this.$search_modal_results.find(".search_list_content"),
                pre_focused = all.filter(".navigate_active") || $(all[0]);
            let offset = all.index(pre_focused),
                key = ev.key;
            if (!all.length) {
                return;
            }
            if (key === "Tab") {
                ev.preventDefault();
                key = ev.shiftKey ? "ArrowUp" : "ArrowDown";
            }
            switch (key) {
                case "Enter":
                    $(pre_focused).find('.autoComplete_highlighted').click();
                    // this.$search_modal_popup.modal('hide');
                    break;
                case "ArrowUp":
                    offset--;
                    break;
                case "ArrowDown":
                    offset++;
                    break;
                default:
                    return;
            }
            if (offset < 0) {
                offset = all.length + offset;
            } else if (offset >= all.length) {
                offset -= all.length;
            }
            const new_focused = $(all[offset]);
            pre_focused.removeClass("navigate_active");
            new_focused.addClass("navigate_active");
            this.$search_modal_results.scrollTo(new_focused, {
                offset: {
                    top: this.$search_modal_results.height() * -0.5,
                },
            });
        },

        _searchMenuTimeout: function (ev) {
            this._search_def = new Promise((resolve) => {
                setTimeout(resolve, 50);
            });
            this._search_def.then(this._searchPages.bind(this));
        },

        _searchPages: function(){
            const searchvals = this.$search_modal_input.val();
            if (searchvals === "") {
                this.$search_modal_results.empty();
                this.$search_modal_Noresults.toggleClass('d-none', true);
                return;
            }
            var $selected_search_mainmenu_name = this.$search_modal_select.children(":selected").attr("value").toLowerCase();
            var self = this;
            this._searchableMenus = _.reduce(this.menu_data.children, findNames, {});
            if ($selected_search_mainmenu_name != 'all'){
                $.each(self._searchableMenus, function( key, value ) {
                    var key_split = key.split("/");
                    var key_name = key_split[0].toLowerCase();
                    if (value['parent_id'][1]){
                        if (key_name.indexOf($selected_search_mainmenu_name) != -1){
                        } else {
                            delete self._searchableMenus[key]

                        }
                    } else {
                        delete self._searchableMenus[key]
                    }
                })
            }

            var results = fuzzy.filter(searchvals, _.keys(this._searchableMenus), {
                pre: "<b>",
                post: "</b>",
            });
            this.$search_modal_Noresults.toggleClass('d-none', Boolean(results.length));
            this.$search_modal_results.html(
                core.qweb.render("spiffy_theme_backend.MenuSearchResults", {
                    results: results,
                    widget: this,
                })
            );
        },
    });
});