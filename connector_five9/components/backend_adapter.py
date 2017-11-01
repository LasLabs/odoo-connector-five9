# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from uuid import uuid4

from odoo import _

from odoo.addons.component.core import AbstractComponent

_logger = logging.getLogger(__name__)

try:
    from zeep.helpers import serialize_object
except ImportError:
    _logger.debug("`zeep` Python library not installed.")

try:
    from five9 import Five9
except ImportError:
    _logger.debug("`five9` Python library not installed.")


class Five9Api(object):
    def __new__(cls, username, password, *args, **kwargs):
        return Five9(username, password)


class Five9CRUDAdapter(AbstractComponent):

    _name = 'five9.crud.adapter'
    _inherit = ['base.backend.adapter', 'base.five9.connector']
    _usage = 'backend.adapter'

    UID_FIELD = 'name'
    _five9 = None

    @property
    def five9(self):
        """Return the Five9 API for use."""
        try:
            return getattr(self.work, 'five9_api')
        except AttributeError:
            raise AttributeError(_(
                'You must provide a `five9_api` attribute to be able '
                'to use this Backend Adapter.',
            ))

    # pylint: disable=W8106
    def read(self, external_id):
        """Return the record from the remote.

        This is a default implementation that uses ``search_read``.

        Args:
            external_id (int): The ID on the remote. Five9 doesn't actually
                have a concept of an ID though, so this is the UID that was
                created for tracking.
        """
        results = self.search_read({
            self.UID_FIELD: external_id,
        })
        for result in results:
            return result

    def search(self, filters):
        """``filters`` should conform to ``Five9.create_criteria``."""
        return [
            r[self.UID_FIELD] for r in self.search_read(filters)
        ]

    # pylint: disable=W8106
    def create(self, data):
        """Create the web connector on the remote.

        Args:
            data (dict): The data dictionary to create on remote.
        """
        raise NotImplementedError

    # pylint: disable=W8106
    def write(self, external_id, data):
        """Update a record on the remote.

        Args:
            data (dict): A dictionary representing the record data.
        """
        raise NotImplementedError

    def delete(self, external_id):
        raise NotImplementedError

    def new_uuid(self):
        return str(uuid4())

    def create_meta_fields(self):
        """Create the fields necessary for operation.

        Child modules should inherit and override this if needed.
        """
        pass

    def create_web_connector(self):
        """Create the web connector for this model.

        Child modules should inherit and override this if needed.
        """
        pass

    def _serialize(self, zeep_object):
        return serialize_object(zeep_object)


class Five9Adapter(AbstractComponent):

    _name = 'five9.adapter'
    _inherit = 'five9.crud.adapter'

    # Declare in children - either ``configuration`` or ``supervisor``
    _five9_api = None

    @property
    def endpoint(self):
        """Return a usable endpoint for the API."""
        return getattr(self.five9, self._five9_api)
