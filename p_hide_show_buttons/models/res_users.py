# -*- coding: utf-8 -*-
# Part of Param Enterprice. See LICENSE file for full copyright and licensing details.
from odoo import models,fields,api

class Res_Users(models.Model):
    _inherit = 'res.users'
    
    hide_show_id = fields.One2many(
        'hide.show.button',
        'request_id',
    )
    
    @api.model
    def hide_buttons(self,button,model_name,view_type):
        print(button)
        print(model_name)
        print(view_type)
        print(type(button))
        user_id = self.env.user
        if view_type == 'list':
            new_val = {
                'save' : 'null',
                'discard' : 'null',
                'create' : 'null',
                'export' : 'null',
            }
            if not user_id.hide_show_id:
                return new_val
            else:
                button_list = []
                if isinstance(button, str):
                    button_list = [str(button)]
                elif isinstance(button, dict):
                    button['export'] = True
                    button_list = button.keys()
                for record in user_id.hide_show_id:
                    if record.button in button_list and not record.ir_model_ids:
                        if not record.ir_views_ids:
                            new_val[record.button] = True
                            # return True
                        else:
                            for view in record.ir_views_ids:
                                if view.view_name == view_type:
                                    new_val[record.button] = True
                                    # return True
                    elif record.button in button_list and record.ir_model_ids:
                        for model in record.ir_model_ids:
                            if model.model == model_name and not record.ir_views_ids:
                                new_val[record.button] = True
                                # return True
                            elif model.model == model_name and record.ir_views_ids:
                                for view in record.ir_views_ids:
                                    if view.view_name == view_type:
                                        new_val[record.button] = True
                                        # return True

            return new_val

        elif view_type == 'form':
            new_val = {
                'save': 'null',
                'discard': 'null',
                'create': 'null',
                'edit': 'null'
            }
            if not user_id.hide_show_id:
                return new_val
            else:
                button_list = []
                if isinstance(button, str):
                    button_list = [str(button)]
                elif isinstance(button, dict):
                    button_list = button.keys()
                for record in user_id.hide_show_id:
                    if record.button in button_list and not record.ir_model_ids:
                        if not record.ir_views_ids:
                            new_val[record.button] = True
                            # return True
                        else:
                            for view in record.ir_views_ids:
                                if view.view_name == view_type:
                                    new_val[record.button] = True
                                    # return True
                    elif record.button in button_list and record.ir_model_ids:
                        for model in record.ir_model_ids:
                            if model.model == model_name and not record.ir_views_ids:
                                new_val[record.button] = True
                                # return True
                            elif model.model == model_name and record.ir_views_ids:
                                for view in record.ir_views_ids:
                                    if view.view_name == view_type:
                                        new_val[record.button] = True
                                        # return True

            return new_val

        elif view_type == 'kanban':
            new_val = {
                'create': 'null',
            }
            if not user_id.hide_show_id:
                return new_val
            else:
                button_list = []
                if isinstance(button, str):
                    button_list = [str(button)]
                elif isinstance(button, dict):
                    button_list = button.keys()
                for record in user_id.hide_show_id:
                    if record.button in button_list and not record.ir_model_ids:
                        if not record.ir_views_ids:
                            new_val[record.button] = True
                            # return True
                        else:
                            for view in record.ir_views_ids:
                                if view.view_name == view_type:
                                    new_val[record.button] = True
                                    # return True
                    elif record.button in button_list and record.ir_model_ids:
                        for model in record.ir_model_ids:
                            if model.model == model_name and not record.ir_views_ids:
                                new_val[record.button] = True
                                # return True
                            elif model.model == model_name and record.ir_views_ids:
                                for view in record.ir_views_ids:
                                    if view.view_name == view_type:
                                        new_val[record.button] = True
                                        # return True

            return new_val
        elif view_type == 'pivot':
            new_val = {
                'export': 'null',
            }
            if not user_id.hide_show_id:
                return new_val
            else:
                button_list = []
                if isinstance(button, str):
                    button_list = [str(button)]
                elif isinstance(button, dict):
                    button['export'] = True
                    button_list = button.keys()
                for record in user_id.hide_show_id:
                    if record.button in button_list and not record.ir_model_ids:
                        if not record.ir_views_ids:
                            new_val[record.button] = True
                            # return True
                        else:
                            for view in record.ir_views_ids:
                                if view.view_name == view_type:
                                    new_val[record.button] = True
                                    # return True
                    elif record.button in button_list and record.ir_model_ids:
                        for model in record.ir_model_ids:
                            if model.model == model_name and not record.ir_views_ids:
                                new_val[record.button] = True
                                # return True
                            elif model.model == model_name and record.ir_views_ids:
                                for view in record.ir_views_ids:
                                    if view.view_name == view_type:
                                        new_val[record.button] = True
                                        # return True

            return new_val
        return False
    
class hide_buttons(models.Model):
    _name='hide.show.button'
    
    request_id = fields.Many2one(
        'res.users'
    )
    ir_model_ids = fields.Many2many(
        'ir.model',
        string = "Models"
    )
    button = fields.Selection(
        [
            ('create','Create'),
            ('edit','Edit'),
            ('save','Save'),
            ('discard','Discard'),
            ('import','Import'),
            ('export','Export')
        ],
        sting = "Buttons",
        required = True
    )
    
    ir_views_ids = fields.One2many(
        'ir.views',
        'request_id',
        string = "Views"
    )
    
class Views(models.Model):
    _name = 'ir.views'
    
    request_id = fields.Many2one(
        'hide.show.button'
    )
    name = fields.Char(
        "Name",
        required = True
    )
    view_name = fields.Char(
        "View Name",
        required = True
    )
