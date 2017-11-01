# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase, recorder


class TestImportContact(Five9SyncTestCase):

    def setUp(self):
        super(TestImportContact, self).setUp()
        self.model = self.env['five9.contact']
        self.expect = {
            'first_name': 'Test',
            'last_name': 'User',
            'number1': '2345678901',
            'number2': '9876543210',
            'number3': '5647382910',
            'street': '123 Test St',
            'city': 'Testerville',
            'state': self.env.ref('base.state_us_23').code,
            'zip': '12345',
            'backend_date_created': None,
            'backend_date_modified': None,
        }

    def _import_batch(self):
        self.model.import_batch(self.backend,
                                {'number1': self.expect['number1']},
                                )
        partner = self.model.search([('phone', '=', self.expect['number1']),
                                     ('backend_id', '=', self.backend.id)])
        return partner

    def _get_fields(self):
        with self.backend.work_on(self.model._name) as work:
            adapter = work.component(usage='backend.adapter')
            fields = adapter._get_contact_fields()
            meta_names = [m['name'] for m in adapter.META_FIELDS]
        return fields, meta_names

    @recorder.use_cassette
    def test_contact_meta_fields(self):
        """It should have inserted the meta fields into contact fields."""

        fields, meta_names = self._get_fields()
        for meta_name in meta_names:
            self.assertNotIn(meta_name, fields)

        self.model.create_meta_fields(self.backend)

        fields, meta_names = self._get_fields()
        for meta_name in meta_names:
            self.assertIn(meta_name, fields)

    @recorder.use_cassette
    def test_import_contact_batch(self):
        """It should import the test contact using batch import."""
        self.assertTrue(self._import_batch())

    @recorder.use_cassette
    def test_import_contact_writes_odoo_id(self):
        """It should write the new Odoo ID to the external record."""
        partner = self._import_batch()
        self.assertTrue(self._get_external(partner.external_id))

    @recorder.use_cassette
    def test_import_contact_existing_partner(self):
        """It should bind to existing partner with same info."""
        partner = self.env['res.partner'].with_context(
            connector_no_export=True,
        ).create({
            'firstname': self.expect['first_name'],
            'lastname': self.expect['last_name'],
            'phone': self.expect['number1'],
        })
        binding = self._import_batch()
        self.assertEqual(binding.odoo_id, partner)
