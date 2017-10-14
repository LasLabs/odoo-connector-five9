# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)

try:
    from zeep.exceptions import Fault
except ImportError:
    _logger.debug("`zeep` Python library not installed.")


class Five9AdapterContact(Component):

    _name = 'five9.adapter.contact'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.contact'

    _five9_api = 'configuration'

    UID_FIELD = '__odoo_uid__'

    META_FIELDS = [
        {'name': 'modified_at',
         'display_as': 'Invisible',
         'map_to': 'LastModifiedDateTime',
         'system': True,
         'type': 'DATE_TIME',
         },
        {'name': 'created_at',
         'display_as': 'Invisible',
         'map_to': 'CreatedDateTime',
         'system': True,
         'type': 'DATE_TIME',
         },
        {'name': UID_FIELD,
         'display_as': 'Invisible',
         'system': False,
         'type': 'STRING',
         },
    ]

    def create_meta_fields(self):
        """Create the fields necessary for operation, if necessary."""
        existing = self._get_contact_fields()
        for field in self.META_FIELDS:
            if field['name'] not in existing:
                self.create_field(**field)

    def create_field(self, name, display_as='Short', map_to='None',
                     system=False, type='STRING'):
        """Create a field in the CRM."""
        try:
            self.endpoint.createContactField({
                'displayAs': display_as,
                'mapTo': map_to,
                'name': name,
                'system': system,
                'type': type,
            })
        except Fault as e:
            if e.message == 'Mapping already exists':
                return
            raise

    # pylint: disable=W8106
    def create(self, data):
        if not data.get(self.UID_FIELD):
            data[self.UID_FIELD] = self.new_uuid()
        return self.upsert(
            external_id=data[self.UID_FIELD],
            data=data,
            allow_add=True,
            allow_update=False,
        )

    def delete(self, external_id, uid_field=None):

        if uid_field is None:
            uid_field = self.UID_FIELD

        data = {uid_field or self.UID_FIELD: external_id}
        mapping = self.five9.create_mapping(data, keys=[uid_field])
        return self.endpoint.deleteFromContacts(
            importData={'values': mapping['fields']},
            crmDeleteSettings={
                'fieldsMapping': mapping['field_mappings'],
                'crmDeleteMode': 'DELETE_SOLE_MATCHES',
                'skipHeaderLine': False,
            },
        )

    # pylint: disable=W8106
    def write(self, external_id, data):
        return self.upsert(
            external_id=external_id,
            data=data,
            allow_add=True,
            allow_update=True,
        )

    def search_read(self, filters, inject_uid=True):
        _logger.debug('Searching for %s', filters)
        result = self.endpoint.getContactRecords(
            self.five9.create_criteria(filters),
        )
        if not result:
            return []
        records = self.five9.parse_response(
            result['fields'], result['records'],
        )
        if inject_uid:
            records = [self.inject_uid(r) for r in records]
        return records

    def inject_uid(self, record):
        """If a UID isn't existing on the record, inject and send to remote.
        """
        if record.get(self.UID_FIELD):
            return record
        record = {k: v for k, v in record.items() if v}
        keys = record.keys()
        record[self.UID_FIELD] = self.new_uuid()
        mapping = self.five9.create_mapping(record, keys=keys)
        _logger.debug('Injecting UID with mapping: %s', mapping)
        self.endpoint.updateCrmRecord(
            record={'fields': mapping['fields']},
            crmUpdateSettings={
                'fieldsMapping': mapping['field_mappings'],
                'skipHeaderLine': False,
                'crmAddMode': 'DONT_ADD',
                'crmUpdateMode': 'UPDATE_SOLE_MATCHES',
            },
        )
        return record

    def upsert(self, external_id, data, allow_add=True, allow_update=True,
               sole_match=True, uid_field=None):

        add_mode = 'ADD_NEW' if allow_add else 'DONT_ADD'
        if allow_update:
            update_mode = sole_match and 'UPDATE_SOLE_MATCHES' or 'UPDATE_ALL'
        else:
            update_mode = 'DONT_UPDATE'

        if uid_field is None:
            uid_field = self.UID_FIELD

        data[uid_field] = external_id
        mapping = self.five9.create_mapping(data, keys=[uid_field])

        return self.endpoint.updateCrmRecord(
            record={'fields': mapping['fields']},
            crmUpdateSettings={
                'fieldsMapping': mapping['field_mappings'],
                'skipHeaderLine': False,
                'crmAddMode': add_mode,
                'crmUpdateMode': update_mode,
            },
        )

    def _get_contact_fields(self):
        return [
            e['name'] for e in self.endpoint.getContactFields()
        ]
