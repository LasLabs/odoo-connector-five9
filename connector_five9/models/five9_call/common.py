# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProjectTask(models.Model):

    _inherit = 'project.task'

    five9_bind_ids = fields.One2many(
        string='Five9 Bindings',
        comodel_name='five9.call',
        inverse_name='odoo_id',
    )


class Five9Call(models.Model):

    _name = 'five9.call'
    _inherit = 'five9.binding'
    _inherits = {'project.task': 'odoo_id'}
    _description = 'Five9 Calls'

    _rec_name = 'name'

    odoo_id = fields.Many2one(
        string='Issue',
        comodel_name='project.task',
        required=True,
        ondelete='cascade',
    )
    campaign_id = fields.Many2one(
        string='Campaign',
        comodel_name='five9.campaign',
        required=True,
    )
    disposition_id = fields.Many2one(
        string='Disposition',
        comodel_name='five9.disposition',
    )
    skill_id = fields.Many2one(
        string='Skill',
        comodel_name='five9.skill',
    )
    ani = fields.Char(
        string='ANI',
    )
    dnis = fields.Char(
        string='DNIS',
    )
    call_length = fields.Char()
    handle_time = fields.Char()
    wrapup_time = fields.Char()
    timestamp_start = fields.Datetime()
    timestamp_end = fields.Datetime()
    session_id = fields.Char()
    type = fields.Char()
    queue_time = fields.Char()
    hold_time = fields.Char()
    park_time = fields.Char()
    bill_time = fields.Char()
    number = fields.Char()
    media_type = fields.Char()
    tcpa_date_of_consent = fields.Datetime()
    language = fields.Char()
