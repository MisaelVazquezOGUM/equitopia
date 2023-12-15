odoo.define('spiffy_theme_backend.ListRendererInherit', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');
    var DocumentViewer = require('mail.DocumentViewer');
    var ajax = require("web.ajax");
    var core = require("web.core");
    var _t = core._t;

    var biz_listrenderer = ListRenderer.include({
        events: _.extend({}, ListRenderer.prototype.events, {
            "click .attachment_box": "_loadattachmentviewer",
        }),
        willStart: async function () {
            const _super = this._super.bind(this);
            var self = this;
            await ajax.jsonRpc("/get/attachment/data", "call", {
                domain: this.state.domain,
                model: this.state.model,
                rec_ids: this.state.res_ids,
            }).then(function (data) {
                if (data) {
                  self.biz_attachment_data = data;
                }
            });
            return _super(...arguments);
        },
        _loadattachmentviewer: function (ev) {
            var attachment_id = parseInt($(ev.currentTarget).data("id"));
            var rec_id = parseInt($(ev.currentTarget).data("rec_id"));
            var attachment_mimetype = $(ev.currentTarget).data("mimetype");
            var mimetype_match = attachment_mimetype.match("(image|application/pdf|text|video)");
            var attachment_data = this.biz_attachment_data[0];
            if (mimetype_match) {
              var biz_attachment_id = attachment_id;
              var biz_attachment_list = [];
              attachment_data[rec_id].forEach((attachment) => {
                if (attachment.attachment_mimetype.match("(image|application/pdf|text|video)")) {
                  biz_attachment_list.push({
                    id: attachment.attachment_id,
                    filename: attachment.attachment_name,
                    name: attachment.attachment_name,
                    url: "/web/content/"+attachment.attachment_id+"?download=true",
                    type: attachment.attachment_mimetype,
                    mimetype: attachment.attachment_mimetype,
                    is_main: false,
                  });
                }
              });
              var biz_attachmentViewer = new DocumentViewer(self,biz_attachment_list,biz_attachment_id);
              biz_attachmentViewer.appendTo($("body"));
            } else this.call("notification", "notify", {
                title: _t("File Format Not Supported"),
                message: _t("Preview for this file type can not be shown"),
                sticky: false,
            });
        },
        _renderRow: function (record) {
            var res = this._super.apply(this, arguments);
            if ($('body').hasClass('show_attachment')){
              if (this.biz_attachment_data) {
                var attachment_data = this.biz_attachment_data[0];
                if (attachment_data[record.data.id]) {
                    var $main_div = $("<div>", {
                        class: "attachment_div",
                    });
                    var $attachment_section = $("<section>", {
                      class: "biz_attachment_section d-flex align-items-center justify-content-center w-100 position-absolute",
                      id: record.id,
                    });
                    attachment_data[record.data.id].every((attachment, index, arr) => {
                      if (index < 5) {
                        var $attachment_box = $("<div>", {
                          class: "attachment_box border d-flex align-items-center mx-2",
                          "data-id": attachment.attachment_id,
                          "data-name": attachment.attachment_name,
                          "data-mimetype": attachment.attachment_mimetype,
                          "data-rec_id": record.data.id,
                        });
          
                        var $attachment_image = $("<span>", {
                            "data-mimetype": attachment.attachment_mimetype,
                            class: "o_image mr-2",
                        })
                        $attachment_box = $attachment_box.append($attachment_image);
          
                        var $attachment_name = $("<div>", {
                          class: "attachment-name text-nowrap",
                        }).append($("<span>").html(attachment.attachment_name));
                        $attachment_box = $attachment_box.append($attachment_name);
  
                        $attachment_section = $attachment_section.append($attachment_box);
                        $main_div = $main_div.append($attachment_section);
                        return true;
                      } else {
                        var $attachment_box = $("<div>", {
                          class: "attachment_box border attachment_box_counter d-flex align-items-center px-2 ",
                          "data-id": attachment.attachment_id,
                          "data-name": attachment.attachment_name,
                          "data-mimetype": attachment.attachment_mimetype,
                          "data-rec_id": record.data.id,
                        });
                        var $attachment_name = $("<div>", {
                          class: "attachment-name text-nowrap",
                        }).append(
                          $("<span>").html("+" + (arr.length - 5))
                        );
                        $attachment_box = $attachment_box.append($attachment_name);
                        $attachment_section = $attachment_section.append($attachment_box);
                        $main_div = $main_div.append($attachment_section);
                        return false;
                      }
                    });
                    res = res.add($main_div);
                }
              }
            }
            return res
        },
    });
    return biz_listrenderer;
});