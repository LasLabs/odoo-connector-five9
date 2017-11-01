# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from uuid import uuid4

from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    five9_bind_ids = fields.One2many(
        string='Five9 Bindings',
        comodel_name='five9.contact',
        inverse_name='odoo_id',
    )


class Five9Contact(models.Model):

    _name = 'five9.contact'
    _inherit = 'five9.binding'
    _inherits = {'res.partner': 'odoo_id'}
    _description = 'Five9 Contacts'

    _rec_name = 'name'

    odoo_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        required=True,
        ondelete='cascade',
    )
    external_id = fields.Char(
        default=lambda s: str(uuid4()),
    )
