# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class Five9AdapterAgentGroup(Component):

    _name = 'five9.adapter.agent.group'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.agent.group'

    _five9_api = 'configuration'

    UID_FIELD = 'id'

    def search_read(self, filters):
        _filter = filters.get(self.UID_FIELD, '.*')
        return self._serialize(self.endpoint.getAgentGroups(_filter))
