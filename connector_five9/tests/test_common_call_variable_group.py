# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase


class TestCommonCallVariableGroup(Five9SyncTestCase):

    def setUp(self):
        super(TestCommonCallVariableGroup, self).setUp()
        self.model = self.env['five9.call.variable.group']
        self.record = self.model.create({
            'name': 'Call',
        })

    def test_compute_bind_model_name(self):
        """It should compute the bind model for the type."""
        self.assertEqual(self.record.bind_model_name, 'five9.call')
