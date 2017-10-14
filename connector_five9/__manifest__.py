# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# pylint: disable=C8101
{
    "name": "Five9 Connector",
    "summary": "Two way synchronization with Five9",
    "version": "10.0.1.0.0",
    "category": "Connector",
    "website": "https://github.com/LasLabs/odoo-connector_five9.git",
    "author": "LasLabs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": ['five9'],
    },
    "depends": [
        "base_web_hook",
        "connector",
        "sales_team",
        "partner_firstname",
        "project",
        "project_task_category",
        "queue_job",
    ],
    "data": [
        "data/five9_call_variable_type_data.xml",
        "security/ir.model.access.csv",
        "views/five9_backend_view.xml",
        "views/five9_call_variable_view.xml",
        "views/five9_web_connector_view.xml",
        # Menu must load last
        "views/connector_menu.xml",
    ],
}
