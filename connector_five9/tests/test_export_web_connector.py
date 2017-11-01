# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from contextlib import contextmanager

from .common import Five9SyncTestCase, recorder


class TestExportWebConnector(Five9SyncTestCase):

    def setUp(self):
        super(TestExportWebConnector, self).setUp()
        self.model = self.env['five9.web.connector']

    @contextmanager
    def _create_web_connector(self, export=True):
        """Create a connector and delete from the remote when done."""

        model = self.model.with_context(connector_no_export=True)
        self.connector_vals = self.backend._get_hook_vals(
            'OnCallDispositioned',
        )

        try:
            self.connector = model.create(self.connector_vals)
            if export:
                self.connector.export_record()
            yield self.connector
        finally:
            if export:
                with self.backend.work_on(self.model._name) as work:
                    adapter = work.component(usage='backend.adapter')
                    adapter.delete(self.connector.external_id)

    @recorder.use_cassette
    def test_export_and_delete_connector(self):
        """It should export and delete the connector on Five9."""
        with self._create_web_connector() as connector:
            external_id = connector.external_id
            self.assertTrue(self._get_external(external_id))
        self.assertFalse(self._get_external(external_id))
