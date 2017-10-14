# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class Five9AdapterDisposition(Component):

    _name = 'five9.adapter.disposition'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.disposition'

    _five9_api = 'configuration'

    UID_FIELD = 'name'

    # pylint: disable=W8106
    def create(self, data):
        return self.five9.env.Disposition.create(data)

    def update(self, data):
        disposition = self.five9.env.Disposition(data)
        return disposition.write()

    # pylint: disable=W8106
    def read(self, external_id):
        _logger.debug('Reading for %s', external_id)
        return self.five9.env.Disposition.read(external_id)

    def search_read(self, filters):
        return self.five9.env.Disposition.search(filters)
