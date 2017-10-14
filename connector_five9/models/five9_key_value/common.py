# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class Five9KeyValue(models.Model):
    _name = 'five9.key.value'
    _description = 'Five9 Key Value'

    key = fields.Char(
        required=True,
        index=True,
    )
    value = fields.Char(
        required=True,
        index=True,
    )
    five9_dict = fields.Serialized(
        compute='_compute_five9_dict',
    )

    _sql_constraints = [
        ('key_value_uniq', 'UNIQUE(key, value)',
         'This key and value combination already exists.'),
    ]

    @api.multi
    def _compute_five9_dict(self):
        """Returns a dictionary for deserialization into a Five9 Object."""
        for record in self:
            record.five9_dict = {
                'key': record.key,
                'value': record.value,
            }

    @api.model
    def upsert(self, key, value):
        """Find or create by key and value."""
        key_value = self.search([
            ('key', '=', key),
            ('value', '=', value),
        ])
        if not key_value:
            key_value = self.create({
                'key': key,
                'value': value,
            })
        return key_value
