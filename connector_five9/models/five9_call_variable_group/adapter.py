# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class Five9AdapterCallVariableGroup(Component):

    _name = 'five9.adapter.call.variable.group'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.call.variable.group'

    _five9_api = 'configuration'

    UID_FIELD = 'name'

    # pylint: disable=W8106
    def create(self, data):
        return self.endpoint.createCallVariablesGroup(**data)

    def update(self, data):
        return self.endpoint.modifyCallVariablesGroup(**data)

    def search_read(self, filters):
        return self._serialize(
            self.endpoint.getCallVariableGroups(filters.get(self.UID_FIELD)),
        )
