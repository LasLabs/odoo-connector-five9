# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, datetime, time, timedelta
from dateutil.parser import parse

from odoo import api, models, fields
from odoo.tools import safe_eval


class Five9CallVariableType(models.Model):

    _name = 'five9.call.variable.type'
    _description = 'Five9 Call Variable Types'

    name = fields.Char(
        required=True,
    )
    deserialize = fields.Text(
        default='value and str(value) or False',
        help='Code used to deserialize a value for insert into an Odoo typed '
             'column. It receives ``value``, which is the string value of the '
             'record. It also receives the locals from ``_get_locals_dict``.'
    )

    @api.multi
    def action_deserialize(self, value):
        self.ensure_one()
        locals = self._get_locals_dict()
        locals['value'] = value
        return safe_eval(self.deserialize, locals)

    def _get_locals_dict(self):
        return {
            'fields': fields,
            'date': date,
            'datetime': datetime,
            'parse': parse,
            'time': time,
            'timedelta': timedelta,
        }
