# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from .common import Five9SyncTestCase, recorder


class TestImportSkill(Five9SyncTestCase):

    EXISTING_SKILLS = 1

    def setUp(self):
        super(TestImportSkill, self).setUp()
        self.model = self.env['five9.skill']

    @recorder.use_cassette
    def _import_skills(self):
        self.model.import_batch(self.backend)
        return self.model.search([('backend_id', '=', self.backend.id)])

    def test_import_skill_batch(self):
        """It should import all of the skills using batch import."""
        self.assertEqual(len(self._import_skills()),
                         self.EXISTING_SKILLS)
