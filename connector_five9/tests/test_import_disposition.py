# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase, recorder


class TestImportDisposition(Five9SyncTestCase):

    EXISTING_DISPOSITIONS = 38

    def setUp(self):
        super(TestImportDisposition, self).setUp()
        self.model = self.env['five9.disposition']

    @recorder.use_cassette
    def _import_dispositions(self):
        self.model.import_batch(self.backend)
        return self.model.search([('backend_id', '=', self.backend.id)])

    def test_import_disposition_batch(self):
        """It should import all of the dispositions using batch import."""
        self.assertEqual(len(self._import_dispositions()),
                         self.EXISTING_DISPOSITIONS)
