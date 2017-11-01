# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import external_to_m2o


class Five9CallImportMapper(Component):
    _name = 'five9.import.mapper.call'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.call'

    direct = [('call_id', 'external_id'),
              ('session_id', 'session_id'),
              ('type_name', 'type'),
              ('comments', 'description'),
              ('ANI', 'ani'),
              ('DNIS', 'dnis'),
              ('length', 'call_length'),
              ('handle_time', 'handle_time'),
              ('wrapup_time', 'wrapup_time'),
              ('start_timestamp', 'timestamp_start'),
              ('end_timestamp', 'timestamp_end'),
              ('queue_time', 'queue_time'),
              ('hold_time', 'hold_time'),
              ('park_time', 'park_time'),
              ('bill_time', 'bill_time'),
              ('number', 'number'),
              ('mediatype', 'media_type'),
              ('tcpa_date_of_consent', 'tcpa_date_of_consent'),
              ('language', 'language'),
              (external_to_m2o('campaign_name'), 'campaign_id'),
              (external_to_m2o('disposition_name'), 'disposition_id'),
              (external_to_m2o('skill_name'), 'skill_id'),
              ]


class Five9CallImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.call'
    _inherit = 'five9.importer'
    _apply_on = 'five9.call'

    def _import_dependencies(self):
        self._import_dependency(self.five9_record['campaign_name'],
                                'five9.campaign')
        self._import_dependency(self.five9_record['disposition_name'],
                                'five9.disposition')
        self._import_dependency(self.five9_record['skill_name'],
                                'five9.skill')


class Five9CallBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.call'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.call'
