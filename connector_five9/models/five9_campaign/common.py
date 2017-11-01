# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Five9Campaign(models.Model):

    _name = 'five9.campaign'
    _inherit = 'five9.binding'
    _description = 'Five9 Campaigns'

    name = fields.Char(
        required=True,
    )
    description = fields.Char()
    mode = fields.Selection([
        ('BASIC', 'Basic'),
        ('ADVANCED', 'Advanced'),
    ],
        required=True,
        default='BASIC',
    )
    type = fields.Selection([
        ('INBOUND', 'Inbound'),
        ('OUTBOUND', 'Outbound'),
        ('AUTODIAL', 'Auto-Dial'),
    ],
        required=True,
        default='INBOUND',
    )
    profile_name = fields.Char()
    state = fields.Selection([
        ('NOT_RUNNING', 'Not Running'),
        ('STARTING', 'Starting'),
        ('RUNNING', 'Running'),
        ('STOPPING', 'Stopping'),
        ('RESETTING', 'Resetting'),
    ],
        required=True,
        default='NOT_RUNNING',
    )
    training_mode = fields.Boolean()
