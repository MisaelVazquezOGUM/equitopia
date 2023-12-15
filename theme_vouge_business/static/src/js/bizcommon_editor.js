odoo.define('theme_vouge_business.bizcommon_editor_js', function(require) {
    'use strict';
    var options = require('web_editor.snippets.options');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    ajax.loadXML('/vouge_corporate_theme_common/static/src/xml/bizople_theme_common.xml', qweb);
    ajax.loadXML('/theme_vouge_business/static/src/xml/web_editor_inherit.xml', qweb);

    options.registry.health_blog_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.health_blog_slider').empty();
            
            if (!editMode) {
                self.$el.find(".health_blog_slider").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.health_blog_slider').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.vouge_corporate_theme_common_blog_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.bizcommon_blog_slider').empty();
           
            if (!editMode) {
                self.$el.find(".bizcommon_blog_slider").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.bizcommon_blog_slider').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.s_bizople_theme_blog_slider_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_slider_owl').empty();
            
            if (!editMode) {
                self.$el.find(".blog_slider_owl").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_slider_owl').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_3_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_3_custom').empty();
            
            if (!editMode) {
                self.$el.find(".blog_3_custom").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_3_custom').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    
    options.registry.blog_4_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_4_custom').empty();
           
            if (!editMode) {
                self.$el.find(".blog_4_custom").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_4_custom').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_6_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_6_custom').empty();
           
            if (!editMode) {
                self.$el.find(".blog_6_custom").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_6_custom').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_5_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_5_custom').empty();
            if (!editMode) {
                self.$el.find(".blog_5_custom").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_5_custom').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });
    options.registry.blog_8_custom_snippet = options.Class.extend({
        start: function(editMode) {
            var self = this;
            this._super();
            this.$target.removeClass("o_hidden");
            this.$target.find('.blog_8_custom').empty();
            if (!editMode) {
                self.$el.find(".blog_8_custom").on("click", _.bind(self.vouge_corporate_theme_common_blog_slider, self));
            }
        },
        onBuilt: function() {
            var self = this;
            this._super();
            if (this.vouge_corporate_theme_common_blog_slider()) {
                this.vouge_corporate_theme_common_blog_slider().fail(function() {
                    self.getParent()._removeSnippet();
                });
            }
        },
        cleanForSave: function() {
            $('.blog_8_custom').empty();
        },
        vouge_corporate_theme_common_blog_slider: function(type, value) {
            var self = this;
            if (type != undefined && type.type == "click" || type == undefined) {
                self.$modal = $(qweb.render("vouge_corporate_theme_common.bizcommon_blog_slider_block"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $slider_filter = self.$modal.find("#blog_slider_filter"),
                    $blog_slider_cancel = self.$modal.find("#cancel"),
                    $sub_data = self.$modal.find("#blog_sub_data");

                ajax.jsonRpc('/vouge_corporate_theme_common/blog_get_options', 'call', {}).then(function(res) {
                    $('#blog_slider_filter option[value!="0"]').remove();
                    _.each(res, function(y) {
                        $("select[id='blog_slider_filter'").append($('<option>', {
                            value: y["id"],
                            text: y["name"]
                        }));
                    });
                });
                $sub_data.on('click', function() {
                    var type = '';
                    self.$target.attr('data-blog-slider-type', $slider_filter.val());
                    self.$target.attr('data-blog-slider-id', 'blog-myowl' + $slider_filter.val());
                    if ($('select#blog_slider_filter').find(":selected").text()) {
                        type = _t($('select#blog_slider_filter').find(":selected").text());
                    } else {
                        type = _t("Blog Post Slider");
                    }
                    self.$target.empty().append('<div class="container">\
                                                    <div class="block-title">\
                                                        <h3 class="filter">' + type + '</h3>\
                                                    </div>\
                                                </div>');
                });
                $blog_slider_cancel.on('click', function() {
                    self.getParent()._onRemoveClick($.Event("click"))
                })
            } else {
                return;
            }
        },
    });

});