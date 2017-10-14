# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping, none, only_create


class Five9ContactImportMapper(Component):
    _name = 'five9.import.mapper.contact'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.contact'

    direct = [(none('first_name'), 'firstname'),
              (none('last_name'), 'lastname'),
              (none('street'), 'street'),
              (none('city'), 'city'),
              (none('zip'), 'zip'),
              (none('number1'), 'phone'),
              (none('number2'), 'mobile'),
              (none('number3'), 'fax'),
              ('__odoo_uid__', 'external_id'),
              ]

    @mapping
    @only_create
    def odoo_id(self, record):
        """Match on partners with same information."""
        numbers = (record['number1'], record['number2'], record['number3'])
        partner = self.env['res.partner'].search([
            ('firstname', '=', record.get('first_name')),
            ('lastname', '=', record.get('last_name')),
            ('phone', 'in', numbers),
        ])
        if partner:
            return {'odoo_id': partner[:1].id}

    @mapping
    def state_id(self, record):
        state = self.env['res.country.state'].search([
            '|',
            ('name', '=', record.get('state')),
            ('code', '=', record.get('state')),
        ])
        if state:
            return {'state_id': state.id}


class Five9ContactImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.contact'
    _inherit = 'five9.importer'
    _apply_on = 'five9.contact'


class Five9ContactBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.contact'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.contact'
