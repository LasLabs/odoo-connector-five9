# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class Five9AdapterAgent(Component):

    _name = 'five9.adapter.agent'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.agent'

    _five9_api = 'configuration'

    UID_FIELD = 'id'

    # pylint: disable=W8106
    def read(self, name):
        for record in self.search_read({self.UID_FIELD: name}):
            return self._format_record(record)

    def search_read(self, filters):
        return self._serialize(
            self.endpoint.getUsersInfo(filters.get('name')),
        )

    def _format_record(self, record):
        """Squash all the top level keys into generalInfo and return that."""
        for key, val in record.items():
            if key == 'generalInfo':
                continue
            record['generalInfo'][key] = val
        return record['generalInfo']
