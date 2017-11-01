# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import (external_to_m2o,
                                                     mapping,
                                                     none,
                                                     )


class Five9CallVariableImportMapper(Component):
    _name = 'five9.import.mapper.call.variable'
    _inherit = 'five9.import.mapper'
    _apply_on = 'five9.call.variable'

    direct = [(none('name'), 'name'),
              (none('description'), 'description'),
              (none('name'), 'external_id'),
              ('applyToAllDispositions', 'apply_to_all_dispositions'),
              (none('defaultValue'), 'default_value'),
              ('reporting', 'reporting'),
              ('sensitiveData', 'sensitive_data'),
              (external_to_m2o('group'), 'group_id'),
              ]

    @mapping
    def disposition_ids(self, record):
        disposition_ids = [(5, 0)]
        for name in record['dispositions']:
            binder = self.binder_for('five9.disposition')
            disposition = binder.to_internal(name, unwrap=False)
            if disposition:
                disposition_ids.append((4, disposition.id))
        return {'disposition_ids': disposition_ids}

    @mapping
    def type_id(self, record):
        variable_type = self.env['five9.call.variable.type'].search([
            ('name', '=', record['type']),
        ])
        return {'type_id': variable_type.id}


class Five9CallVariableImporter(Component):
    """Import one Five9 record."""
    _name = 'five9.record.importer.call.variable'
    _inherit = 'five9.importer'
    _apply_on = 'five9.call.variable'

    def _import_dependencies(self):
        self._import_dependency(self.five9_record['group'],
                                'five9.call.variable.group')
        for disposition in self.five9_record['dispositions']:
            self._import_dependency(disposition,
                                    'five9.disposition')


class Five9CallVariableBatchImporter(Component):
    """Import a batch of Five9 records."""
    _name = 'five9.batch.importer.call.variable'
    _inherit = 'five9.direct.batch.importer'
    _apply_on = 'five9.call.variable'
