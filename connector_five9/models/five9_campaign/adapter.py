# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class Five9AdapterCampaign(Component):

    _name = 'five9.adapter.campaign'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.campaign'

    _five9_api = 'configuration'

    UID_FIELD = 'name'

    def search_read(self, filters):
        return self._serialize(
            self.endpoint.getCampaigns(filters.get(self.UID_FIELD)),
        )
