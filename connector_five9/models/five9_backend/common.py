# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from contextlib import contextmanager

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from odoo.addons.connector.checkpoint import checkpoint
from ...components.backend_adapter import Five9Api


_logger = logging.getLogger(__name__)


class Five9Backend(models.Model):

    _name = 'five9.backend'
    _description = 'Five9 Backend'
    _inherit = 'connector.backend'

    HOOK_FIELD_SECRET = '__odoo_secret__'

    version = fields.Selection(
        selection='_get_versions',
        default='v1',
        required=True,
    )
    username = fields.Char(
        required=True,
    )
    password = fields.Char(
        required=True,
    )
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=True,
        default=lambda s: s.env.user.company_id.id,
    )
    project_id = fields.Many2one(
        string='Project',
        comodel_name='project.project',
        required=True,
        help='This is the project that Five9 issues will be created in. '
             'Note that once created, the project is disassociated from '
             'automation and can be updated on the issue as desired.',
    )
    web_hook_ids = fields.One2many(
        string='Web Hook',
        comodel_name='five9.web.connector',
        inverse_name='backend_id',
        readonly=True,
    )
    disposition_ids = fields.One2many(
        string='Dispositions',
        comodel_name='five9.disposition',
        inverse_name='backend_id',
        readonly=True,
    )
    is_default_export = fields.Boolean(
        string='Default Exporter?',
        help='Check to indicate this is the default Five9 connector '
             'that should be used for exporting records created in Odoo for '
             'this company, that are not otherwise assigned to a Five9 '
             'backend.',
    )
    is_setup_complete = fields.Boolean(
        help='This indicates that setup has been completed on the backend.',
    )

    @property
    @api.model
    def default_exporter(self):
        """Return the default exporter for the current company."""
        return self.search([
            ('company_id', '=', self.env.user.company_id.id),
            ('is_default_export', '=', True),
        ])

    @api.model
    def _get_versions(self):
        """Available versions for this backend."""
        return [('v1', 'v1')]

    @api.multi
    @api.constrains('company_id', 'is_default_export')
    def _check_company_id_is_default_export(self):
        """Only allow one default exporter per company."""
        for record in self.filtered(lambda r: r.is_default_export):
            domain = [
                ('company_id', '=', record.company_id.id),
                ('is_default_export', '=', True),
            ]
            if len(self.search(domain)) > 1:
                raise ValidationError(_(
                    'You cannot have two default Five9 exporters for the '
                    'same company.',
                ))

    @api.multi
    @contextmanager
    def work_on(self, model_name, **kwargs):
        """Context manager providing a usable API for external access.

        Yields:
            odoo.addons.component.core.WorkContext: The worker context for
                this backend record. The ``Five9`` object is exposed on
                the ``five9_api`` attribute of this context.
        """
        self.ensure_one()
        five9_api = Five9Api(self.username, self.password)
        # From the components, we can do ``self.work.five9_api``
        with super(Five9Backend, self).work_on(
            model_name, five9_api=five9_api, **kwargs
        ) as work:
            yield work

    @api.multi
    def add_checkpoint(self, record):
        self.ensure_one()
        record.ensure_one()
        return checkpoint.add_checkpoint(
            self.env, record._name, record.id, self._name, self.id,
        )

    @api.multi
    def setup_meta(self):
        """Create the metadata columns in Five9 that are necessary for sync.
        """
        for backend in self:
            self.env['five9.contact'].create_meta_fields(backend)

    @api.multi
    def action_create_hooks(self):
        """Create the web hooks that are necessary to receive stuff."""
        for record in self:
            triggers = self.env['five9.web.connector']._get_triggers()
            for trigger in triggers:
                self.env['five9.web.connector'].create(
                    record._get_hook_vals(trigger[0]),
                )

    @api.multi
    def action_do_setup(self):
        """Setup the backend.

        Creates the customer meta fields, creates necessary web hooks,
        schedules initial record syncs.
        """
        self.ensure_one()
        if self.is_setup_complete:
            raise ValidationError(_(
                'You should not perform setup on a backend more than once.',
            ))
        self.setup_meta()

        self.env['five9.disposition'].import_batch(self)
        self.env['five9.call.variable'].import_batch(self)

        self.action_create_hooks()

        self.env['five9.skill'].with_delay().import_batch(self)
        self.env['five9.contact'].with_delay().import_batch(self)
        self.is_setup_complete = True
        return True

    @api.multi
    def action_delete_hooks(self):
        for record in self:
            record.web_hook_ids.unlink()

    @api.multi
    def _get_hook_vals(self, trigger):
        """Return the values for creating/updating a hook."""
        self.ensure_one()
        description = '%s for the %s connector on %s\'s Odoo.' % (
            trigger, self.name, self.company_id.name,
        )
        name = '%s - %s' % (self.name, trigger)
        secret = self.env['web.hook']._default_secret()
        secret_post_constant = {
            'key': self.HOOK_FIELD_SECRET,
            'value': secret,
        }
        # This is required to create a connector for some reason
        variable = self.env['five9.key.value'].upsert(
            '_customer_id', 'Customer._record_id',
        )
        values = {
            # Standard hook data:
            'interface_type': 'five9.web.connector',
            'token_type': 'web.hook.token.plain',
            'token_secret': secret,
            'backend_id': self.id,
            'add_worksheet': True,
            'agent_application': 'EmbeddedBrowser',
            'clear_trigger_dispositions': True,
            'cti_web_services': 'CurrentBrowserWindow',
            'execute_in_browser': True,
            'is_post': True,
            'start_page_text': 'Please wait - Odoo connection is loading.',

            # Trigger specific data:
            'name': name,
            'description': description,
            'trigger': trigger,
            'post_variable_ids': [(6, 0, self._get_worksheet_vars().ids)],
            'post_constant_ids': [(0, 0, secret_post_constant)],
            'constant_ids': [(5, 0)],
            'variable_ids': [(6, 0, variable.ids)],
        }
        # Listen on all dispositions
        if trigger == 'OnCallDispositioned':
            values['trigger_disposition_ids'] = [
                (6, 0, self.disposition_ids.ids),
            ]
        _logger.debug('Hook values %s', values)
        return values

    @api.multi
    def _get_worksheet_vars(self):
        self.ensure_one()
        grouped_variables = self.env['five9.call.variable']._get_grouped(self)
        results = self.env['five9.key.value'].browse()
        for group, variables in grouped_variables.items():
            for variable in variables:
                results += results.upsert(
                    variable.name, '%s.%s' % (group.name, variable.name),
                )
        return results

    # Import actions
    @api.multi
    def action_import_mailboxes(self):
        """Trigger an import for mailboxes on the appropriate from field."""
        self.import_from_date('five9.mailbox',
                              'import_mailboxes_from_date')

    @api.multi
    def action_import_contacts(self):
        """Trigger an import for contacts on the appropriate from field."""
        self.import_from_date('five9.contact',
                              'import_contacts_from_date')
