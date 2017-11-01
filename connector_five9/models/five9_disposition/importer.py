# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none


class Five9DispositionImportMapper(Component):
    _name = 'five9.import.mapper.disposition'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.disposition'

    direct = [(none('name'), 'name'),
              (none('description'), 'description'),
              (none('name'), 'external_id'),
              ]


class Five9DispositionImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.disposition'
    _inherit = 'five9.importer'
    _apply_on = 'five9.disposition'


class Five9DispositionBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.disposition'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.disposition'
