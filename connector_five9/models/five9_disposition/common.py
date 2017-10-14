# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProjectCategory(models.Model):

    _inherit = 'project.category'

    five9_bind_ids = fields.One2many(
        string='Five9 Bindings',
        comodel_name='five9.disposition',
        inverse_name='odoo_id',
    )


class Five9Disposition(models.Model):

    _name = 'five9.disposition'
    _inherit = 'five9.binding'
    _inherits = {'project.category': 'odoo_id'}
    _description = 'Five9 Dispositions'

    _rec_name = 'name'

    odoo_id = fields.Many2one(
        string='Project Category',
        comodel_name='project.category',
        required=True,
        ondelete='cascade',
    )
