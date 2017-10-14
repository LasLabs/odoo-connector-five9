# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class Five9AdapterWebConnector(Component):

    _name = 'five9.adapter.web.connector'
    _inherit = 'five9.adapter'
    _apply_on = 'five9.web.connector'

    # pylint: disable=W8106
    def create(self, data):
        """Create the web connector on the remote.

        Args:
            data (dict): The data dictionary to create on remote.
        """
        return self.five9.env.WebConnector.create(data)

    def delete(self, name):
        """Delete the web connector.

        Args:
            name (str): The name of the connector.
        """
        connector = self.five9.env.WebConnector.new({'name': name})
        return connector.delete()

    def search_read(self, filters):
        """Search for data by filters and return the result.

        Args:
            filters (dict): A dictionary of search strings, keyed by the name
                of the field to search.

        Returns:
            five9.environment.Environment: An environment representing the
                recordset.
        """
        return self.five9.env.WebConnector.search(filters)

    # pylint: disable=W8106
    def write(self, external_id, data):
        """Update a record on the remote.

        Args:
            external_id (mixed): The ID on the remote.
            data (dict): A dictionary representing the record data.
        """
        data[self.five9.env.WebConnector.__uid_field__] = external_id
        record = self.five9.env.WebConnector.new(data)
        record.write()
        return record
