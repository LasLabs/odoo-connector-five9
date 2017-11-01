|License AGPL-3| | |Build Status| | |Test Coverage|

===============
Five9 Connector
===============

This module allows for you to synchronize Odoo and Five9 in the following
capacities:

+---------------------+--------+--------+--------+
| Object              | Import | Export | Delete |
+=====================+========+========+========+
| Agent               | Yes    | No     | No     |
+---------------------+--------+--------+--------+
| Agent Group         | Yes    | No     | No     |
+---------------------+--------+--------+--------+
| Call                | Yes    | No     | No     |
+---------------------+--------+--------+--------+
| Call Variable       | Yes    | No     | No     |
+---------------------+--------+--------+--------+
| Call Variable Group | Yes    | No     | No     |
+---------------------+--------+--------+--------+
| Campaign            | Yes    | No     | No     |
+---------------------+--------+--------+--------+
| Contact             | Yes    | Yes    | No     |
+---------------------+--------+--------+--------+
| Disposition         | Yes    | Yes    | No     |
+---------------------+--------+--------+--------+
| Skill               | Yes    | No     | No     |
+---------------------+--------+--------+--------+
| Web Connector       | Yes    | Yes    | No     |
+---------------------+--------+--------+--------+

Installation
============

To install this module, you need to:

#. Follow `queue_job <https://github.com/OCA/queue/tree/10.0/queue_job#installation>`_
   install instructions.

Configuration
=============

To configure this module, you need to:

#. Go to Connectors => [Five9] Backends
#. Create a new backend. Note that the name must be unique, and cannot be shared
   with other remote Five9 connectors. This is because the web hooks are created
   using this name, so remote systems that are named the same will conflict
   silently.
#. Click ``Initialize Backend`` to setup the hooks on Five9, setup any meta fields,
   and perform an initial data import.
#. Restart Odoo (this is required for the async job queue)

Known Issues / Road Map
=======================

* Backend should use an adapter for web hook processing
* Web hooks are not updated when dispositions are created/edited
* The web connectors must be manually assigned to campaigns in the Five9
  administration console due to a limitation in the API. This is done in
  the campaign configuration screen in the Five9 administration UI.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/LasLabs/odoo-connector-five9/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Dave Lasley <dave@laslabs.com>

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://laslabs.com/logo.png
   :alt: LasLabs Inc.
   :target: https://laslabs.com

This module is maintained by LasLabs Inc.


.. |Build Status| image:: https://img.shields.io/travis/LasLabs/odoo-connector-five9/master.svg
   :target: https://travis-ci.org/LasLabs/odoo-connector-five9
.. |Test Coverage| image:: https://img.shields.io/codecov/c/github/LasLabs/odoo-connector-five9/master.svg
   :target: https://codecov.io/gh/LasLabs/odoo-connector-five9
.. |License AGPL-3| image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3
