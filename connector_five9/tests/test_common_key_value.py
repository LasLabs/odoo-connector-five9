# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase


class TestCommonKeyValue(Five9SyncTestCase):

    def setUp(self):
        super(TestCommonKeyValue, self).setUp()
        self.model = self.env['five9.key.value']
        self.record = self.model.create({
            'key': 'Test',
            'value': 'Value',
        })

    def test_five9_dict(self):
        self.assertDictEqual(
            self.record.five9_dict,
            {'key': self.record.key, 'value': self.record.value},
        )

    def test_upsert_creates(self):
        """It should create a new key/value pair."""
        self.assertTrue(self.model.upsert('key', 'value'))

    def test_upsert_uses_existing(self):
        """It should use existing key/value pairs."""
        self.assertEqual(
            self.model.upsert(self.record.key, self.record.value),
            self.record,
        )
