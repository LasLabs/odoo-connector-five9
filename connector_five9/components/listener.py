# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class Five9Listener(Component):
    """Generic event listener for Five9."""
    _name = 'five9.listener'
    _inherit = ['base.event.listener', 'base.five9.connector']

    def no_connector_export(self, record):
        return self.env.context.get('connector_no_export')

    def export_record(self, record, fields=None):
        record.with_delay().export_record(fields=fields)

    def delete_record(self, record):
        record.with_delay().export_delete_record()


class Five9ListenerBinding(Component):
    """Generic event listener for Five9 bindings."""
    _name = 'five9.listener.binding'
    _inherit = 'five9.listener'
    _apply_on = [
        'five9.contact',
        'five9.disposition',
        'five9.web.connector',
    ]

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        self.export_record(record, fields)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        self.export_record(record, fields)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_unlink(self, record):
        self.delete_record(record)


class Five9ListenerOdoo(Component):
    """Generic event listener for Odoo models."""
    _name = 'five9.listener.odoo'
    _inherit = 'five9.listener'
    _apply_on = [
        'res.partner',
    ]

    def new_binding(self, record):
        exporter = self.env['five9.backend'].default_exporter
        if exporter:
            return record.five9_bind_ids.create({
                'odoo_id': record.id,
                'backend_id': exporter.id,
            })

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        self.new_binding(record)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        if not record.five9_bind_ids:
            return
        self.export_record(record.five9_bind_ids, fields)

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_unlink(self, record):
        if not record.five9_bind_ids:
            return
        self.delete_record(record.five9_bind_ids)
