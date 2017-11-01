# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import (mapping,
                                                     none,
                                                     )


class Five9ContactExportMapper(Component):

    _name = 'five9.export.mapper.contact'
    _inherit = 'five9.export.mapper'
    _apply_on = 'five9.contact'

    direct = [(none('firstname'), 'first_name'),
              (none('lastname'), 'last_name'),
              (none('street'), 'street'),
              (none('city'), 'city'),
              (none('zip'), 'zip'),
              (none('phone'), 'number1'),
              (none('mobile'), 'number2'),
              (none('fax'), 'number3'),
              ('external_id', '__odoo_uid__'),
              ]

    @mapping
    def state(self, record):
        return {'state': record.state_id.code}


class Five9ContactExporter(Component):
    """Export one Five9 record."""
    _name = 'five9.contact.record.exporter'
    _inherit = 'five9.exporter'
    _apply_on = 'five9.contact'
