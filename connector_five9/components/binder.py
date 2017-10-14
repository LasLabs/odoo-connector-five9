# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class Five9ModelBinder(Component):
    """Bind records and give odoo/five9 ID relations."""

    _name = 'five9.binder'
    _inherit = ['base.binder', 'base.five9.connector']
    _apply_on = [
        'five9.agent',
        'five9.agent.group',
        'five9.call',
        'five9.call.variable',
        'five9.call.variable.group',
        'five9.campaign',
        'five9.contact',
        'five9.disposition',
        'five9.skill',
        'five9.web.connector',
    ]
