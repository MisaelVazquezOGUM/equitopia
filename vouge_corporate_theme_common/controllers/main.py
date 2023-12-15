# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import re
import math
import json
import os
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo import http, SUPERUSER_ID, fields
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug, unslug

class bizcommonSliderSettings(http.Controller):

    def get_blog_data(self, slider_filter):
        slider_header = request.env['biz.blog.slider'].sudo().search(
            [('id', '=', int(slider_filter))])
        values = {
            'slider_header': slider_header,
            'blog_slider_details': slider_header.blog_post_ids,
        }
        return values


    @http.route(['/vouge_corporate_theme_common/blog_get_options'], type='json', auth="public", website=True)
    def bizcommon_get_slider_options(self):
        slider_options = []
        option = request.env['biz.blog.slider'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options



    @http.route(['/vouge_corporate_theme_common/second_blog_get_dynamic_slider'], type='http', auth='public', website=True)
    def second_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.render("vouge_corporate_theme_common.bizcommon_blog_slider_view", values)



    @http.route(['/vouge_corporate_theme_common/blog_image_effect_config'], type='json', auth='public', website=True)
    def bizcommon_product_image_dynamic_slider(self, **post):
        slider_data = request.env['biz.blog.slider'].search(
            [('id', '=', int(post.get('slider_filter')))])
        values = {
            's_id': str(slider_data.no_of_objects) + '-' + str(slider_data.id),
            'counts': slider_data.no_of_objects,
            'auto_slide': slider_data.auto_slide,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values