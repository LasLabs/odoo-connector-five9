# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import (only_create,
                                                     external_to_m2o,
                                                     mapping,
                                                     none,
                                                     )


class Five9AgentImportMapper(Component):
    _name = 'five9.import.mapper.agent'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.agent'

    direct = [(external_to_m2o('skills'), 'skill_ids'),
              (external_to_m2o('agentGroups'), 'group_ids'),
              (none('active'), 'active'),
              (none('canChangePassword'), 'can_change_password'),
              (none('EMail'), 'email'),
              (none('extension'), 'extension'),
              (none('firstName'), 'firstname'),
              (none('lastName'), 'lastname'),
              (none('IEXScheduled'), 'iex_scheduled'),
              (none('locale'), 'locale'),
              ('mediaTypeConfig', 'media_type_config'),
              ('mustChangePassword', 'must_change_password'),
              ('osLogin', 'os_login'),
              ('phoneNumber', 'phone'),
              ('startDate', 'start_date'),
              ('userName', 'user_name'),
              ('userProfileName', 'user_profile_name'),
              ('roles', 'roles'),
              ]

    @mapping
    @only_create
    def odoo_id(self, record):
        user = self.env['res.users'].search([
            ('email', '=', record['EMail']),
        ])
        if user:
            return {'odoo_id': user.id}


class Five9AgentImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.agent'
    _inherit = 'five9.importer'
    _apply_on = 'five9.agent'

    def _import_dependencies(self):
        self._import_dependency(self.five9_record['skills'],
                                'five9.agent')
        self._import_dependency(self.five9_record['agentGroups'],
                                'five9.agent.group')


class Five9AgentBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.agent'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.agent'
