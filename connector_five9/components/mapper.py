# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent
from odoo.addons.connector.components.mapper import mapping, only_create


def key_value(field):
    def modifier(self, record, to_attr):
        _field = getattr(record, field, None)
        if not _field:
            return [(5, )]
        records = self.model.env['five9.key.value']
        for row in _field:
            records |= records.upsert(
                key=row['key'], value=row['value'],
            )
        return [(6, 0, records.ids)]
    return modifier


def mapped(field, map_string):
    """Return a mapped value."""
    def modifier(self, record, to_attr):
        _field = getattr(record, field, None)
        if not _field:
            return []
        return _field.mapped(map_string)
    return modifier


class Five9ImportMapper(AbstractComponent):
    _name = 'five9.import.mapper'
    _inherit = ['base.five9.connector', 'base.import.mapper']
    _usage = 'import.mapper'

    @mapping
    @only_create
    def backend_date_created(self, record):
        if record.get('created_at'):
            return {'backend_date_created': record['created_at'][:19]}

    @mapping
    def backend_date_modified(self, record):
        if record.get('modified_at'):
            return {'backend_date_modified': record['modified_at'][:19]}

    @mapping
    @only_create
    def backend_id(self, _):
        return {'backend_id': self.backend_record.id}


class Five9ExportMapper(AbstractComponent):
    _name = 'five9.export.mapper'
    _inherit = ['base.five9.connector', 'base.export.mapper']
    _usage = 'export.mapper'
