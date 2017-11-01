# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase


class TestCommonCallVariable(Five9SyncTestCase):

    def setUp(self):
        super(TestCommonCallVariable, self).setUp()
        self.model = self.env['five9.call.variable']
        self.variable_type = self.env['five9.call.variable.type'].create({
            'name': 'INTEGER',
            'backend_id': self.backend.id,
        })
        self.group_call = self.env['five9.call.variable.group'].create({
            'name': 'Call',
            'backend_id': self.backend.id,
        })
        self.group_customer = self.env['five9.call.variable.group'].create({
            'name': 'Customer',
            'backend_id': self.backend.id,
        })
        self.record_call = self.model.create({
            'name': 'call',
            'description': 'Test Call Variable',
            'type_id': self.variable_type.id,
            'group_id': self.group_call.id,
            'backend_id': self.backend.id,
        })
        self.record_customer = self.model.create({
            'name': 'customer',
            'description': 'Test Customer Variable',
            'type_id': self.variable_type.id,
            'group_id': self.group_customer.id,
            'backend_id': self.backend.id,
        })

    def test_get_data(self):
        """It should return the type-casted dataset."""
        data = {'customer': 1, 'call': 2}
        res = self.model.search([])._get_data(data)
        for key, val in res.items():
            self.assertEqual(val, str(data[key]))

    def test_get_grouped(self):
        """It should return a dict of variables for the backend by group."""
        res = self.model._get_grouped(self.backend)
        expect = {
            self.group_call: self.record_call,
            self.group_customer: self.record_customer,
        }
        self.assertDictEqual(res, expect)

    def test_get_grouped_name(self):
        """It should only return the attributes in the dictionary."""
        res = self.model._get_grouped(self.backend, {'customer': 1})
        expect = {
            self.group_customer: self.record_customer,
        }
        self.assertDictEqual(res, expect)
