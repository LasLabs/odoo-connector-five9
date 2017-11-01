# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Five9AgentGroup(models.Model):

    _name = 'five9.agent.group'
    _inherit = 'five9.binding'
    _description = 'Five9 Agent Groups'

    name = fields.Char()
    description = fields.Char()
    agent_ids = fields.Many2many(
        string='Agents',
        comodel_name='five9.agent',
    )
