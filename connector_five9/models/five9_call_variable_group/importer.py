# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none


class Five9CallVariableGroupImportMapper(Component):
    _name = 'five9.import.mapper.call.variable.group'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.call.variable.group'

    direct = [(none('name'), 'name'),
              (none('description'), 'description'),
              (none('name'), 'external_id'),
              ]


class Five9CallVariableGroupImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.call.variable.group'
    _inherit = 'five9.importer'
    _apply_on = 'five9.call.variable.group'


class Five9CallVariableGroupBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.call.variable.group'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.call.variable.group'
