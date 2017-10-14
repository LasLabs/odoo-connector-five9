# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none


class Five9SkillImportMapper(Component):
    _name = 'five9.import.mapper.skill'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.skill'

    direct = [('name', 'name'),
              (none('description'), 'description'),
              ('name', 'external_id'),
              ('messageOfTheDay', 'message_of_the_day'),
              ('routeVoiceMails', 'route_voice_mails'),
              ]


class Five9SkillImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.skill'
    _inherit = 'five9.importer'
    _apply_on = 'five9.skill'


class Five9SkillBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.skill'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.skill'
