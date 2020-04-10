##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v2.0.0
******
**Release Date: 2020-04-10**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:meth:`khoros.core.Khoros.perform_v1_search` method.
* Added the :py:meth:`khoros.core.Khoros._import_node_class` and :py:meth:`khoros.core.Khoros._import_user_class`
  methods within the core :py:class:`khoros.Khoros` object class.
* Added the :py:class:`khoros.core.Khoros.Node` inner class within the core :py:class:`khoros.Khoros` object class.
* Added the static methods below within the core :py:class:`khoros.core.Khoros` object class:
    * :py:meth:`khoros.core.Khoros.Node.get_node_id`
    * :py:meth:`khoros.core.Khoros.Node.get_node_type_from_url`
* Added the :py:class:`khoros.core.Khoros.User` inner class within the core :py:class:`khoros.Khoros` object class.
* Added the methods below within the core :py:class:`khoros.core.Khoros` object class:
    * :py:meth:`khoros.core.Khoros.User.create`
    * :py:meth:`khoros.core.Khoros.User.delete`
    * :py:meth:`khoros.core.Khoros.User.get_user_id`
    * :py:meth:`khoros.core.Khoros.User.get_username`
    * :py:meth:`khoros.core.Khoros.User.get_login`
    * :py:meth:`khoros.core.Khoros.User.get_email`
    * :py:meth:`khoros.core.Khoros.User.query_users_table_by_id`
    * :py:meth:`khoros.core.Khoros.User.get_user_data`
    * :py:meth:`khoros.core.Khoros.User.get_album_count`
    * :py:meth:`khoros.core.Khoros.User.get_followers_count`
    * :py:meth:`khoros.core.Khoros.User.get_following_count`
    * :py:meth:`khoros.core.Khoros.User.get_images_count`
    * :py:meth:`khoros.core.Khoros.User.get_public_images_count`
    * :py:meth:`khoros.core.Khoros.User.get_messages_count`
    * :py:meth:`khoros.core.Khoros.User.get_roles_count`
    * :py:meth:`khoros.core.Khoros.User.get_solutions_authored_count`
    * :py:meth:`khoros.core.Khoros.User.get_topics_count`
    * :py:meth:`khoros.core.Khoros.User.get_replies_count`
    * :py:meth:`khoros.core.Khoros.User.get_videos_count`
    * :py:meth:`khoros.core.Khoros.User.get_kudos_given_count`
    * :py:meth:`khoros.core.Khoros.User.get_kudos_received_count`
    * :py:meth:`khoros.core.Khoros.User.get_online_user_count`
    * :py:meth:`khoros.core.Khoros.User.get_registration_data`
    * :py:meth:`khoros.core.Khoros.User.get_registration_timestamp`
    * :py:meth:`khoros.core.Khoros.User.get_registration_status`
    * :py:meth:`khoros.core.Khoros.User.get_last_visit_timestamp`
* Added the :py:func:`khoros.api.query_successful` function.
* Added the :py:func:`khoros.api.get_results_count` function.
* Added the :py:func:`khoros.api.get_items_list` function.
* Added the :py:func:`khoros.api.perform_v1_search` function.
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
    * :py:func:`khoros.objects.users.get_user_id`
    * :py:func:`khoros.objects.users.get_username`
    * :py:func:`khoros.objects.users.get_login`
    * :py:func:`khoros.objects.users.get_email`
    * :py:func:`khoros.objects.users.get_user_data_with_v1`
    * :py:func:`khoros.objects.users._get_where_clause_for_user_id`
    * :py:func:`khoros.objects.users._get_where_clause_for_username`
    * :py:func:`khoros.objects.users._get_where_clause_for_email`
    * :py:func:`khoros.objects.users._get_user_identifier`
    * :py:func:`khoros.objects.users.query_users_table_by_id`
    * :py:func:`khoros.objects.users._get_count`
    * :py:func:`khoros.objects.users._get_sum_weight`
    * :py:func:`khoros.objects.users.get_user_data`
    * :py:func:`khoros.objects.users.get_album_count`
    * :py:func:`khoros.objects.users.get_followers_count`
    * :py:func:`khoros.objects.users.get_following_count`
    * :py:func:`khoros.objects.users.get_images_count`
    * :py:func:`khoros.objects.users.get_public_images_count`
    * :py:func:`khoros.objects.users.get_messages_count`
    * :py:func:`khoros.objects.users.get_replies_count`
    * :py:func:`khoros.objects.users.get_roles_count`
    * :py:func:`khoros.objects.users.get_solutions_authored_count`
    * :py:func:`khoros.objects.users.get_topics_count`
    * :py:func:`khoros.objects.users.get_videos_count`
    * :py:func:`khoros.objects.users.get_kudos_given_count`
    * :py:func:`khoros.objects.users.get_kudos_received_count`
    * :py:func:`khoros.objects.users.get_online_user_count`
    * :py:func:`khoros.objects.users.get_registration_data`
    * :py:func:`khoros.objects.users.get_registration_timestamp`
    * :py:func:`khoros.objects.users.get_registration_status`
    * :py:func:`khoros.objects.users.get_last_visit_timestamp`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.core_utils.decode_html_entities` function.
* Added the following exception classes:
    * :py:exc:`khoros.errors.exceptions.APIRequestError`
    * :py:exc:`khoros.errors.exceptions.DELETERequestError`
    * :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    * :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    * :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`
    * :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    * :py:exc:`khoros.errors.exceptions.TooManyResultsError`
    * :py:exc:`khoros.errors.exceptions.UserCreationError`
* Added the following functions to the :py:mod:`khoros.errors.handlers` module.
    * :py:func:`khoros.errors.handlers.get_error_from_xml`
    * :py:func:`khoros.errors.handlers.get_error_from_json`
    * :py:func:`khoros.errors.handlers._get_v1_error_from_json`
    * :py:func:`khoros.errors.handlers._get_v2_error_from_json`
    * :py:func:`khoros.errors.handlers.verify_v1_response`
    * :py:func:`khoros.errors.handlers._import_exception_classes`
    * :py:func:`khoros.errors.handlers._exceptions_module_imported`
    * :py:func:`khoros.errors.handlers._import_exceptions_module`
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

* Added the :doc:`Core Object Subclasses <primary-modules>` to the :doc:`Primary Modules <primary-modules>` page.
* Added the :py:mod:`khoros.objects` module and the :py:mod:`khoros.objects.base` and :py:mod:`khoros.objects.users`
  sub-modules to the :doc:`Primary Modules <primary-modules>` page.
* Added the :py:mod:`khoros.utils.tests.test_node_id_extract` module to the
  :doc:`Supporting Modules <supporting-modules>` page.

General
-------
* Added *PyCharm Python Security Scanner* to the
  `pythonpackage.yml <https://github.com/jeffshurtliff/khorosjx/blob/master/.github/workflows/pythonpackage.yml>`_ file.


Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.liql.perform_query` function to allow a raw LiQL query to be passed rather than only
  pre-formatted query URLs.
* Updated the :py:func:`khoros.liql.perform_query` function to include an optional ``verify_success`` argument which
  verifies that the API query was successful and raises the :py:exc:`khoros.errors.exceptions.GETRequestError`
  exception if not.
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
* Updated the :py:func:`khoros.errors.handlers.get_error_from_html` function to have a second ``v1`` argument, which
  is ``False`` by default.

Documentation
-------------
Changes to the documentation.

* Updated the docstring in :py:func:`khoros.api.query_successful` indicating the API response should be in JSON format.

General
-------
* Changed the **Development Status** in ``setup.py`` to be **3 - Alpha**.

Fixed
=====

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.liql.format_query` function to properly encode the double-quote (``"``) character and
  several other special characters.


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

* Added the :py:func:`khoros.core.Khoros.signout` method.
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
