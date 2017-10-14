# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import api, models, fields


class Five9CallVariable(models.Model):

    _name = 'five9.call.variable'
    _inherit = 'five9.binding'
    _description = 'Five9 Call Variables'

    name = fields.Char(
        required=True,
    )
    description = fields.Char(
        required=True,
    )
    apply_to_all_dispositions = fields.Boolean()
    default_value = fields.Char()
    disposition_ids = fields.Many2many(
        string='Dispositions',
        comodel_name='five9.disposition',
    )
    group_id = fields.Many2one(
        string='Group',
        comodel_name='five9.call.variable.group',
    )
    type_id = fields.Many2one(
        string='Type',
        comodel_name='five9.call.variable.type',
        required=True,
    )
    reporting = fields.Boolean()
    sensitive_data = fields.Boolean()

    @api.multi
    def _get_data(self, data):
        """Find the proper variables in data and return in a dict."""
        results = {}
        for record in self:
            results[record.name] = record.type_id.action_deserialize(
                data.get(record.name),
            )
        return results

    @api.model
    def _get_grouped(self, backend, data=None):
        """Return a dictionary of variable records, keyed by group."""
        grouped = defaultdict(self.browse)
        domain = [('backend_id', '=', backend.id)]
        if data is not None:
            domain.append(('name', 'in', data.keys()))
        for record in self.search(domain):
            grouped[record.group_id] += record
        return grouped
