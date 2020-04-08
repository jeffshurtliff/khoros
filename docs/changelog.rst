##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v2.0.0
******
**Release Date: TBD**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.api.query_successful` function.
* Added the :py:func:`khoros.api.get_results_count` function.
* Added the :py:func:`khoros.api.delete` function.
* Added the new :py:mod:`khoros.objects` module to contain sub-modules for the various API objects.
* Added the :py:mod:`khoros.objects.base` module with the following functions and classes:
    * :py:func:`khoros.objects.base.get_node_id`
    * :py:func:`khoros.objects.base.get_node_type_from_url`
    * :py:func:`khoros.objects.base.__get_node_type_identifier`
    * :py:class:`khoros.objects.base.Mapping`
* Added the :py:mod:`khoros.objects.users` module with the following functions:
    * :py:func:`khoros.objects.users.create`
    * :py:func:`khoros.objects.users.process_user_settings`
    * :py:func:`khoros.objects.users.structure_payload`
    * :py:func:`khoros.objects.users.delete`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the following exception classes:
    * :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    * :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    * :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`
    * :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    * :py:exc:`khoros.errors.exceptions.TooManyResultsError`
    * :py:exc:`khoros.errors.exceptions.UserCreationError`
* Added the :py:mod:`khoros.utils.tests.test_node_id_extract` module with the following functions:
    * :py:func:`khoros.utils.tests.test_node_id_extract.set_package_path`
    * :py:func:`khoros.utils.tests.test_node_id_extract.get_test_data`
    * :py:func:`khoros.utils.tests.test_node_id_extract.test_with_valid_node_types`
    * :py:func:`khoros.utils.tests.test_node_id_extract.test_with_invalid_node_types`
    * :py:func:`khoros.utils.tests.test_node_id_extract.test_with_only_url`
    * :py:func:`khoros.utils.tests.test_node_id_extract.test_url_without_node`

Documentation
-------------
Additions to the documentation.

* Added the :py:mod:`khoros.objects` module and the :py:mod:`khoros.objects.base` and :py:mod:`khoros.objects.users`
  sub-modules to the :doc:`Primary Modules <primary-modules>` page.
* Added the :py:mod:`khoros.utils.tests.test_node_id_extract` module to the
  :doc:`Supporting Modules <supporting-modules>` page.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Removed the unnecessary ``import requests`` line in the :py:mod:`khoros.liql` module.
* Renamed the :py:meth:`khoros.core.Khoros.__connect_with_session_key` method to be
  :py:meth:`khoros.core.Khoros._connect_with_session_key` (single underscore prefix) instead.
* Renamed the :py:meth:`khoros.core.Khoros.__define_url_settings` method to be
  :py:meth:`khoros.core.Khoros._define_url_settings` (single underscore prefix) instead.
* Renamed the :py:meth:`khoros.core.Khoros.__parse_helper_settings` method to be
  :py:meth:`khoros.core.Khoros._parse_helper_settings` (single underscore prefix) instead.
* Renamed the :py:meth:`khoros.core.Khoros.__populate_auth_settings` method to be
  :py:meth:`khoros.core.Khoros._populate_auth_settings` (single underscore prefix) instead.
* Renamed the :py:meth:`khoros.core.Khoros.__populate_construct_settings` method to be
  :py:meth:`khoros.core.Khoros._populate_construct_settings` (single underscore prefix) instead.
* Renamed the :py:meth:`khoros.core.Khoros.__populate_core_settings` method to be
  :py:meth:`khoros.core.Khoros._populate_core_settings` (single underscore prefix) instead.
* Renamed the :py:meth:`khoros.core.Khoros.__validate_base_url` method to be
  :py:meth:`khoros.core.Khoros._validate_base_url` (single underscore prefix) instead.


Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError` exception class to allow the respective
  feature to be passed as a string argument for it to be explicitly referenced in the exception message.

Documentation
-------------
Changes to the documentation.

* Updated the docstring in :py:func:`khoros.api.query_successful` indicating the API response should be in JSON format.

Fixed
=====

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.liql.format_query` function to properly encode the double-quote (``"``) character.


Documentation
-------------
Fixes in the documentation.

* Fixed two bad hyperlinks in the `README.md <https://github.com/jeffshurtliff/khoros/blob/master/README.md>`_ file.
* Fixed the docstrings in the :py:exc:`khoros.errors.exceptions.InvalidOperatorError` exception class to be accurate.
* Fixed the docstrings in the :py:exc:`khoros.errors.exceptions.OperatorMismatchError` exception class to be accurate.

|

******
v1.2.0
******
**Release Date: 2020-03-22**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:meth:`khoros.core.Khoros.signout` method.
* Added the :py:func:`khoros.auth.get_oauth_authorization_url` function.
* Added the :py:func:`khoros.auth.get_oauth_callback_url_from_user` function.
* Added the :py:func:`khoros.auth.invalidate_session` function.
* Added the :py:mod:`khoros.api` module with the following functions:
    * :py:func:`khoros.api.define_headers`
    * :py:func:`khoros.api.get_request_with_retries`
    * :py:func:`khoros.api.post_request_with_retries`
    * :py:func:`khoros.api.put_request_with_retries`
    * :py:func:`khoros.api.__api_request_with_payload`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.core_utils.get_random_string` function.
* Added the :py:func:`khoros.utils.core_utils.__structure_query_string` function.
* Added the following exception classes:
    * :py:exc:`khoros.errors.exceptions.APIConnectionError`
    * :py:exc:`khoros.errors.exceptions.GETRequestError`
    * :py:exc:`khoros.errors.exceptions.InvalidCallbackURLError`
    * :py:exc:`khoros.errors.exceptions.InvalidEndpointError`
    * :py:exc:`khoros.errors.exceptions.InvalidLookupTypeError`
    * :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`
    * :py:exc:`khoros.errors.exceptions.LookupMismatchError`
    * :py:exc:`khoros.errors.exceptions.NotFoundResponseError`
    * :py:exc:`khoros.errors.exceptions.POSTRequestError`
    * :py:exc:`khoros.errors.exceptions.PUTRequestError`

Documentation
-------------
Additions to the documentation.

* Added the :py:mod:`khoros.api` module to the :doc:`Primary Modules <primary-modules>` page.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the core :py:class:`khoros.core.Khoros` class to include the ``active`` Boolean flag in ``self.auth``.
* Updated the :py:func:`khoros.liql.perform_query` function to utilize the
  :py:func:`khoros.api.get_request_with_retries` function.
* Made minor docstring adjustments to the :py:func:`khoros.liql.perform_query` function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added the ``no_encode`` argument and associated functionality to the
  :py:func:`khoros.utils.core_utils.encode_query_string` function.

|

******
v1.1.0
******
**Release Date: 2020-03-17**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.utils.version.warn_when_not_latest` function call to the main :py:mod:`khoros` module.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.version.get_latest_stable` function.
* Added the :py:func:`khoros.utils.version.latest_version` function.
* Added the :py:func:`khoros.utils.version.warn_when_not_latest` function.

Documentation
-------------
Additions to the documentation.

* Added the **Changelog** and **Usage** sections to the
  `README.md <https://github.com/jeffshurtliff/khoros/blob/master/README.md>`_ file.
* Created the :doc:`Change Log <changelog>` page and populated it with the `v1.1.0`_ changes.
* Created the :doc:`Primary Modules <primary-modules>` and :doc:`Supporting Modules <supporting-modules>` pages.
