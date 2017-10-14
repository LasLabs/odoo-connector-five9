# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase, recorder


class TestImportWebConnector(Five9SyncTestCase):

    EXISTING_WEB_CONNECTORS = 1

    def setUp(self):
        super(TestImportWebConnector, self).setUp()
        self.model = self.env['five9.web.connector']

    @recorder.use_cassette
    def _import_web_connectors(self):
        self.model.import_batch(self.backend)
        return self.model.search([('backend_id', '=', self.backend.id)])

    def test_import_web_connector_batch(self):
        """It should import all of the web connectors using batch import."""
        self.assertEqual(len(self._import_web_connectors()),
                         self.EXISTING_WEB_CONNECTORS)
