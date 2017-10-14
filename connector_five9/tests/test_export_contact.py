# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from contextlib import contextmanager
from time import sleep

from .common import Five9SyncTestCase, recorder


class TestExportContact(Five9SyncTestCase):

    def setUp(self):
        super(TestExportContact, self).setUp()
        self.model = self.env['five9.contact']
        self.partner_vals = {
            'firstname': 'New',
            'lastname': 'Test',
            'phone': '3456789012',
            'mobile': '8765432109',
            'fax': '6473829105',
            'street': '321 Fake Ave',
            'city': 'Test Town',
            'state_id': self.env.ref('base.state_us_23').id,
            'zip': '54321',
            'backend_id': self.backend.id,
        }

    @contextmanager
    def _create_contact(self, export=True):
        """Create a contact and delete from the remote when done."""

        model = self.model.with_context(connector_no_export=True)

        try:
            self.partner = model.create(self.partner_vals)
            if export:
                self.partner.export_record()
            yield self.partner
        finally:
            if export:
                with self.backend.work_on(self.model._name) as work:
                    adapter = work.component(usage='backend.adapter')
                    adapter.delete(self.partner.external_id)

    @recorder.use_cassette
    def test_export_and_delete_contact(self):
        """It should export and delete the contact on Five9."""
        with self._create_contact() as contact:
            external_id = contact.external_id
            self.assertTrue(self._get_external(external_id))
        sleep(3)  # The delete is async on Five9
        self.assertFalse(self._get_external(external_id))
