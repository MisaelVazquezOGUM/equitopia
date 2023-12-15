# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models

class BizBlogSlider(models.Model):
    _name = 'biz.blog.slider'
    _description = 'Blog Slider'

    name = fields.Char(string="Slider name", default='Blogs',
                       required=True, translate=True)
    active = fields.Boolean(string="Publish on Website", default=True)
    blog_subtitle = fields.Text(string="Slider sub title", default='Blog Sub Title',
                            help="""Slider sub title to be display""", translate=True)
    no_of_objects = fields.Selection([('1', '1'), ('2', '2'), ('3', '3')], string="Blogs Count",
                                    default='3',required=True)
    auto_slide = fields.Boolean(string='Auto Rotate Slider', default=True)
    sliding_speed = fields.Integer(string="Slider sliding speed", default='5000')
    blog_post_ids = fields.Many2many('blog.post', 'blogpost_slider_rel', 'slider_id',
                                             'post_id',
                                             string="Blogs", required=True, domain="[('is_published', '=', True)]")

