# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none

from ...components.mapper import key_value


class Five9WebConnectorImportMapper(Component):
    _name = 'five9.import.mapper.web.connector'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.web.connector'

    direct = [
        (none('addWorksheet'), 'add_worksheet'),
        (none('agentApplication'), 'agent_application'),
        (none('clearTriggerDispositions'),
         'clear_trigger_dispositions'),
        (none('ctiWebServices'), 'cti_web_services'),
        (none('name'), 'name'),
        (none('description'), 'description'),
        (none('executeInBrowser'), 'execute_in_browser'),
        (none('postMethod'), 'is_post'),
        (none('startPageText'), 'start_page_text'),
        (none('trigger'), 'trigger'),
        (none('triggerDispositions'),
         'trigger_dispositions_list'),
        (none('url'), 'uri_json'),
        (none('name'), 'external_id'),
        (key_value('constants'), 'constant_ids'),
        (key_value('postConstants'), 'post_constant_ids'),
        (key_value('postVariables'), 'post_variable_ids'),
        (key_value('variables'), 'variable_ids'),
    ]


class Five9WebConnectorImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.web.connector'
    _inherit = 'five9.importer'
    _apply_on = 'five9.web.connector'

    def _import_dependencies(self):
        for disposition in self.five9_record.triggerDispositions:
            self._import_dependency(disposition, 'five9.disposition')


class Five9ContactBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.web.connector'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.web.connector'
