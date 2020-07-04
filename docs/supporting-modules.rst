##################
Supporting Modules
##################
This section provides details around the supporting modules used in the **khoros** package,
which are listed below.

* `Classes & Exceptions`_
    * `Errors Module (khoros.errors)`_
        * `Exceptions Module (khoros.errors.exceptions)`_
        * `Handlers Module (khoros.errors.handlers)`_
        * `Translations Module (khoros.errors.translations)`_
* `Tools & Utilities`_
    * `Core Utilities Module (khoros.utils.core_utils)`_
    * `Environment Module (khoros.utils.environment)`_
    * `Helper Module (khoros.utils.helper)`_
    * `Version Module (khoros.utils.version)`_
* `Unit Testing`_
    * `Tests Module (khoros.utils.tests)`_
        * `Resources Modules (khoros.utils.tests.resources)`_
        * `Test Board Creation Module (khoros.utils.tests.test_board_creation)`_
        * `Test Core Utilities Module (khoros.utils.tests.test_core_utils)`_
        * `Test Group Hub Creation Module (khoros.utils.tests.test_grouphub_creation)`_
        * `Test Helper File Module (khoros.utils.tests.test_helper_file)`_
        * `Test HTTP Headers Module (khoros.utils.tests.test_http_headers)`_
        * `Test Library Import Module (khoros.utils.tests.test_library_import)`_
        * `Test LiQL WHERE Parsing Module (khoros.utils.tests.test_liql_where_parsing)`_
        * `Test Mentions Module (khoros.utils.tests.test_mentions)`_
        * `Test Node ID Extract Module (khoros.utils.tests.test_node_id_extract)`_
        * `Test Tags Module (khoros.utils.tests.test_tags)`_

|

********************
Classes & Exceptions
********************
This section includes modules that contain the classes and exceptions used throughout the package.

|

Errors Module (khoros.errors)
=============================
This module contains all of the exception classes and error handling functions leveraged throughout the library.

.. automodule:: khoros.errors
   :members:

:doc:`Return to Top <supporting-modules>`

|

Exceptions Module (khoros.errors.exceptions)
--------------------------------------------
This sub-module contains all of the exception classes leveraged in functions throughout the library.

.. automodule:: khoros.errors.exceptions
   :members:

:doc:`Return to Top <supporting-modules>`

|

Handlers Module (khoros.errors.handlers)
----------------------------------------
This sub-module contains various error handling functions that are leveraged throughout the library.

.. automodule:: khoros.errors.handlers
   :members:

:doc:`Return to Top <supporting-modules>`

|

Translations Module (khoros.errors.translations)
------------------------------------------------
This sub-module provides more relevant translations for error messages in API responses where possible.

.. automodule:: khoros.errors.translations
   :members:

:doc:`Return to Top <supporting-modules>`

|

*****************
Tools & Utilities
*****************
This section includes modules that contain tools and utilities leveraged by other scripts.

|

Core Utilities Module (khoros.utils.core_utils)
===============================================
This module includes various utilities to assist in converting dictionaries to JSON,
formatting timestamps, etc.

.. automodule:: khoros.utils.core_utils
   :members:

:doc:`Return to Top <supporting-modules>`

|

Environment Module (khoros.utils.environment)
=============================================
This module identifies any environmental variables that have been defined for use within
the :py:mod:`khoros` library.

.. automodule:: khoros.utils.environment
   :members:

:doc:`Return to Top <supporting-modules>`

|

Helper Module (khoros.utils.helper)
===================================
This module allows a "helper" configuration file to be imported and parsed to
facilitate the use of the library (e.g. defining the base URL and API credentials) and
defining additional settings.

.. automodule:: khoros.utils.helper
   :members:

:doc:`Return to Top <supporting-modules>`

|

Version Module (khoros.utils.version)
=====================================
This module is the primary source of the current version of the khoros package, and includes two simple
functions to return either the full version or the major.minor (i.e. X.Y) version.

.. automodule:: khoros.utils.version
   :members:

:doc:`Return to Top <supporting-modules>`

|

************
Unit Testing
************
This section includes modules that are used in unit testing the library.

|

Tests Module (khoros.utils.tests)
=================================
This module includes unit tests for the package that are performed using pytest.

.. automodule:: khoros.utils.tests
   :members:

:doc:`Return to Top <supporting-modules>`

|

Resources Modules (khoros.utils.tests.resources)
------------------------------------------------
This module includes frequently used resources for performing unit testing.

.. automodule:: khoros.utils.tests.resources
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Board Creation Module (khoros.utils.tests.test_board_creation)
-------------------------------------------------------------------
This module is used by pytest to verify that that the board creation works properly.

.. automodule:: khoros.utils.tests.test_board_creation
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Core Utilities Module (khoros.utils.tests.test_core_utils)
---------------------------------------------------------------
This module is used by pytest to verify that the core package utilities work properly.

.. automodule:: khoros.utils.tests.test_core_utils
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Group Hub Creation Module (khoros.utils.tests.test_grouphub_creation)
--------------------------------------------------------------------------
This module is used by pytest to verify that that the group hub creation works properly.

.. automodule:: khoros.utils.tests.test_grouphub_creation
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Helper File Module (khoros.utils.tests.test_helper_file)
-------------------------------------------------------------
This module is used by pytest to verify that the helper configuration files work properly.

.. automodule:: khoros.utils.tests.test_helper_file
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test HTTP Headers Module (khoros.utils.tests.test_http_headers)
---------------------------------------------------------------
This module is used by pytest to verify that HTTP headers are formatted appropriately.

.. automodule:: khoros.utils.tests.test_http_headers
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Library Import Module (khoros.utils.tests.test_library_import)
-------------------------------------------------------------------
This module tests importing each of the primary modules in the library.

.. automodule:: khoros.utils.tests.test_library_import
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test LiQL WHERE Parsing Module (khoros.utils.tests.test_liql_where_parsing)
---------------------------------------------------------------------------
This module tests parsing the WHERE clause of a LiQL query.

.. automodule:: khoros.utils.tests.test_liql_where_parsing
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Mentions Module (khoros.utils.tests.test_mentions)
-------------------------------------------------------
This module is used by pytest to verify that user and content mentions work properly.

.. automodule:: khoros.utils.tests.test_mentions
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Node ID Extract Module (khoros.utils.tests.test_node_id_extract)
---------------------------------------------------------------------
This module is used by pytest to verify that Node IDs can be extracted successfully from URLs.

.. automodule:: khoros.utils.tests.test_node_id_extract
   :members:

:doc:`Return to Top <supporting-modules>`

|

Test Tags Module (khoros.utils.tests.test_tags)
-----------------------------------------------
This module is used by pytest to verify that tags function properly.

.. automodule:: khoros.utils.tests.test_tags
   :members:

:doc:`Return to Top <supporting-modules>`

|

The previous page addresses the :doc:`primary-modules` within the *khoros* package.
