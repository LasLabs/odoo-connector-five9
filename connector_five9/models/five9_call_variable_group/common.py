# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class Five9CallVariableGroup(models.Model):

    _name = 'five9.call.variable.group'
    _inherit = 'five9.binding'
    _description = 'Five9 Call Variable Groups'

    BIND_MAP = {
        'Call': 'five9.call',
        'Customer': 'five9.contact',
        'Agent': 'five9.agent',
    }

    name = fields.Char(
        required=True,
    )
    description = fields.Char()
    variable_ids = fields.One2many(
        string='Variables',
        comodel_name='five9.call.variable',
        inverse_name='group_id',
    )
    bind_model_name = fields.Char(
        help='The name of the bind model to use for this variable group '
             'type.',
        compute='_compute_bind_model_name',
        store=True,
    )

    @api.multi
    @api.depends('name')
    def _compute_bind_model_name(self):
        for record in self:
            record.bind_model_name = self.BIND_MAP.get(record.name, False)
