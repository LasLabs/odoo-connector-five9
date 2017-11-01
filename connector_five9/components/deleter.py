# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.addons.component.core import AbstractComponent


class Five9Deleter(AbstractComponent):

    _name = 'five9.exporter.deleter'
    _inherit = ['base.deleter', 'base.five9.connector']
    _usage = 'record.exporter.deleter'

    def run(self, external_id):
        self.backend_adapter.delete(external_id)
        return _('Record %s deleted on Five9') % external_id
