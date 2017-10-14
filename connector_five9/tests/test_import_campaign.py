# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase, recorder


class TestImportCampaign(Five9SyncTestCase):

    EXISTING_CAMPAIGNS = 1

    def setUp(self):
        super(TestImportCampaign, self).setUp()
        self.model = self.env['five9.campaign']

    @recorder.use_cassette
    def _import_campaigns(self):
        self.model.import_batch(self.backend)
        return self.model.search([('backend_id', '=', self.backend.id)])

    def test_import_campaign_batch(self):
        """It should import all of the campaigns using batch import."""
        self.assertEqual(len(self._import_campaigns()),
                         self.EXISTING_CAMPAIGNS)
