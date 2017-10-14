# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

from odoo.addons.queue_job.job import job

_logger = logging.getLogger(__name__)

try:
    from five9.models import WebConnector
except ImportError:
    _logger.debug("`five9` Python library not installed.")


class Five9WebConnector(models.Model):

    _name = 'five9.web.connector'
    _inherit = ['five9.binding', 'web.hook.adapter']
    _description = 'Web Hook - Five9'

    interface_type = fields.Selection(
        default='five9.web.connector',
    )
    token_type = fields.Selection(
        default='web.hook.token.none',
    )
    token_secret = fields.Char(
        default='',
    )
    add_worksheet = fields.Boolean(
        help='Applies only to POST requests. Whether to pass worksheet '
             'answers as parameters.',
    )
    agent_application = fields.Selection([
        ('EmbeddedBrowser', 'Embedded browser window.'),
        ('ExternalBrowser', 'External browser window.'),
    ],
        default='EmbeddedBrowser',
        required=True,
        help='If execute in browser, this parameter specifies whether '
             'to open the URL in an external or an embedded browser.',
    )
    clear_trigger_dispositions = fields.Boolean(
        help='When modifying an existing connector, whether to clear the '
             'existing triggers.',
    )
    constant_ids = fields.Many2many(
        string='Constants',
        comodel_name='five9.key.value',
        relation='five9_key_value_five9_web_connector_rel_constant_ids',
        help='Parameters passed with constant values.',
    )
    cti_web_services = fields.Selection([
        ('CurrentBrowserWindow', 'Current browser window.'),
        ('NewBrowserWindow', 'New browser window.'),
    ],
        default='CurrentBrowserWindow',
        required=True,
        help='In the Internet Explorer toolbar, whether to open the HTTP '
             'request in the current or a new browser window.',
    )
    description = fields.Char(
        help='Purpose of the connector.',
    )
    execute_in_browser = fields.Boolean(
        help='When enabling the agent to view or enter data, whether to '
             'open the URL in an embedded or external browser window.',
    )
    post_constant_ids = fields.Many2many(
        string='Post Constants',
        comodel_name='five9.key.value',
        relation='five9_key_value_five9_web_connector_rel_post_constant_ids',
        help='When using the POST method, constant parameters to pass in '
             'the URL.'
    )
    is_post = fields.Boolean(
        string='Use Post',
        help='Whether the HTTP request type is POST.',
    )
    post_variable_ids = fields.Many2many(
        string='Post Variables',
        comodel_name='five9.key.value',
        relation='five9_key_value_five9_web_connector_rel_post_variable_ids',
        help='When using the POST method, variable parameters to pass in '
             'the URL.',
    )
    start_page_text = fields.Char(
        help='When using the POST method, enables the administrator to enter '
             'text to be displayed in the browser (or agent Browser tab) '
             'while waiting for the completion of the connector.',
    )
    trigger = fields.Selection(
        selection=lambda s: s._get_triggers(),
        required=True,
        help='Available trigger during a call when the request is sent.',
    )
    trigger_disposition_ids = fields.Many2many(
        string='Trigger Dispositions',
        comodel_name='five9.disposition',
        help='When the trigger is OnCallDispositioned, specifies the trigger '
             'dispositions. White space separated list.',
    )
    trigger_dispositions_list = fields.Serialized(
        compute='_compute_trigger_dispositions_list',
        inverse='_inverse_trigger_dispositions_list',
    )
    variable_ids = fields.Many2many(
        string='Variables',
        relation='five9_key_value_five9_web_connector_rel_variable_ids',
        comodel_name='five9.key.value',
        help='When using the POST method, connectors can include worksheet '
             'data as parameter values. The variable placeholder values are '
             'surrounded by @ signs. For example, the parameter ANI has the '
             'value `@Call.ANI@`.',
    )

    @api.multi
    @api.depends('trigger_disposition_ids')
    def _compute_trigger_dispositions_list(self):
        """Return a list of trigger dispositions."""
        for record in self:
            dispositions = record.trigger_disposition_ids.mapped('name')
            record.trigger_dispositions_list = dispositions

    @api.multi
    def _inverse_trigger_dispositions_list(self):
        for record in self.filtered(lambda r: r.trigger_dispositions_list):
            dispositions = self.env['five9.disposition'].search([
                ('backend_id', '=', record.backend_id.id),
                ('name', 'in', record.trigger_dispositions_list),
            ])
            record.disposition_ids = [(6, 0, dispositions.ids)]

    @api.model
    def _get_triggers(self):
        triggers = WebConnector._props['trigger'].descriptions
        return [
            (n, '[%s] %s' % (n, desc)) for n, desc in triggers.items()
        ]

    @api.multi
    @job(default_channel='root.five9')
    def receive(self, data, headers):
        """Receive the authenticated data.

        Args:
            data (dict): Data that was received with the hook.
            headers (dict): Headers that were received with the request.
        """

        grouped_variables = self.env['five9.call.variable']._get_grouped(data)

        for group, variables in grouped_variables:

            if not group.bind_model_name:
                _logger.info(
                    'A bind model is not selected for the Five9 variable '
                    'group type "%s". Skipping.' % group.name,
                )
                continue

            self.env[group.bind_model_name].with_delay().import_direct(
                self.backend_id, variables._get_data(data),
            )

    @api.multi
    def extract_token(self, data, headers):
        """Extract the token from the data and return it.

        Args:
            data (dict): Data that was received with the hook.
            headers (dict): Headers that were received with the request.

        Returns:
            mixed: The token data. Should be compatible with the hook's token
                interface (the ``token`` parameter of ``token_id.validate``).
        """
        return data.get(self.backend_id.HOOK_FIELD_SECRET)
