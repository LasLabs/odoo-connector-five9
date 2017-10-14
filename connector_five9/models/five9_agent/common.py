# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResUsers(models.Model):

    _inherit = 'res.users'

    five9_bind_ids = fields.One2many(
        string='Five9 Bindings',
        comodel_name='five9.agent',
        inverse_name='odoo_id',
    )


class Five9Agent(models.Model):

    _name = 'five9.agent'
    _inherit = 'five9.binding'
    _description = 'Five9 Agents'

    odoo_id = fields.Many2one(
        string='User',
        comodel_name='res.users',
        required=True,
        ondelete='cascade',
    )
    group_ids = fields.Many2many(
        string='Groups',
        comodel_name='five9.agent.group',
    )
    skill_ids = fields.Many2many(
        string='Skills',
        comodel_name='five9.skill',
    )
    can_change_password = fields.Boolean()
    extension = fields.Char()
    iex_schedules = fields.Boolean()
    locale = fields.Char()
    media_type_config = fields.Serialized()
    must_change_password = fields.Boolean()
    os_login = fields.Boolean()
    phone_number = fields.Char()
    start_date = fields.Datetime()
    user_name = fields.Char()
    user_profile_name = fields.Char()
    roles = fields.Serialized()
