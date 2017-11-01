# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Five9Skill(models.Model):

    _name = 'five9.skill'
    _inherit = 'five9.binding'
    _description = 'Five9 Skills'

    name = fields.Char(
        required=True,
    )
    description = fields.Char()
    message_of_the_day = fields.Char()
    route_voice_mails = fields.Boolean()
