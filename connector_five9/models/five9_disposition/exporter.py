# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import none


class Five9DispositionExportMapper(Component):

    _name = 'five9.export.mapper.disposition'
    _inherit = 'five9.export.mapper'
    _apply_on = 'five9.disposition'

    direct = [(none('name'), 'name'),
              (none('description'), 'description'),
              ]


class Five9DispositionExporter(Component):
    """Export one Five9 record."""
    _name = 'five9.disposition.record.exporter'
    _inherit = 'five9.exporter'
    _apply_on = 'five9.disposition'
