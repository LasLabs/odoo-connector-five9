# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class Five9AdapterCallVariable(Component):

    _name = 'five9.adapter.call.variable'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.call.variable'

    _five9_api = 'configuration'

    UID_FIELD = 'name'

    # pylint: disable=W8106
    def create(self, data):
        return self.endpoint.createCallVariable(**data)

    def update(self, data):
        return self.endpoint.modifyCallVariable(**data)

    def search_read(self, filters):
        return self._serialize(
            self.endpoint.getCallVariables(filters.get(self.UID_FIELD)),
        )
