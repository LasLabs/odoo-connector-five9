# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase, recorder


class TestImportCallVariableGroup(Five9SyncTestCase):

    EXISTING_CALL_VARIABLE_GROUPS = 4

    def setUp(self):
        super(TestImportCallVariableGroup, self).setUp()
        self.model = self.env['five9.call.variable.group']

    @recorder.use_cassette
    def _import_call_variable_groups(self):
        self.model.import_batch(self.backend)
        return self.model.search([('backend_id', '=', self.backend.id)])

    def test_import_call_variable_group_batch(self):
        """It should import all of the call var groups using batch import."""
        self.assertEqual(len(self._import_call_variable_groups()),
                         self.EXISTING_CALL_VARIABLE_GROUPS)
