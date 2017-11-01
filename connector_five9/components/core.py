# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent


class BaseFive9ConnectorComponent(AbstractComponent):

    _name = 'base.five9.connector'
    _inherit = 'base.connector'
    _collection = 'five9.backend'
