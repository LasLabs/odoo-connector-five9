# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import fields, _
from odoo.addons.component.core import AbstractComponent
from odoo.addons.connector.exception import IDMissingInBackend
from odoo.addons.queue_job.exception import NothingToDoJob


_logger = logging.getLogger(__name__)


class Five9Importer(AbstractComponent):
    """ Base importer for Five9 """

    _name = 'five9.importer'
    _inherit = ['base.importer', 'base.five9.connector']
    _usage = 'record.importer'

    def __init__(self, work_context):
        super(Five9Importer, self).__init__(work_context)
        self.external_id = None
        self.five9_record = None

    def _get_five9_data(self):
        """Return the raw Five9 data for ``self.external_id``."""
        return self.backend_adapter.read(self.external_id)

    def _before_import(self):
        """Hook called before the import, when we have the Five9 data."""
        return

    def _is_up_to_date(self, binding):
        """Return True if the data is already up to date in Odoo."""
        assert self.five9_record
        if not hasattr(self.five9_record, 'modified_at'):
            return  # no update date on Five9, always import it.
        if not binding:
            return  # it does not exist so it should not be skipped
        sync = binding.sync_date
        if not sync:
            return
        sync_date = fields.Datetime.from_string(sync)
        five9_date = self.five9_record.modified_at
        # if the last synchronization date is greater than the last
        # update in five9, we skip the import.
        # Important: at the beginning of the exporters flows, we have to
        # check if the five9_date is more recent than the sync_date
        # and if so, schedule a new import. If we don't do that, we'll
        # miss changes done in Five9.
        return five9_date < sync_date

    def _import_dependency(self, external_id, binding_model,
                           importer=None, always=False):
        """Import a dependency.

        Args:
            external_id (int): ID of the external record to import.
            binding_model (basestring): Name of the model to bind to.
            importer (AbstractComponent, optional): Importer to use.
            always (bool, optional): Always update the record, regardless
                of if it exists in Odoo already. Note that if the record
                hasn't changed, it still may be skipped.
        """
        if not external_id:
            return
        binder = self.binder_for(binding_model)
        if always or not binder.to_internal(external_id):
            if importer is None:
                importer = self.component(usage='record.importer',
                                          model_name=binding_model)
            try:
                importer.run(external_id)
            except NothingToDoJob:
                _logger.info(
                    'Dependency import of %s(%s) has been ignored.',
                    binding_model._name, external_id
                )

    def _import_dependencies(self):
        """Import the dependencies for the record.

        Import of dependencies can be done manually or by calling
        :meth:`_import_dependency` for each dependency.
        """
        return

    def _map_data(self):
        """Returns an instance of
        :py:class:`~odoo.addons.connector.components.mapper.MapRecord`
        """
        return self.mapper.map_record(self.five9_record)

    def _validate_data(self, data):
        """Check if the values to import are correct.

        Pro-actively check before the ``_create`` or
        ``_update`` if some fields are missing or invalid.

        Raises:
            InvalidDataError: In the event of a validation error
        """
        return

    def _must_skip(self):
        """Hook called right after we read the data from the backend.
        If the method returns a message giving a reason for the
        skipping, the import will be interrupted and the message
        recorded in the job (if the import is called directly by the
        job, not by dependencies).
        If it returns None, the import will continue normally.
        :returns: None | str | unicode
        """
        return

    def _get_binding(self):
        return self.binder.to_internal(self.external_id)

    def _create_data(self, map_record, **kwargs):
        return map_record.values(for_create=True, **kwargs)

    def _create(self, data):
        """Create the Odoo record. """
        # special check on data before import
        self._validate_data(data)
        model = self.model.with_context(connector_no_export=True)
        binding = model.create(data)
        _logger.debug(
            '%d created from five9 %s', binding, self.external_id,
        )
        return binding

    def _update_data(self, map_record, **kwargs):
        return map_record.values(**kwargs)

    def _update(self, binding, data):
        """Update an Odoo record."""
        # special check on data before import
        self._validate_data(data)
        binding.with_context(connector_no_export=True).write(data)
        _logger.debug(
            '%d updated from five9 %s', binding, self.external_id,
        )
        return

    def _after_import(self, binding):
        """Hook called at the end of the import."""
        return

    def run(self, external_id, force=False, external_record=None):
        """Run the synchronization.

        Args:
            external_id (int | five9.BaseModel): identifier of the
                record in Five9, or a Five9 record.
            force (bool, optional): Set to ``True`` to force the sync.
            external_record (five9.models.BaseModel): Record from
                Five9. Defining this will force the import of this
                record, instead of the search of the remote.

        Returns:
            str: Canonical status message.
        """

        self.external_id = external_id
        lock_name = 'import({}, {}, {}, {})'.format(
            self.backend_record._name,
            self.backend_record.id,
            self.work.model_name,
            external_id,
        )

        if external_record is not None:
            self.five9_record = external_record
        else:
            try:
                self.five9_record = self._get_five9_data()
            except IDMissingInBackend:
                return _('Record no longer exists in Five9.')

        skip = self._must_skip()
        if skip:
            return skip

        binding = self._get_binding()

        if not force and self._is_up_to_date(binding):
            return _('Already up to date.')

        # Keep a lock on this import until the transaction is committed.
        # The lock is kept since we have detected that the information
        # will be updated in Odoo.
        self.advisory_lock_or_retry(lock_name)
        self._before_import()

        # import the missing linked resources
        self._import_dependencies()

        map_record = self._map_data()

        if binding:
            record = self._update_data(map_record)
            self._update(binding, record)
        else:
            record = self._create_data(map_record)
            binding = self._create(record)

        self.binder.bind(self.external_id, binding)

        self._after_import(binding)

        return _('Import complete.')


class BatchImporter(AbstractComponent):
    """The role of a BatchImporter is to search for a list of
    items to import, then it can either import them directly or delay
    the import of each item separately.
    """

    _name = 'five9.batch.importer'
    _inherit = ['base.importer', 'base.five9.connector']
    _usage = 'batch.importer'

    def run(self, filters=None):
        """Run the synchronization."""
        record_ids = self.backend_adapter.search(filters)
        for record_id in record_ids:
            self._import_record(record_id)

    def _import_record(self, external_id):
        """Import a record directly or delay import, TBD by subclass logic.

        This should be implemented in subclasses.
        """
        raise NotImplementedError


class DirectBatchImporter(AbstractComponent):
    """Import the records directly (no delay)."""

    _name = 'five9.direct.batch.importer'
    _inherit = 'five9.batch.importer'

    def _import_record(self, external_id, **kwargs):
        """Import the record directly."""
        self.model.import_record(self.backend_record, external_id, **kwargs)


class DelayedBatchImporter(AbstractComponent):
    """Schedule a delayed import of the records."""

    _name = 'five9.delayed.batch.importer'
    _inherit = 'five9.batch.importer'

    def _import_record(self, external_id, job_options=None, **kwargs):
        """Delay the record imports."""
        delayed = self.model.with_delay(**job_options or {})
        delayed.import_record(self.backend_record, external_id, **kwargs)
