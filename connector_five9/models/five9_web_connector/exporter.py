# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none

from ...components.mapper import mapped


class Five9WebConnectorExportMapper(Component):
    _name = 'five9.export.mapper.web.connector'
    _inherit = 'five9.export.mapper'
    _apply_on = 'five9.web.connector'

    direct = [(none('add_worksheet'), 'addWorksheet'),
              (none('agent_application'), 'agentApplication'),
              (none('clear_trigger_dispositions'),
               'clearTriggerDispositions'),
              (none('cti_web_services'), 'ctiWebServices'),
              (none('name'), 'name'),
              (none('description'), 'description'),
              (none('execute_in_browser'), 'executeInBrowser'),
              (none('is_post'), 'postMethod'),
              (none('start_page_text'), 'startPageText'),
              (none('trigger'), 'trigger'),
              (none('trigger_dispositions_list'), 'triggerDispositions'),
              (none('uri_http_authenticated'), 'url'),
              (mapped('constant_ids', 'five9_dict'), 'constants'),
              (mapped('post_constant_ids', 'five9_dict'), 'postConstants'),
              (mapped('post_variable_ids', 'five9_dict'), 'postVariables'),
              (mapped('variable_ids', 'five9_dict'), 'variables'),
              ]


class Five9WebConnectorExporter(Component):
    """Export one Five9 record."""
    _name = 'five9.record.exporter.web.connector'
    _inherit = 'five9.exporter'
    _apply_on = 'five9.web.connector'

    def _after_export(self):
        """The external_id needs to be manually set."""
        self.binding.external_id = self.binding.name
