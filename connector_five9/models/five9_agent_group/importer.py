# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none


class Five9AgentGroupImportMapper(Component):
    _name = 'five9.import.mapper.agent.group'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.agent.group'

    direct = [('name', 'name'),
              (none('description'), 'description'),
              ]


class Five9AgentGroupImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.agent.group'
    _inherit = 'five9.importer'
    _apply_on = 'five9.agent.group'


class Five9AgentGroupBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.agent.group'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.agent.group'
