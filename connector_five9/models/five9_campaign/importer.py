# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none


class Five9CampaignImportMapper(Component):
    _name = 'five9.import.mapper.campaign'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.campaign'

    direct = [('name', 'name'),
              (none('description'), 'description'),
              ('name', 'external_id'),
              ('mode', 'mode'),
              ('profileName', 'profile_name'),
              ('state', 'state'),
              ('trainingMode', 'training_mode'),
              ('type', 'type'),
              ]


class Five9CampaignImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.campaign'
    _inherit = 'five9.importer'
    _apply_on = 'five9.campaign'


class Five9CampaignBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.campaign'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.campaign'