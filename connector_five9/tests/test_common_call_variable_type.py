# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime

from .common import Five9SyncTestCase


class TestCommonCallVariableType(Five9SyncTestCase):

    def setUp(self):
        super(TestCommonCallVariableType, self).setUp()
        self.model = self.env['five9.call.variable.type']
        self.record = self.model.create({
            'name': 'Datetime Field',
            'deserialize': 'fields.Datetime.from_string(value)',
        })

    def test_action_deserialize(self):
        """It should deserialize into the proper datetime."""
        expect = datetime(2017, 1, 2)
        res = self.record.action_deserialize('2017-01-02')
        self.assertIsInstance(res, datetime)
        self.assertEqual(res, expect)
