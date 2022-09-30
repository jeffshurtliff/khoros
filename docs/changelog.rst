##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v5.1.2
******
**Release Date: TBD**

Added
=====

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:class:`khoros.utils.tests.resources.MockResponse` class.
* Added the :py:func:`khoros.utils.tests.resources.mock_success_post` and
  :py:func:`khoros.utils.tests.resources.mock_error_post` functions.
* Added the :py:func:`khoros.utils.tests.test_categories.test_create_category` function.

Changed
=======

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the following functions to leverage monkeypatching:
    * :py:func:`khoros.utils.tests.test_messages.test_kudo_message`
    * :py:func:`khoros.utils.tests.test_messages.test_flagging_message`
    * :py:func:`khoros.utils.tests.test_messages.test_label_message`
    * :py:func:`khoros.utils.tests.test_messages.test_tag_message`

|

-----

******
v5.1.1
******
**Release Date: 2022-09-29**

Added
=====

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the following functions to the :py:mod:`khoros.utils.tests.resources` module:
    * :py:func:`khoros.utils.tests.resources.get_core_object`
    * :py:func:`khoros.utils.tests.resources.get_control_data`
    * :py:func:`khoros.utils.tests.resources.secrets_helper_exists`
    * :py:func:`khoros.utils.tests.resources.instantiate_with_secrets_helper`

Changed
=======

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the :py:func:`khoros.utils.tests.resources.instantiate_with_local_helper` function
  to raise a :py:exc:`FileNotFoundError` exception if the helper file cannot be found.
* Updated the :py:func:`khoros.utils.tests.resources.control_data_exists` and
  :py:func:`khoros.utils.tests.resources.import_control_data` functions to support the
  GitHub Workflows control data.
* Updated the :py:func:`khoros.utils.tests.test_categories` functions to support the GitHub
  Workflows helper file instantiation.
* Updated the :py:func:`khoros.utils.tests.test_messages` functions to support the GitHub
  Workflows helper file instantiation.
* Updated the :py:func:`khoros.utils.tests.test_liql` functions to support the GitHub
  Workflows helper file instantiation.

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Fixed the issue reported in Issue `#59 <https://github.com/jeffshurtliff/khoros/issues/59>`_
  where the :py:func:`khoros.structures.base.get_structure_field` function was failing with
  a :py:exc:`KeyError` exception.

Removed
=======

Supporting Modules
------------------
Removals in the :doc:`supporting modules <supporting-modules>`.

* Removed the :py:func:`khoros.utils.tests.test_categores.get_control_data` and
  :py:func:`khoros.utils.tests.test_categories.get_core_object` functions that became obsolete.

|

-----

******
v5.1.0
******
**Release Date: 2022-09-28**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the following methods:
    * :py:meth:`khoros.core.Khoros.Message.kudo`
    * :py:meth:`khoros.core.Khoros.Message.flag`
    * :py:meth:`khoros.core.Khoros.Message.unflag`
    * :py:meth:`khoros.core.Khoros.Message.label`
    * :py:meth:`khoros.core.Khoros.Message.tag`

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the following functions to the :py:mod:`khoros.objects.messages` module:
    * :py:func:`khoros.objects.messages.kudo`
    * :py:func:`khoros.objects.messages.flag`
    * :py:func:`khoros.objects.messages.unflag`
    * :py:func:`khoros.objects.messages._set_spam`
    * :py:func:`khoros.objects.messages.label`
    * :py:func:`khoros.objects.messages.tag`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the following functions to the :py:mod:`khoros.utils.tests.resources` module:
    * :py:func:`khoros.utils.tests.resources.import_control_data`
    * :py:func:`khoros.utils.tests.resources.control_data_exists`
    * :py:func:`khoros.utils.tests.resources._get_control_dataset_file`
* Added the following functions to the :py:mod:`khoros.utils.tests.test_messages` module:
    * :py:func:`khoros.utils.tests.test_messages.set_package_path`
    * :py:func:`khoros.utils.tests.test_messages.test_kudo_message`
    * :py:func:`khoros.utils.tests.test_messages.test_flagging_message`
    * :py:func:`khoros.utils.tests.test_messages.test_label_message`
    * :py:func:`khoros.utils.tests.test_messages.test_tag_message`
* Added the following functions to the :py:mod:`khoros.utils.tests.test_version` module:
    * :py:func:`khoros.utils.tests.test_version.test_full_version`
    * :py:func:`khoros.utils.tests.test_version.test_major_minor_version`
    * :py:func:`khoros.utils.tests.test_version.test_latest_stable`
    * :py:func:`khoros.utils.tests.test_version.test_latest_version`
* Added the following functions to the :py:mod:`khoros.utils.tests.test_communities` module:
    * :py:func:`khoros.utils.tests.test_communities.set_package_path`
    * :py:func:`khoros.utils.tests.test_communities.test_community_details`
* Added the following functions to the :py:mod:`khoros.utils.tests.test_categories` module:
    * :py:func:`khoros.utils.tests.test_communities.set_package_path`
    * :py:func:`khoros.utils.tests.test_communities.get_core_object`
    * :py:func:`khoros.utils.tests.test_communities.get_control_data`
    * :py:func:`khoros.utils.tests.test_communities.test_get_category_id`
    * :py:func:`khoros.utils.tests.test_communities.test_total_count`
    * :py:func:`khoros.utils.tests.test_communities.test_if_category_exists`
    * :py:func:`khoros.utils.tests.test_communities.test_category_details`

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Fixed the issue reported in Issue `#58 <https://github.com/jeffshurtliff/khoros/issues/58>`_
  where the :py:func:`khoros.structures.categories.get_creation_date` function was failing with
  an exception.

|

-----

******
v5.0.0
******
**Release Date: 2022-09-20**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added and configured the ``self.bulk_data_settings`` dictionary in the core object.
* Added the :py:class:`khoros.core.Khoros.BulkData` inner class with the following methods:
    * :py:meth:`khoros.core.Khoros.BulkData.query`
    * :py:meth:`khoros.core.Khoros.BulkData.get_base_url`
* Added the following methods to the :py:class:`khoros.core.Khoros.Message` inner class:
    * Added the :py:meth:`khoros.core.Khoros.Message.get_context_id` method.
    * Added the :py:meth:`khoros.core.Khoros.Message.get_context_url` method.
    * Added the :py:meth:`khoros.core.Khoros.Message.define_context_id` method.
    * Added the :py:meth:`khoros.core.Khoros.Message.define_context_url` method.
* Added the :py:meth:`khoros.core.Khoros.User.get_registered_users_count` method.
* Added the :py:meth:`khoros.core.Khoros.User.get_online_users_count` method.
* Added the :py:meth:`khoros.core.Khoros.Community.sso_enabled` method.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the new :py:mod:`khoros.bulk_data` module with the following functions:
    * :py:func:`khoros.bulk_data.get_base_url`
    * :py:func:`khoros.bulk_data.query`
    * :py:func:`khoros.bulk_data._construct_headers`
    * :py:func:`khoros.bulk_data._get_export_header`
    * :py:func:`khoros.bulk_data._construct_parameters`
    * :py:func:`khoros.bulk_data._validate_date_field`
* Added the following functions to the :py:mod:`khoros.objects.messages` module:
    * Added the :py:func:`khoros.objects.messages.get_context_id` function.
    * Added the :py:func:`khoros.objects.messages.get_context_url` function.
    * Added the :py:func:`khoros.objects.messages.define_context_id` function.
    * Added the :py:func:`khoros.objects.messages.define_context_url` function.
* Added the :py:func:`khoros.objects.users.get_registered_users_count` function.
* Added the :py:func:`khoros.objects.users.get_online_users_count` function.
* Added the :py:func:`khoros.structures.communities.sso_enabled` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.helper._get_bulk_data_info` function.
* Added the :py:func:`khoros.utils.tests.resources.instantiate_with_placeholder` function.
* Added the :py:mod:`khoros.utils.tests.test_bulk_data` module with the following test functions:
    * :py:func:`khoros.utils.tests.test_bulk_data.test_base_url_without_helper`
    * :py:func:`khoros.utils.tests.test_bulk_data.test_core_object_settings`
    * :py:func:`khoros.utils.tests.test_bulk_data.test_export_type_header`
    * :py:func:`khoros.utils.tests.test_bulk_data.test_valid_header_construction`
    * :py:func:`khoros.utils.tests.test_bulk_data.test_valid_parameter_construction`
* Added the :py:func:`khoros.utils.tests.test_settings.test_sso_status_retrieval` test function.
* Added the :py:func:`khoros.utils.tests.test_roles` module with the following functions:
    * :py:func:`khoros.utils.tests.test_roles.set_package_path`
    * :py:func:`khoros.utils.tests.test_roles.test_get_role_id`
    * :py:func:`khoros.utils.tests.test_roles.test_invalid_role_type`
    * :py:func:`khoros.utils.tests.test_roles.test_total_role_type_counts`
    * :py:func:`khoros.utils.tests.test_roles.test_get_roles_for_user`
    * :py:func:`khoros.utils.tests.test_roles.test_get_users_with_role`

General
-------
* Added the ``bulk_data`` section to the ``examples/helper.yml`` file.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Merged two ``if`` statements in the :py:meth:`khoros.core.Khoros._populate_auth_settings` method.
* Added a reference to the `Khoros Developer Documentation <https://bit.ly/3LQLyW5>`_ in the
  :py:meth:`khoros.core.Khoros.Role.get_users_with_role` method.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Improved the error handling in the :py:func:`khoros.auth.get_session_key` function.
* Merged two ``if`` statements in the following functions:
    * :py:func:`khoros.auth.get_sso_key`
    * :py:func:`khoros.liql.perform_query`
* Added a reference to the `Khoros Developer Documentation <https://bit.ly/3LQLyW5>`_ in the
  :py:func:`khoros.objects.roles.get_users_with_role` function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added a function call in :py:func:`khoros.utils.helper._get_connection_info` to parse the
  Bulk Data API connection information when applicable.
* Merged two ``if`` statements in the :py:func:`khoros.utils.version.warn_when_not_latest` function.
* Made a minor change to the docstring for :py:func:`khoros.errors.handlers._exceptions_module_imported`.

General
-------
* Updated the `Security Policy <https://github.com/jeffshurtliff/khoros/blob/master/SECURITY.md>`_ to
  add support for version 5.0.x and to remove support for version 3.x.x.

Fixed
=====

Core Object
-----------
Fixes to the :doc:`core-object-methods`.

* Removed the redundant ``return`` statement from the
  :py:meth:`khoros.core.Khoros.Tag.add_tags_to_message` method.

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.structures.grouphubs._create_group_hub_with_avatar` to pass a defined
  content-type value which was previously stored in an unused variable.
* Removed redundant ``return`` statements from the following functions in the :py:mod:`khoros.api` module:
    * :py:func:`khoros.api._confirm_field_supplied`
    * :py:func:`khoros.api._display_ssl_verify_warning`
    * :py:func:`khoros.api._report_failed_attempt`
* Removed redundant ``return`` statements from the following functions in the
  :py:mod:`khoros.objects.tags` module:
    * :py:func:`khoros.objects.tags.add_tags_to_message`
    * :py:func:`khoros.objects.tags.add_single_tag_to_message`
* Removed the redundant ``return`` statement from the
  :py:func:`khoros.structures.boards._warn_about_ignored_settings` function.
* Removed the redundant ``return`` statement from the
  :py:func:`khoros.structures.communities._check_for_multiple_tenants` function.
* Removed the redundant ``return`` statement from the
  :py:func:`khoros.structures.grouphubs.refresh_enabled_discussion_styles` function.
* Removed the :py:exc:`DeprecationWarning` from the
  :py:class:`khoros.structures.base.Mapping` class to address Issue
  `#57 <https://github.com/jeffshurtliff/khoros/issues/57>`_.

Supporting Modules
------------------
Fixes to the :doc:`supporting modules <supporting-modules>`.

* Removed redundant ``return`` statements from the following functions in the
  :py:mod:`khoros.utils.version` module:
    * :py:func:`khoros.utils.version.log_current_version`
    * :py:func:`khoros.utils.version.warn_when_not_latest`
* Removed redundant ``return`` statements from the following functions in the
  :py:mod:`khoros.utils.environment` module:
    * :py:func:`khoros.utils.environment.update_env_variable_names`
    * :py:func:`khoros.utils.environment._update_env_list`
    * :py:func:`khoros.utils.environment._update_env_mapping`
* Removed redundant ``return`` statements from the following functions in the
  :py:mod:`khoros.errors.handlers` module:
    * :py:func:`khoros.errors.handlers.eprint`
    * :py:func:`khoros.errors.handlers.verify_v1_response`
    * :py:func:`khoros.errors.handlers.verify_core_object_present`
    * :py:func:`khoros.errors.handlers._import_exceptions_module`
    * :py:func:`khoros.errors.handlers._import_exception_classes`
* Removed the redundant ``return`` statement from the
  :py:func:`khoros.utils.core_utils.display_warning` function.
* Removed the redundant ``return`` statement from the
  :py:func:`khoros.utils.tests.resources.set_package_path` and
  :py:func:`khoros.utils.tests.resources.parse_testing_config_file` functions.
* Removed the redundant ``return`` statement from all or most functions in the
  following modules:
    * :py:func:`khoros.utils.tests.test_board_creation`
    * :py:func:`khoros.utils.tests.test_core_utils`
    * :py:func:`khoros.utils.tests.test_grouphub_creation`
    * :py:func:`khoros.utils.tests.test_helper_file`
    * :py:func:`khoros.utils.tests.test_http_headers`
    * :py:func:`khoros.utils.tests.test_library_import`
    * :py:func:`khoros.utils.tests.test_liql`
    * :py:func:`khoros.utils.tests.test_mentions`
    * :py:func:`khoros.utils.tests.test_messages`
    * :py:func:`khoros.utils.tests.test_node_id_extract`
    * :py:func:`khoros.utils.tests.test_settings`
    * :py:func:`khoros.utils.tests.test_ssl_verify`
    * :py:func:`khoros.utils.tests.test_tags`

|

-----

******
v4.5.0
******
**Release Date: 2022-01-16**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.core.Khoros.Message.get_metadata` method.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.objects.messages.get_metadata` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:exc:`khoros.errors.exceptions.InvalidMetadataError` exception class.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Replaced the phrase *"This function"* with *"This method"* in all of the core method docstrings.

|

-----

******
v4.4.0
******
**Release Date: 2021-10-12**

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Introduced the ``proxy_user_object`` parameter to the :py:meth:`khoros.core.Khoros.Message.create`
  method to allow messages to be created on behalf of other users.
* Introduced the ``proxy_user_object`` parameter to the :py:meth:`khoros.core.Khoros.Message.update`
  method to allow messages to be updated on behalf of other users.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Introduced the ``proxy_user_object`` parameter to the :py:func:`khoros.objects.messages.create`
  function to allow messages to be created on behalf of other users.
* Introduced the ``proxy_user_object`` parameter to the :py:func:`khoros.objects.messages.update`
  function to allow messages to be updated on behalf of other users.

|

-----

************
v4.3.0.post1
************
**Release Date: 2021-10-10**

Changed
=======

General
-------
* Added Python version 3.10 to ``setup.py``.

|

-----

******
v4.3.0
******
**Release Date: 2021-10-10**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.core.Khoros.Message.validate_message_payload` static method.
* Added the :py:class:`khoros.core.Khoros.SAML` inner class with the following methods:
    * :py:meth:`khoros.core.Khoros.SAML.import_assertion`
    * :py:meth:`khoros.core.Khoros.SAML.send_assertion`
* Added the :py:meth:`khoros.core.Khoros._import_saml_class` method.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:mod:`khoros.saml` module with the following functions:
    * :py:func:`khoros.saml.import_assertion`
    * :py:func:`khoros.saml.send_assertion`
    * :py:func:`khoros.saml._is_decoded`
    * :py:func:`khoros.saml._get_api_uri`
* Added the :py:func:`khoros.objects.messages.validate_message_payload` function.
* Added the :py:mod:`khoros.objects.labels` module to begin addressing the enhancement
  request `#48 <https://github.com/jeffshurtliff/khoros/issues/48>`_.
* Added the global variable ``ssl_verify_disabled`` to the :py:mod:`khoros.api` module
  to allow the verification to be performed even in functions that do not leverage the
  instantiated core object.
* Added the :py:func:`khoros.api._display_ssl_verify_warning` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:exc:`khoros.errors.exceptions.InvalidMessagePayloadError` exception class.
* Added the :py:func:`khoros.utils.tests.test_messages.test_payload_validation` test function.

Documentation
-------------
* Added the :py:mod:`khoros.saml` and :py:mod:`khoros.objects.labels` modules to the
  :doc:`Primary Modules <primary-modules>` page.
* Added a ``TODO`` section in the docstring for the
  :py:func:`khoros.objects.messages.construct_payload` function to indicate the missing
  functionality that still remains to be added.
* Added the new :doc:`manage-settings` page to the documentation.

General
-------
* Created the GitHub issue template ``.github/ISSUE_TEMPLATE/documentation_request.md``.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Added support for the ``full_payload`` parameter in the :py:meth:`khoros.core.Khoros.Message.create`
  method to implement the enhancement request `#46 <https://github.com/jeffshurtliff/khoros/issues/46>`_.
* Added support for the ``wrap_json`` parameter in the :py:func:`khoros.core.Khoros.Tag.structure_tags_for_message`
  function to implement the enhancement request `#47 <https://github.com/jeffshurtliff/khoros/issues/47>`_.
* Updated the ``__init__`` module for the core object class to define the ``ssl_verify_disabled`` global
  variable in the :py:mod:`khoros.api` module as ``True`` when the ``ssl_verify`` flag in the core settings are
  explicitly set to ``False``.  (See line 186)

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added support for the ``full_payload`` parameter in the :py:func:`khoros.objects.messages.create`
  function to implement the enhancement request `#46 <https://github.com/jeffshurtliff/khoros/issues/46>`_.
* Added support for the ``wrap_json`` parameter in the :py:func:`khoros.objects.tags.structure_tags_for_message`
  function to implement the enhancement request `#47 <https://github.com/jeffshurtliff/khoros/issues/47>`_.
* Updated the ``__all__`` variable in the :py:mod:`khoros.objects` init module (``__init__py.``) and
  added import statements for the :py:mod:`khoros.objects.attachments`, :py:mod:`khoros.objects.base` and
  :py:mod:`khoros.objects.labels` modules.
* Updated the :py:func:`khoros.api.should_verify_tls` function to introduce the ``ssl_verify_disabled`` global
  variable, which allows the check to be performed even when the core object is not passed to the function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added support for utilizing the ``defined_settings`` parameter in the
  :py:func:`khoros.utils.tests.resources.initialize_khoros_object` function.


General
-------
* Updated the GitHub issue template ``.github/ISSUE_TEMPLATE/bug_report.md`` to be more intuitive.
* Added quotes in ``pythonpackage.yml`` to avoid issue referenced in
  `actions/setup-python#160 <https://github.com/actions/setup-python/issues/160>`_.
* Added `Python v3.10 <https://docs.python.org/3/whatsnew/3.10.html>`_ to ``pythonpackage.yml``.
* Refactored ``pythonpackage.yml`` to perform macOS builds in order to ensure support for Python
  v3.10 per request `#50 <https://github.com/jeffshurtliff/khoros/issues/50>`_.

Fixed
=====

Core Object
-----------
Fixes in the :doc:`core-object-methods`.

* Fixed some incorrect information in the docstring for :py:meth:`khoros.core.Khoros.User.get_username`.
* Fixed an issue in the ``__init__`` method of the core object where the ``ssl_verify`` parameter
  was being mostly disregarded.
* Fixed an issue in the ``__init__`` method of the core object where the ``auto_connect`` parameter
  defined via the ``defined_settings`` parameter was being disregarded.

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Fixed an issue in the following functions that prevented the SSL verification from being disabled
  when configured to do so in the helper settings.
    * :py:func:`khoros.api._api_request_with_payload`
    * :py:func:`khoros.api._api_request_without_payload`
    * :py:func:`khoros.api.delete`
    * :py:func:`khoros.api.perform_v1_search`
    * :py:func:`khoros.api.make_v1_request`
    * :py:func:`khoros.api.get_platform_version`
* Refactored the :py:func:`khoros.liql.parse_where_clause` function to be more efficient and Pythonic,
  and added missing parenthesis on the exception classes. Docstring syntax errors were also fixed.

Supporting Modules
------------------
Fixes in the :doc:`supporting modules <supporting-modules>`.

* Fixed an issue in the :py:func:`khoros.utils.helper.get_helper_settings` function where the
  ``ssl_verify`` field was being overridden even if defined elsewhere.

|

-----

******
v4.2.1
******
**Release Date: 2021-09-24**

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.api.put_request_with_retries` function call within the
  :py:func:`khoros.roles._assign_role_with_v2` function to explicitly define the content-type
  as ``application/json`` in order to resolve `Issue #45 <https://github.com/jeffshurtliff/khoros/issues/45>`_.

|

-----

******
v4.2.0
******
**Release Date: 2021-09-13**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.core.Khoros._connect_with_lithium_token` method to connect using
  `LithiumSSO Token authentication <https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token>`_.

  .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #42 <https://github.com/jeffshurtliff/khoros/pull/42>`_.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.auth.get_sso_key` function.
* Added the :py:func:`khoros.auth._get_khoros_login_url` private function.

  .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #42 <https://github.com/jeffshurtliff/khoros/pull/42>`_.
            However, the use of the :py:mod:`xml.etree.ElementTree` module was replaced
            with the :py:mod:`defusedxml.ElementTree` module to proactively mitigate a
            `known XML attack vulnerability
            <https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b313-b320-xml>`_
            in the former module.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:exc:`khoros.errors.exceptions.SsoAuthenticationError` exception for use with
  `LithiumSSO Token authentication <https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token>`_.
* Added the :py:mod:`khoros.utils.tests.test_ssl_verify` module with the following test functions:
    * :py:func:`khoros.utils.tests.test_ssl_verify.test_default_core_object_setting`
    * :py:func:`khoros.utils.tests.test_ssl_verify.test_core_object_with_param_setting`
    * :py:func:`khoros.utils.tests.test_ssl_verify.test_api_global_variable_assignment`
    * :py:func:`khoros.utils.tests.test_ssl_verify.test_api_should_verify_function`

Documentation
-------------
* Added example syntax for authenticating using a
  `LithiumSSO token <https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token>`_
  in the ``README.md`` file.

  .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #42 <https://github.com/jeffshurtliff/khoros/pull/42>`_.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Support was introduced in the :py:class:`khoros.core.Khoros` core object class to support
  `LithiumSSO Token authentication <https://developer.khoros.com/khoroscommunitydevdocs/docs/lithiumsso-token>`_.

  .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #42 <https://github.com/jeffshurtliff/khoros/pull/42>`_.

* Support was introduced in the :py:class:`khoros.core.Khoros` core object class to support
  user impersonation with LithiumSSO token authentication.

  .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #44 <https://github.com/jeffshurtliff/khoros/pull/44>`_.

* The following methods within the :py:class:`khoros.core.Khoros` core object class
  were improved to avoid unnecessary :py:exc:`KeyError` exceptions:
    * :py:meth:`khoros.core.Khoros._populate_core_settings`
    * :py:meth:`khoros.core.Khoros._populate_auth_settings`
    * :py:meth:`khoros.core.Khoros._populate_construct_settings`
    * :py:meth:`khoros.core.Khoros._parse_helper_settings`
    * :py:meth:`khoros.core.Khoros._validate_base_url`
    * :py:meth:`khoros.core.Khoros._define_url_settings`
    * :py:meth:`khoros.core.Khoros._session_auth_credentials_defined`
    * :py:meth:`khoros.core.Khoros._connect_with_session_key`
    * :py:meth:`khoros.core.Khoros.connect`
    * :py:meth:`khoros.core.Khoros.get`
* General code improvements were made throughout the ``__init__`` method for the
  :py:class:`khoros.core.Khoros` core object class.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* The URI in the :py:func:`khoros.auth.get_session_key` function is now generated utilizing the
  :py:func:`khoros.auth._get_khoros_login_url` function.

  .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #42 <https://github.com/jeffshurtliff/khoros/pull/42>`_.

* Support was introduced in the :py:class:`khoros.objects.users.ImpersonatedUser` object class
  to support user impersonation with LithiumSSO token authentication.

  .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #44 <https://github.com/jeffshurtliff/khoros/pull/44>`_.

General
-------
* Added the :py:mod:`defusedxml` package to ``requirements.txt`` and as a required install package
  in ``setup.py``.

Fixed
=====

Core Object
-----------
Fixes to the :doc:`core-object-methods`.

* Resolved `Issue #41 <https://github.com/jeffshurtliff/khoros/issues/41>`_ which involved the
  :py:exc:`requests.exceptions.InvalidSchema` exception being raised when using absolute URLs
  with the :py:meth:`khoros.core.Khoros.get`, :py:meth:`khoros.core.Khoros.post` and
  :py:meth:`khoros.core.Khoros.put` core methods.
* Corrected how the exception error message is defined in the :py:meth:`khoros.core.Khoros.connect`
  method.

|

-----

******
v4.1.1
******
**Release Date: 2021-08-05**

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.objects.archives.aggregate_results_data` function to properly
  handle the ``ARCHIVED`` status when it is returned.

|

-----

******
v4.1.0
******
**Release Date: 2021-06-29**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:class:`khoros.core.Khoros.Archives` inner class within the
  core :py:class:`khoros.Khoros` object with the following methods:
    * :py:meth:`khoros.core.Khoros.Archives.archive`
    * :py:meth:`khoros.core.Khoros.Archives.unarchive`
    * :py:meth:`khoros.core.Khoros.Archives.aggregate_results`
* Added the :py:meth:`khoros.core.Khoros._import_archives_class` method.
* Added the :py:class:`khoros.core.Khoros.Tag` inner class within the core
  :py:class:`khoros.Khoros` object with the following methods:
    * :py:meth:`khoros.core.Khoros.Tag.get_tags_for_message`
    * :py:meth:`khoros.core.Khoros.Tag.add_single_tag_to_message`
    * :py:meth:`khoros.core.Khoros.Tag.add_tags_to_message`
    * :py:meth:`khoros.core.Khoros.Tag.structure_single_tag_payload`
    * :py:meth:`khoros.core.Khoros.Tag.structure_tags_for_message`
* Added the :py:meth:`khoros.core.Khoros._import_tag_class` method.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.objects.archives.aggregate_results_data` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the following functions to utilize with the :py:mod:`pytest` package
  for unit testing:
    * :py:func:`khoros.utils.tests.resources.local_helper_exists`
    * :py:func:`khoros.utils.tests.resources.instantiate_with_local_helper`
    * :py:func:`khoros.utils.tests.resources._get_local_helper_file_name`
    * :py:func:`khoros.utils.tests.resources.local_test_config_exists`
    * :py:func:`khoros.utils.tests.resources.parse_testing_config_file`
    * :py:func:`khoros.utils.tests.resources.get_testing_config`
    * :py:func:`khoros.utils.tests.resources.get_structure_collection`
* Added the following functions to the :py:mod:`khoros.utils.tests.test_liql` module:
    * :py:func:`khoros.utils.tests.test_liql.perform_test_query`
    * :py:func:`khoros.utils.tests.test_liql.test_liql_query`
    * :py:func:`khoros.utils.tests.test_liql.test_return_items_option`
* Added the :py:mod:`khoros.utils.tests.test_settings` module with the following functions:
    * :py:func:`khoros.utils.tests.test_settings.set_package_path`
    * :py:func:`khoros.utils.tests.test_settings.test_node_setting_retrieval`
    * :py:func:`khoros.utils.tests.test_settings.test_invalid_node_type_exception`

Documentation
-------------

* Added sections for the :py:class:`khoros.core.Khoros.Archives` and
  :py:class:`khoros.core.Khoros.Archives` inner classes on the
  :doc:`core-object-methods` page.
* Added a section for the :py:mod:`khoros.utils.tests.test_settings`
  module on the :doc:`supporting-modules` page.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Removed the following parameters from the :py:meth:`khoros.core.Khoros.Archives.archive`
  and :py:meth:`khoros.core.Khoros.Archives.unarchive` methods: ``full_response``,
  ``return_id``, ``return_url``, ``return_api_url``, ``return_http_code``, ``return_status``,
  ``return_error_messages`` and ``split_errors``
* Introduced the ``return_items`` parameter in the :py:meth:`khoros.core.Khoros.query`
  function to automatically reduce the JSON response to only the returned items when
  desired. (``False`` by default)

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Some minor docstring adjustments were made in the `khoros.objects.archives.archive`
  and `khoros.objects.archives.unarchive` functions.
* Explicitly set the ``full_response`` flag in the :py:func:`khoros.objects.archives.archive`
  and :py:func:`khoros.objects.archives.unarchive` functions because of unique response format
  and subsequently removed the following parameters: ``full_response``, ``return_id``,
  ``return_url``, ``return_api_url``, ``return_http_code``, ``return_status``,
  ``return_error_messages`` and ``split_errors``
* Introduced the optional ``aggregate_results`` parameter in the `khoros.objects.archives.archive`
  and `khoros.objects.archives.unarchive` functions.
* Introduced the ``return_items`` parameter in the :py:func:`khoros.liql.perform_query`
  function to automatically reduce the JSON response to only the returned items when
  desired. (``False`` by default)
* Imported the :py:mod:`khoros.objects.tags` module within the ``__init__`` file for the
  :py:mod:`khoros.objects` module and added ``tags`` to the ``__all__`` special variable.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Renamed the :py:mod:`khoros.utils.tests.test_liql_where_parsing` module to be
  :py:mod:`khoros.utils.tests.test_liql` to allow other LiQL tests to be performed
  within the same module.
* Updated the :py:func:`khoros.utils.tests.test_liql.set_package_path` function to
  leverage a global variable to ensure the operation is only performed once.

Documentation
-------------
* Updated the :doc:`supporting modules <supporting-modules>` to account for the
  renamed :py:mod:`khoros.utils.tests.test_liql` module.

General
-------
* Adjusted the Sphinx-related package versions in ``requirements.txt``.

Fixed
=====

Core Object
-----------
Fixes to the :doc:`core-object-methods`.

* Corrected an issue in the :py:meth:`khoros.core.Khoros.Role.get_roles_for_user` docstring
  where the wrong raised exception was referenced.

    .. note:: This change was introduced by
            `stevenspasbo <https://github.com/stevenspasbo>`_ via
            `Pull Request #33 <https://github.com/jeffshurtliff/khoros/pull/33>`_.

* Added some missing exception references in the :py:meth:`khoros.core.Khoros.query` docstring.

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Fixed an issue with the :py:func:`khoros.objects.archives.structure_archive_payload`
  function call in the :py:func:`khoros.objects.archives.archive` function.
* Renamed the incorrect JSON field ``messageID`` to be ``messageId`` instead in the
  :py:func:`khoros.objects.archives._format_single_archive_entry` function to prevent the
  following error from getting returned:

  .. code-block:: json

     {
       'status': 'error',
       'message': 'A possible invalid request has been made.
                   Make sure you are following the API spec and have used the correct URL,
                   are included all required parameters and if a request payload is required
                   you have included one.',
       'data': {
         'type': 'error_data',
         'code': 309,
         'developer_message': '',
         'more_info': ''
       },
       'metadata': {}
     }

* Added a missing section of the docstring for the
  :py:func:`khoros.objects.tags.structure_tags_for_message` function.

|

-----

******
v4.0.0
******
**Release Date: 2021-05-20**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.core.Khoros.User.impersonate_user` method.
* Added the :py:meth:`khoros.core.Khoros.Role.get_role_id` method.
* Added the :py:class:`khoros.core.Khoros.V2` class with the following methods:
    * :py:meth:`khoros.core.Khoros.V2.get`
    * :py:meth:`khoros.core.Khoros.V2.post`
    * :py:meth:`khoros.core.Khoros.V2.put`
* Added and called the :py:meth:`khoros.core.Khoros._import_v2_class` protected class.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:class:`khoros.objects.users.ImpersonatedUser` object class for performing API calls
  as other users.
* Added the :py:func:`khoros.objects.users.impersonate_user` function to assist in instantiating
  the :py:class:`khoros.objects.users.ImpersonatedUser` object.
* Added the following functions to the :py:func:`khoros.objects.roles` module:
    * :py:func:`khoros.objects.roles.get_role_id`
    * :py:func:`khoros.objects.roles.assign_roles_to_user`
    * :py:func:`khoros.objects.roles._assign_role_with_v1`
    * :py:func:`khoros.objects.roles._assign_role_with_v2`
    * :py:func:`khoros.objects.roles._validate_node_type`
    * :py:func:`khoros.objects.roles._query_for_users`
* Added the :py:func:`khoros.api._add_json_query_to_uri` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:exc:`khoros.errors.exceptions.FeatureNotConfiguredError` exception.

General
-------
* Added the :py:func:`read` and :py:func:`get_version` functions to ``setup.py``
  to address `Issue #28 <https://github.com/jeffshurtliff/khoros/issues/28>`_.

  .. note:: This change was introduced by
            `truthbyron <https://github.com/truthbyron>`_ via
            `Pull Request #31 <https://github.com/jeffshurtliff/khoros/pull/31>`_.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Updated the methods below to introduce the ``proxy_user_object`` parameter to allow API requests
  to be performed on behalf of other users.
    * :py:meth:`khoros.core.Khoros.get`
    * :py:meth:`khoros.core.Khoros.post`
    * :py:meth:`khoros.core.Khoros.put`
    * :py:meth:`khoros.core.Khoros.Subscription.add_subscription`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_board`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_category`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_label`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_message`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_product`
    * :py:meth:`khoros.core.Khoros.V1.get`
    * :py:meth:`khoros.core.Khoros.V1.post`
    * :py:meth:`khoros.core.Khoros.V1.put`
    * :py:meth:`khoros.core.Khoros.V1.search`
* Changed the default value of the ``return_json`` parameter to ``True`` in the
  :py:meth:`khoros.core.Khoros.Settings.define_node_setting` function.
* Updated the :py:meth:`khoros.core.Khoros.User.create` method to return the API
  response and introduced the ``ignore_exceptions`` parameter.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the functions below to introduce the ``proxy_user_object`` parameter to allow API requests
  to be performed on behalf of other users.
    * :py:func:`khoros.api.define_headers`
    * :py:func:`khoros.api.get_request_with_retries`
    * :py:func:`khoros.api.payload_request_with_retries`
    * :py:func:`khoros.api.post_request_with_retries`
    * :py:func:`khoros.api.put_request_with_retries`
    * :py:func:`khoros.api.delete`
    * :py:func:`khoros.api.perform_v1_search`
    * :py:func:`khoros.api.make_v1_request`
    * :py:func:`khoros.objects.subscriptions.add_subscription`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_board`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_category`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_label`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_message`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_product`
* Introduced the ``user_and_type`` parameter in the :py:func:`khoros.api.get_v1_user_path` function
  that can be passed instead of a parameter for a specific type.
* Changed the default value of the ``return_json`` parameter to ``True`` in the
  :py:func:`khoros.objects.settings.define_node_setting` function.
* Added proper support for group hubs in the
  :py:func:`khoros.objects.settings.define_node_setting` and
  :py:func:`khoros.objects.settings._get_v1_node_setting` functions.
* Removed node type validation from the :py:func:`khoros.objects.settings.define_node_setting` function.
* Added node type validation in the :py:func:`khoros.objects.settings._get_v2_node_setting` function.
* Updated the :py:func:`khoros.objects.users.create` function to return the API response and
  introduced the ``ignore_exceptions`` parameter.
* Updated the :py:func:`khoros.objects.users.delete` function to raise the new
  :py:exc:`khoros.errors.exceptions.FeatureNotConfiguredError` exception when appropriate.
* Added group hub support in the :py:func:`khoros.api.get_v1_node_collection` function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

 * Introduced the ability for the :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
   exception to accept the ``param`` keyword argument and display a more specific message.
 * Updated the :py:mod:`khoros.utils.environment` module to no longer import the ``PyYAML``
   package directly and instead to leverage the :py:mod:`importlib` module in the
   :py:func:`khoros.utils.environment._import_custom_names_file` function as necessary.

Documentation
-------------
Changes to the documentation.

* Added missing information to the docstring for the following methods and functions:
    * :py:meth:`khoros.core.Khoros.connect`
    * :py:meth:`khoros.core.Khoros.get_session_key`
    * :py:meth:`khoros.core.Khoros.put`
    * :py:func:`khoros.api._confirm_field_supplied`
* Updated the example in the header block for the :py:mod:`khoros.objects.users` module.
* Updated the header block in the ``setup.py`` script to have more information.

General
-------
* Moved the ``PyYAML``, ``urllib3``, ``requests`` and ``setuptools`` packages from the
  ``requirements.txt`` file to the ``setup.py`` file within the ``install_requires`` list
  to address `Issue #28 <https://github.com/jeffshurtliff/khoros/issues/28>`_.

  .. note:: This change was introduced by
            `truthbyron <https://github.com/truthbyron>`_ via
            `Pull Request #31 <https://github.com/jeffshurtliff/khoros/pull/31>`_.

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Fixed issues with the primary functions in the :py:mod:`khoros.api` module that was resulting
  in raised exceptions if JSON responses were requested in v1 API calls without explicitly
  including the ``restapi.response_format=json`` query string.
* Fixed issues in the :py:func:`khoros.objects.users.structure_payload` and
  :py:func:`khoros.objects.users.process_user_settings` functions that were resulting
  in a :py:exc:`KeyError` exception potentially getting raised.
* Added the missing ``type`` key to the payload dictionary in the
  :py:func:`khoros.objects.users.structure_payload` function that was preventing users from
  getting created successfully.
* Fixed an issue in the :py:func:`khoros.objects.subscriptions._construct_category_payload`
  where the payload was getting double-wrapped with the ``data`` dictionary key.
* Refactored the :py:func:`khoros.objects.roles.get_users_with_role` function to leverage a
  ``while`` loop instead of recursion in order to avoid raising a :py:exc:`RecursionError`
  exception with larger queries.
* Wrapped the cursor string in the :py:func:`khoros.liql.structure_cursor_clause` function
  in single quotes to fix an ``Invalid query syntax`` error that was raising the
  :py:exc:`khoros.errors.exceptions.LiQLParseError` exception.

|

-----

******
v3.5.0
******
**Release Date: 2021-03-26**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.core.Khoros.get_session_key` method.
* Added the :py:meth:`khoros.core.Khoros.Role.get_users_with_role` method.
* Added the :py:class:`khoros.core.Khoros.Subscription` inner class with the following methods:
    * :py:meth:`khoros.core.Khoros.Subscription.add_subscription`
    * :py:meth:`khoros.core.Khoros.Subscription.get_subscription_uri`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_board`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_category`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_label`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_message`
    * :py:meth:`khoros.core.Khoros.Subscription.subscribe_to_product`
* Added the :py:meth:`khoros.core.Khoros._import_subscription_class` method and leveraged it to
  allow subscription-related methods to be called with the ``khoros.subscriptions`` namespace.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.api.get_v1_user_path` and :py:func:`khoros.api.get_v1_node_collection`
  functions to facilitate crafting API v1 endpoint URIs.
* Added the new :py:mod:`khoros.objects.subscriptions` module with the following functions:
    * :py:func:`khoros.objects.subscriptions.add_subscription`
    * :py:func:`khoros.objects.subscriptions.get_subscription_uri`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_board`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_category`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_label`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_message`
    * :py:func:`khoros.objects.subscriptions.subscribe_to_product`
    * :py:func:`khoros.objects.subscriptions._construct_category_payload`
    * :py:func:`khoros.objects.subscriptions._construct_target_subscription`
* Updated the ``__init__.py`` file for the :py:mod:`khoros.objects` module to import the new
  :py:mod:`khoros.objects.subscriptions` module and add it to the ``__all__`` variable.
* Added the :py:func:`khoros.auth._get_session_key_payload` function.
* Added the :py:func:`khoros.auth._get_session_key_header` function.
* Added the following functions to the :py:mod:`khoros.objects.roles` module.
    * :py:func:`khoros.objects.roles.get_users_with_role`
* Added the :py:func:`khoros.errors.exceptions.structure_cursor_clause` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.core_utils.convert_dict_list_to_simple_list` function.
* Added the :py:func:`khoros.utils.core_utils.is_iterable` function.

Documentation
-------------
Additions to the documentation.

* Added a badge for the latest beta / release candidate (RC) release on the
  `README <https://github.com/jeffshurtliff/khoros/blob/master/README.md>`_ page.
* Added badges for the security audits (bandit and PyCharm Python Security Scanner) to the
  `README <https://github.com/jeffshurtliff/khoros/blob/master/README.md>`_ page.
* Added a badge for the CodeFactor Grade on the
  `README <https://github.com/jeffshurtliff/khoros/blob/master/README.md>`_ page.

General
-------
* Added the ``.github/workflows/bandit.yml`` GitHub Action workflow configuration file
  to leverage the
  `Python security check using Bandit <https://github.com/marketplace/actions/python-security-check-using-bandit>`_
  action to perform security audits with each push event.
* Added badges in the `README <https://github.com/jeffshurtliff/khoros/blob/master/README.md>`_ page.
* Added comments in multiple scripts within the library to address how the bandit GitHub Action
  will identify users.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Updated the :py:meth:`khoros.core.Khoros.Role.get_roles_for_user` method to allow SELECT fields
  to be explicitly defined.
* Removed the unnecessary ``pass`` statement in the :py:meth:`khoros.core.Khoros.close` method.
* Removed the unnecessary ``return`` statements in the :py:meth:`khoros.core.Khoros.signout` and
  :py:meth:`khoros.core.Khoros.User.create` methods.
* Replaced ``type()`` with ``isinstance()`` when performing typechecks throughout the
  :py:mod:`khoros.core` module.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* The :py:func:`khoros.auth.get_session_key` function has been updated to allow a secondary user to be
  authenticated by passing either a username and password or by passing only a username when calling the
  function as a previously authenticated user with Administrator privileges.
* Added the ``community``, ``grouphub`` and ``global`` keys to the ``ROLE_TYPES`` dictionary constant in
  the :py:mod:`khoros.objects.roles` module.
* Updated the :py:func:`khoros.objects.roles.get_roles_for_user` function to allow SELECT fields to be
  explicitly defined.
* Renamed the :py:func:`khoros.liql._parse_select_fields` function to be
  :py:func:`khoros.liql.parse_select_fields` instead. (i.e. private to public function)
* Refactored the :py:func:`khoros.liql.parse_select_fields` function to leverage the :py:func:`isinstance`
  built-in function.
* Removed the mandatory dependency on the ``requests_toolbelt`` package by leveraging the :py:mod:`importlib`
  package to attempt to import it locally as needed within the :py:func:`khoros.api.encode_multipart_data` function.
* Removed an unnecessary ``else`` statement in the :py:func:`khoros.api.define_headers` function after the
  :py:exc:`khoros.errors.exceptions.MissingAuthDataError` exception is raised.
* Replaced ``type()`` with ``isinstance()`` when performing the typecheck in the
  :py:func:`khoros.api.perform_v1_search` function.
* Removed the unnecessary ``pass`` statement in the following functions:
    * :py:func:`khoros.api._api_request_with_payload`
    * :py:func:`khoros.api._api_request_without_payload`

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.log_utils.initialize_logging` function call to initialize logging within
  the :py:mod:`khoros.utils.core_utils` module.
* Changed the default value for the ``shell`` parameter to be ``False`` in the
  :py:func:`khoros.utils.core_utils.run_cmd` function to improve overall
  `security <https://bandit.readthedocs.io/en/latest/plugins/b602_subprocess_popen_with_shell_equals_true.html>`_
  of the library.
* Added the optional ``delimiter`` parameter to the :py:func:`khoros.utils.core_utils.convert_string_to_tuple`
  function and added functionality to convert delimited strings.

General
-------
* Removed the stale branch ``3.0.0`` from the ``.github/workflows/codeql-analysis.yml`` file.
* Removed ``requests_toolbelt`` from ``requirements.txt``.

Fixed
=====

Core Object
-----------
Fixes to the :doc:`core-object-methods`.

* Updated the :py:meth:`khoros.core.Khoros.post` function so that the ``query_url``
  no longer gets prefixed with a slash (``/``) if the ``relative_url`` parameter is
  set to ``False``.


Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Fixed an issue with the :py:func:`khoros.api.payload_request_with_retries` function
  where non-payload API calls (including those with query parameters defined in the URI)
  were incorrectly raising a :py:exc:`khoros.errors.exceptions.PayloadMismatchError` exception.

|

-----

******
v3.4.0
******
**Release Date: 2021-03-06**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.core.Khoros.get_platform_version` method.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.api.should_verify_tls` function to determine if SSL/TLS certificates should
  be verified when making REST API calls.
* Added a warning to the :py:func:`khoros.api.should_verify_tls` to inform of the suppressed warnings.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Updated the ``__init__`` method for the :py:class:`khoros.core.Khoros` object class to include the ``ssl_verify``
  parameter and to establish a key-value pair for it in the ``core_settings`` dictionary.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Removed an unnecessary ``pass`` statement from the :py:func:`khoros.api.get_request_with_retries` function
  and initially defined the ``response`` variable with a ``NoneType`` value to prevent a linting error from
  being reported.
* Introduced support for the ``ssl_verify`` core setting in the :py:class:`khoros.core.Khoros` object within
  the following functions:
    * :py:func:`khoros.api._api_request_with_payload`
    * :py:func:`khoros.api._api_request_without_payload`
    * :py:func:`khoros.api.delete`
    * :py:func:`khoros.api.get_platform_version`
    * :py:func:`khoros.api.get_request_with_retries`
    * :py:func:`khoros.api.payload_request_with_retries`
    * :py:func:`khoros.api.perform_v1_search`
    * :py:func:`khoros.api.post_request_with_retries`
    * :py:func:`khoros.api.put_request_with_retries`
    * :py:func:`khoros.auth.get_session_key`
    * :py:func:`khoros.liql.perform_query`
* Renamed the function :py:func:`khoros.liql.__parse_select_fields` to be :py:func:`khoros.liql.__parse_select_fields`.
* Renamed the function :py:func:`khoros.liql.__wrap_string_vales` to be :py:func:`khoros.liql._wrap_string_values`.
* Renamed the function :py:func:`khoros.liql.__convert_where_dicts_to_lists` to be
  :py:func:`khoros.liql._convert_where_dicts_to_lists`.
* Renamed the function :py:func:`khoros.liql.__parse_where_clause` to be :py:func:`khoros.liql.parse_where_clause`
  and converted it from a private to a public function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Added support for the ``ssl_verify`` field in the :py:mod:`khoros.utils.helper` module.
* Refactored the :py:func:`khoros.utils.version.get_latest_stable` function to leverage the
  Python `standard library <https://docs.python.org/3/library/urllib.request.html#module-urllib.request>`_
  instead of the `requests <https://requests.readthedocs.io/>`_ library which helps address
  issue `#28 <https://github.com/jeffshurtliff/khoros/issues/28>`_.

|

-----

******
v3.3.3
******
**Release Date: 2021-01-25**

Fixed
=====

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Added error handling in the :py:func:`khoros.objects.settings._get_v2_node_setting` function to prevent
  an :py:exc:`AttributeError` exception from being raised.

|

-----

******
v3.3.2
******
**Release Date: 2021-01-08**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the optional ``skip_env_variables`` argument  to the ``__init__`` method of the
  :py:class:`khoros.core.Khoros` class to explicitly ignore valid environment variables
  when instantiating the core object.
* Added the optional ``empty`` argument to the ``__init__`` method of the
  :py:class:`khoros.core.Khoros` class to instantiate an empty core object with default values.
* Added the method :py:meth:`khoros.core.Khoros._populate_empty_object` to populates necessary
  fields to allow an empty object to be instantiated successfully.
* Logging (via the :py:mod:`khoros.utils.log_utils` module) was introduced in methods throughout
  the :py:mod:`khoros.core` module.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Introduced the ``return_json`` parameter in the :py:meth:`khoros.core.Khoros.Settings.define_node_setting`
  method and the :py:func:`khoros.objects.settings.define_node_setting` function to optionally return the
  Community API response in JSON format. (This option prevents the
  :py:exc:`khoros.errors.exceptions.POSTRequestError` exception from being raised after an unsuccessful API call.)
* Introduced the ``convert_json`` parameter in the :py:meth:`khoros.core.Khoros.Settings.get_node_setting` method
  and the :py:func:`khoros.objects.settings.get_node_setting` function to optionally convert JSON strings into
  Python dictionaries.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Introduced the ``return_json`` parameter in the :py:func:`khoros.objects.settings.define_node_setting` to
  optionally return the Community API response in JSON format. (This option prevents the
  :py:exc:`khoros.errors.exceptions.POSTRequestError` exception from being raised after an unsuccessful API call.)

Documentation
-------------
Changes to the documentation.

* Merged the release notes for version ``3.3.0.post0`` into those for the subsequent
  stable version ``3.3.1``.
* Added an example function call in the header block of the :py:mod:`khoros.utils.log_utils` module.
* Made further improvements to the documentation styling in the ``custom.css`` file.

Fixed
=====

Core Object
-----------
Fixes in the :doc:`core-object-methods`.

* Updated the ``__init__`` method for the :py:class:`khoros.core.Khoros` class to only skip method arguments
  when they explicitly have a ``None`` value and are not just implicitly ``False``.

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* The error handling has been improved in the :py:func:`khoros.liql.get_returned_items` function to avoid
  :py:exc:`IndexError` exceptions from being raised when no items were found in the LiQL response.

|

-----

******
v3.3.1
******
**Release Date: 2021-01-06**

Added
=====

Documentation
-------------
Additions to the documentation.

* Added the
  :ref:`Settings Subclass (khoros.core.Khoros.Settings) <core-object-methods:Settings Subclass (khoros.core.Khoros.Settings)>`
  section to the :doc:`Khoros Core Object <core-object-methods>` page.
* Added the
  :ref:`Settings Module (khoros.objects.settings) <primary-modules:Settings Module (khoros.objects.settings)>`
  section to the :doc:`Primary Modules <primary-modules>` page.
* Updated the CSS styling in ``custom.css`` to improve readability of methods and functions.

Changed
=======

Documentation
-------------
Changes to the documentation.

* Alphabetized the sections on the :doc:`Khoros Core Object <core-object-methods>` page.
* Removed the introductory sentence for each of the modules on the :doc:`Primary Modules <primary-modules>` page
  as they had become redundant with the same information already present in the docstrings.
* Moved the
  :ref:`Studio Subclass (khoros.core.Khoros.Studio) <core-object-methods:Studio Subclass (khoros.core.Khoros.Studio)>`
  section out of the
  :ref:`Core Object Subclasses (khoros.core.Khoros) <core-object-methods:Core Object Subclasses (khoros.core.Khoros)>`
  section and into its own, similar to where it is located on the :doc:`Primary Modules <primary-modules>` page.

Fixed
=====

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Fixed an issue with the :py:func:`khoros.api.make_v1_request` function call within
  the :py:func:`khoros.objects.settings._get_v2_node_setting` that was resulting in
  :py:exc:`IndexError` exceptions.
* Fixed an issue in :py:func:`khoros.objects.settings._get_v2_node_setting` resulting in
  an :py:exc:`IndexError` exception if the setting field is not found, and made changes
  to return a ``None`` value in that situation.

Documentation
-------------
Fixes in the documentation.

* A minor fix was made to the docstring in the :py:func:`khoros.objects.settings.define_node_setting` function
  to correct a Sphinx parsing issue. The function itself was not changed.

|

-----

******
v3.3.0
******
**Release Date: 2020-12-26**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Defined the ``version`` variable within the :py:class:`khoros.core.Khoros` core object to make it
  easy to determine the current version of the package after having instantiated said object.

Changed
=======

General
-------
* Added ``Khoros`` to the ``__all__`` dictionary in the primary ``__init__.py`` file.

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Renamed the ``_settings`` dictionary (private) to be ``core_settings`` (public) in the core object
  to avoid warning messages being displayed in PyCharm and other IDEs as reported in Issue
  `#26 <https://github.com/jeffshurtliff/khoros/issues/26>`_.
* Renamed the ``settings`` argument in the ``__init__`` method for the :py:class:`khoros.core.Khoros`
  object to be ``defined_settings`` to avoid conflicting with the :py:meth:`khoros.core.Khoros.Settings`
  method.
* Made some minor PEP8 compliance-related adjustments in the :py:mod:`khoros.core` module.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the functions below to change ``_settings`` to ``core_settings``.
    * :py:func:`khoros.auth.get_session_key`
    * :py:func:`khoros.auth.invalidate_session`
    * :py:func:`khoros.auth.get_oauth_authorization_url`
    * :py:func:`khoros.objects.users.create`
    * :py:func:`khoros.objects.users.delete`
    * :py:func:`khoros.structures.grouphubs.refresh_enabled_discussion_styles`

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the :py:func:`khoros.errors.translations.translation_enabled` function to change ``_settings``
  to ``core_settings``.

:doc:`Return to Top <changelog>`

|

-----

******
v3.2.0
******
**Release Date: 2020-12-23**

Added
=====

General
-------
* Created the ``dev-requirements.txt`` to indicate which packages may be required for contributors,
  whereas the ``requirements.txt`` file now only contains the absolute necessities to use the package.

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:class:`khoros.core.Khoros.Settings` class with the following methods:
    * :py:meth:`khoros.core.Khoros.Settings.get_node_setting`
    * :py:meth:`khoros.core.Khoros.Settings.define_node_setting`
* Added the :py:meth:`khoros.core.Khoros._import_settings_class` method.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the new :py:mod:`khoros.objects.settings` module with the following functions:
    * :py:func:`khoros.objects.settings.get_node_setting`
    * :py:func:`khoros.objects.settings._get_v1_node_setting`
    * :py:func:`khoros.objects.settings._get_v2_node_setting`
    * :py:func:`khoros.objects.settings._validate_node_type`
* Added the :py:mod:`khoros.objects.settings` module to the ``__init__.py`` file for the
  :py:mod:`khoros.objects` module.
* Added the new :py:func:`khoros.liql.get_returned_items` function.
* Added the new :py:func:`khoros.api.encode_payload_values` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the following new exception classes:
    * :py:exc:`khoros.errors.exceptions.UnsupportedNodeTypeError`
    * :py:exc:`khoros.errors.exceptions.LiQLParseError`
    * :py:exc:`khoros.errors.exceptions.PayloadMismatchError`

Changed
=======

General
-------

* Updated ``setup.py`` to enable support for Python v3.8.x and v3.9.x now that compatibility testing
  has been performed and no issues have been identified.
* Updated the *Development Status* classifier in ``setup.py`` to be ``5 - Production/Stable``.
* Added some additional *Topic* classifiers in ``setup.py``.
* Significantly cleaned up the ``requirements.txt`` file to only include the absolute necessities.
* Updated ``requirements.txt`` to replace ``==`` with ``>=`` to be less strict on dependency versions
  as long as they meet a minimum version requirement.
* Made a minor adjustment to the ``README.md`` file relating to documentation.
* Updated the ``docs/conf.py`` file to require Sphinx version 3.4.0.
* Re-added the Sphinx-related dependencies to ``requirements.txt`` to allow ReadTheDocs builds
  to be successful.

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Updated the methods below to support API v1 calls using payloads:
    * :py:meth:`khoros.core.Khoros.V1.post`
    * :py:meth:`khoros.core.Khoros.V1.put`

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the functions below to support API v1 calls using JSON payloads:
    * :py:func:`khoros.api.make_v1_request`
    * :py:func:`khoros.api.encode_v1_query_string`
* Added support for URL-encoded string payloads in the following functions:
    * :py:func:`khoros.api.payload_request_with_retries`
    * :py:func:`khoros.api.post_request_with_retries`
    * :py:func:`khoros.api.put_request_with_retries`

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Moved the exceptions within the **Base Object Exceptions** section of :py:mod:`khoros.errors.exceptions`
  into a new section entitled **Node Exceptions**.
* Updated the following exceptions to optionally accept ``status_code`` and ``message`` as arguments:
    * :py:exc:`khoros.errors.exceptions.GETRequestError`
    * :py:exc:`khoros.errors.exceptions.POSTRequestError`
    * :py:exc:`khoros.errors.exceptions.PUTRequestError`
* Updated the :py:exc:`khoros.errors.exceptions.SessionAuthenticationError` exception to optionally accept
  ``message`` as an argument.
* Updated the :py:func:`khoros.utils.core_utils.encode_query_string` function to support
  API v1 calls using JSON payloads.
* Updated the function :py:func:`khoros.utils.core_utils.convert_single_value_to_tuple` to be
  more PEP8 compliant.

Fixed
=====

Core Object
-----------
Fixes in the :doc:`core-object-methods`.

* Fixed an argument mismatch issue in the :py:meth:`khoros.core.Khoros.parse_v2_response` and
  :py:meth:`khoros.core.Khoros.Message.parse_v2_response` (deprecated) methods.
* Updated the methods below to pass the query parameters in the message body to avoid exceeding
  the URI limit and receiving responses with ``413`` or ``414`` status codes.

    * :py:meth:`khoros.core.Khoros.V1.post`
    * :py:meth:`khoros.core.Khoros.V1.put`

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Added a missing docstring for the :py:func:`khoros.api.payload_request_with_retries` function.
* Updated the function :py:func:`khoros.api.make_v1_request` to pass the query parameters in the message
  body to avoid exceeding the URI limit and receiving responses with ``413`` or ``414`` status codes.
* Fixed an issue where v1 GET requests were not appending the ``restapi.response_format=json`` query
  string when a JSON response has been requested.

Supporting Modules
------------------
Fixes in the :doc:`supporting modules <supporting-modules>`.

* Updated the default message in the :py:exc:`khoros.errors.exceptions.TooManyResultsError` exception to be
  appropriate as it was inadvertently using the same message leveraged in the
  :py:exc:`khoros.errors.exceptions.OperatorMismatchError` exception.

:doc:`Return to Top <changelog>`

|

-----

******
v3.1.1
******
**Release Date: 2020-11-02**

Fixed
=====

Core Object
-----------
Fixes to the :doc:`core-object-methods`.

* Fixed issues in the following methods to address the bug `#20 <https://github.com/jeffshurtliff/khoros/issues/20>`_:
    * :py:meth:`khoros.core.Khoros.post`
    * :py:meth:`khoros.core.Khoros.put`

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Fixed issues in the function :py:func:`khoros.api.post_request_with_retries` to address the bug
  `#20 <https://github.com/jeffshurtliff/khoros/issues/20>`_.

:doc:`Return to Top <changelog>`

|

-----

******
v3.1.0
******
**Release Date: 2020-10-28**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.get` method to perform simple GET requests that leverage the core
  object authorization headers where necessary.
* Added the :py:meth:`khoros.post` method to perform simple POST requests that leverage the core
  object authorization headers where necessary.
* Added the :py:meth:`khoros.put` method to perform simple PUT requests that leverage the core
  object authorization headers where necessary.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.api.payload_request_with_retries` function to act as a "master function" for
  :py:func:`khoros.api.post_request_with_retries` and :py:func:`khoros.api.put_request_with_retries`.
* Added the :py:func:`khoros.api._is_plaintext_payload` function.

Documentation
-------------
Additions to the documentation.

* Added missing sections to the :doc:`Core Object Methods <core-object-methods>` page.


Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added support for ``text/plain`` payloads and introduced the ``content_type`` parameter in the following functions:
    * :py:func:`khoros.api.post_request_with_retries`
    * :py:func:`khoros.api._api_request_with_payload`
* Updated the :py:func:`khoros.api.post_request_with_retries` and
  :py:func:`khoros.api.put_request_with_retries` functions to leverage the new
  :py:func:`khoros.api.payload_request_with_retries` function.

:doc:`Return to Top <changelog>`

|

-----

******
v3.0.0
******
**Release Date: 2020-10-19**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:class:`khoros.core.Khoros.V1` inner class with the following methods:
    * :py:meth:`khoros.core.Khoros.V1.get`
    * :py:meth:`khoros.core.Khoros.V1.post`
    * :py:meth:`khoros.core.Khoros.V1.put`
    * :py:meth:`khoros.core.Khoros.V1.search`
* Added the :py:meth:`khoros.core.Khoros._import_v1_class` and accompanying method call.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.api.get_platform_version`
* Added the :py:func:`khoros.api._normalize_base_url`
* Instantiated a logger in the following modules:
    * :py:mod:`khoros.api`
    * :py:mod:`khoros.auth`
    * :py:mod:`khoros.liql`
    * :py:mod:`khoros.objects.albums`
    * :py:mod:`khoros.objects.archives`
    * :py:mod:`khoros.objects.attachments`
    * :py:mod:`khoros.objects.base`
    * :py:mod:`khoros.objects.messages`
    * :py:mod:`khoros.objects.roles`
    * :py:mod:`khoros.objects.tags`
    * :py:mod:`khoros.objects.users`
    * :py:mod:`khoros.structures.base`
    * :py:mod:`khoros.structures.boards`
    * :py:mod:`khoros.structures.categories`
    * :py:mod:`khoros.structures.communities`
    * :py:mod:`khoros.structures.grouphubs`
    * :py:mod:`khoros.structures.nodes`
    * :py:mod:`khoros.studio.base`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Introduced logging within the library:
    * Added the :py:mod:`khoros.utils.log_utils` module with the following functions, classes and methods:
        * :py:func:`khoros.utils.log_utils.initialize_logging`
        * :py:class:`khoros.utils.log_utils.LessThanFilter`
        * :py:meth:`khoros.utils.log_utils.LessThanFilter.filter`
        * :py:func:`khoros.utils.log_utils._apply_defaults`
        * :py:func:`khoros.utils.log_utils._get_log_levels_from_dict`
        * :py:func:`khoros.utils.log_utils._set_logging_level`
        * :py:func:`khoros.utils.log_utils._add_handlers`
        * :py:func:`khoros.utils.log_utils._add_file_handler`
        * :py:func:`khoros.utils.log_utils._add_stream_handler`
        * :py:func:`khoros.utils.log_utils._add_split_stream_handlers`
        * :py:func:`khoros.utils.log_utils._add_syslog_handler`
    * Added a ``logging`` section to the ``examples/helper.yml`` file to indicate how logging can be configured.
* Added the :py:func:`khoros.utils.core_utils.encode_base64` function.
* Added the :py:func:`khoros.utils.version.log_current_version` function.

Documentation
-------------
* Added the :doc:`changelog-1.1.0-thru-2.5.2.rst <changelogs/changelog-1.1.0-thru-2.5.2>` file
  and embedded it into this :doc:`changelog` page to have less content per RST document.
* Added :doc:`Return to Top <changelog>` links at the bottom of each version section.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Replaced the basic :py:mod:`logging` initialization with a call to the
  :py:func:`khoros.utils.log_utils.initialize_logging` function.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.api.make_v1_request` function to make the ``query_params``
  argument optional.
* Updated the :py:func:`khoros.api.make_v1_request` function to allow full query strings to be
  passed within the ``endpoint`` argument.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* The following changes were made to the :py:mod:`khoros.utils.version` module:
    * Initialized a logger at the beginning of the module.
    * Added a debug log entry to the :py:func:`khoros.utils.versions.get_full_version` which reports
      the current version of the library.
    * Reduced the :py:func:`khoros.utils.version.latest_version` function to a single return statement.
    * Added error handling and logging in the :py:func:`khoros.utils.version.get_latest_stable` function
      to avoid an exception if PyPI cannot be queried successfully.
    * Updated the :py:func:`khoros.utils.version.warn_when_not_latest` function to use logging for the
      warning rather than the :py:mod:`warnings` module.

General
-------
* Updated the Sphinx configuration file (``conf.py``) to suppress the ``duplicate label`` warnings.
* Added version 3.0.x to the ``SECURITY.md`` file under Supported.

:doc:`Return to Top <changelog>`

Fixed
=====

General
-------
* Changed the `pyYAML <https://pypi.org/project/PyYAML/>`_ version in ``requirements.txt`` to be
  ``5.3.1`` rather than ``5.3`` in order to avoid the CI build failure in GitHub Actions.

Deprecated
==========

Core Object
-----------
Deprecations in the :doc:`core-object-methods`.

* Deprecated the :py:meth:`khoros.core.Khoros.perform_v1_search` method as it has been replaced
  by the :py:meth:`khoros.core.Khoros.V1.search` method.

:doc:`Return to Top <changelog>`

|

-----

******
v2.8.0
******
**Release Date: 2020-07-06**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`khoros.core.Khoros.Message.update` method.
* Added the ``translate_errors`` default setting to the core object.

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the following functions within the :py:mod:`khoros.objects.messages` module:
    * :py:func:`khoros.objects.messages.update`
    * :py:func:`khoros.objects.messages.is_read_only`
    * :py:func:`khoros.objects.messages.set_read_only`
    * :py:func:`khoros.objects.messages._verify_message_id`
    * :py:func:`khoros.objects.messages._add_moderation_status_to_payload`
* Added the new :py:mod:`khoros.objects.tags` module with the following functions:
    * :py:func:`khoros.objects.tags.structure_single_tag_payload`
    * :py:func:`khoros.objects.tags.add_single_tag_to_message`
    * :py:func:`khoros.objects.tags.add_tags_to_message`
    * :py:func:`khoros.objects.tags.get_tags_for_message`
    * :py:func:`khoros.objects.tags._format_tag_data`
* Added the :py:func:`khoros.objects.attachments._structure_attachments_to_add` function.
* Introduced the ability for error messages to be translated where possible to be more relevant
  within the :py:func:`khoros.api.parse_v2_response`, :py:func:`khoros.api.deliver_v2_response`
  and :py:func:`khoros.api._get_v2_return_values` functions, and added the optional
  ``khoros_object`` or ``_khoros_object`` argument to facilitate this.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.errors.handlers.verify_core_object_present` function.
* Added the :py:mod:`khoros.errors.translations` module with the following functions:
    * :py:func:`khoros.errors.translations.translate_error`
    * :py:func:`khoros.errors.translations.translation_enabled`
    * :py:func:`khoros.errors.translations.parse_message`
* Added the :py:mod:`khoros.errors.translations` module to the ``__all__`` special variable
  and imported it by default within the :py:mod:`khoros.errors` (``__init__.py``) module.
* Added the :py:mod:`khoros.utils.tests.test_tags` module with the following functions:
    * :py:func:`khoros.utils.tests.test_tags.test_single_tag_structure`
    * :py:func:`khoros.utils.tests.test_tags.get_structure_control_data`
    * :py:func:`khoros.utils.tests.test_tags.test_message_structure_one_tag`
    * :py:func:`khoros.utils.tests.test_tags.test_message_structure_two_tags`
    * :py:func:`khoros.utils.tests.test_tags.test_message_structure_one_string_tag_ignore`
    * :py:func:`khoros.utils.tests.test_tags.test_message_structure_two_string_tags_ignore`
    * :py:func:`khoros.utils.tests.test_tags.test_message_structure_str_int`
    * :py:func:`khoros.utils.tests.test_tags.test_message_structure_str_int_ignore`
* Added the :py:mod:`khoros.utils.tests.test_messages` module with the following functions:
    * :py:func:`khoros.utils.tests.test_messages.get_control_data`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_only_subject`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_node`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_node_id`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_node_url`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_body`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_one_str_tag`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_one_int_tag`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_str_iter_int_tags`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_str_iter_int_tags_ignore`
    * :py:func:`khoros.utils.tests.test_messages.test_construct_with_tag_iterables`
    * :py:func:`khoros.utils.tests.test_messages.assert_tags_present`
* Added the :py:func:`khoros.utils.core_utils.remove_tld` function.
* Added the :py:func:`khoros.utils.tests.test_core_utils.test_remove_tld` function.
* Added the :py:func:`khoros.utils.core_utils.merge_and_dedup` function.
* Added the :py:func:`khoros.utils.tests.test_core_utils.test_merge_and_dedup` function.

Documentation
-------------
Additions to the documentation.

* Added the :py:mod:`khoros.objects.tags` module  to the :doc:`primary-modules` page.
* Added the :py:mod:`khoros.errors.translations` module to the :doc:`supporting-modules` page.
* Added the :py:mod:`khoros.utils.tests.test_tags` module to the :doc:`supporting-modules` page.
* Added the :py:mod:`khoros.utils.tests.test_messages` module to the :doc:`supporting-modules` page.
* Added a reference to the ``KHOROS_TRANSLATE_ERRORS`` environment variable and added a new
  :ref:`Roadmap <introduction:Roadmap>` section to both the :doc:`introduction` page and the
  ``README.md`` file.
* Created the currently in-progress :doc:`messages` page, per Enhancement
  `#1 <https://github.com/jeffshurtliff/khoros/issues/1>`_.

General
-------
* Added the file ``v2_message_attachment_update_payload.json`` to the
  ``examples/example_output`` directory.

Changed
=======

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Introduced the ``ignore_non_string_tags``, ``return_status``, ``return_error_messages`` and
  ``split_errors`` arguments in the :py:meth:`khoros.core.Khoros.Message.create` method, and
  changed the default value of the ``full_response``, ``return_id``, ``return_url``,
  ``return_api_url`` and ``return_http_code`` arguments to ``None`` rather than ``False``.
* Added support for the ``translate_errors`` Helper setting and any other future top-level
  setting within the :py:meth:`khoros.core.Khoros._parse_helper_settings` method.

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the functions below to support the :py:func:`khoros.objects.messages.update` function.
    * :py:func:`khoros.objects.messages.structure_payload`
    * :py:func:`khoros.objects.attachments.construct_multipart_payload`
    * :py:func:`khoros.objects.attachments.format_attachment_payload`
    * :py:func:`khoros.objects.attachments.get_file_upload_info`
* Updated the if statement in :py:func:`khoros.objects.messages._verify_required_fields` to leverage
  the :py:func:`isinstance` function.
* Added the ``return_status``, ``return_error_messages`` and ``split_errors`` arguments
  to the :py:func:`khoros.objects.messages.create` function, and changed the default value
  of the ``full_response``, ``return_id``, ``return_url``, return_api_url`` and
  ``return_http_code`` arguments to ``None`` rather than ``False``.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the :py:func:`khoros.utils.helper.get_helper_settings` function to capture the
  ``translate_errors`` value when defined in the configuration file.
* Refactored the :py:func:`khoros.utils.helper._get_construct_info` function to leverage the
  :py:func:`khoros.utils.helper._collect_values` function.

Documentation
-------------
Changes to the documentation.

* Updated the **Supported Versions** chart in the
  `Security Policy <https://github.com/jeffshurtliff/khoros/security/policy>`_.
* Made a very minor formatting change on the :doc:`introduction` page.
* Added the :doc:`messages` page to the master :ref:`index:Table of Contents`.
* Added a link to the `PyPI package page <https://pypi.org/project/khoros>`_
  in the first paragraph of the :doc:`index <index>` page.
* Changed the *intersphinx inventory* URL for the built-in Python 3 modules from
  `<https://docs.python.org/>`_ to `<https://docs.python.org/3/>`_ in the
  ``docs/conf.py`` file.

General
-------
* Updated the ``examples/helper.yml`` file to include the ``translate_errors`` setting.
* Added the ``KHOROS_TRANSLATE_ERRORS`` environment variable to the
  ``examples/custom_env_variables.yml`` and ``examples/custom_env_variables.json`` files.

:doc:`Return to Top <changelog>`

|

-----

******
v2.7.6
******
**Release Date: 2020-06-25**

Added
=====

Documentation
-------------
Additions to the documentation.

* Added the `LGTM Grade <https://lgtm.com/projects/g/jeffshurtliff/khoros>`_ to the ``README.md`` file.

General
-------
* Added the two files below to the ``examples/example_output/`` directory.
    * ``v2_message_attachment_create_payload.json``
    * ``v2_message_attachment_create_success.json``

Changed
=======

Documentation
-------------
Changes to the documentation.

* Added the :doc:`core-object-methods` page amd moved the documentation for the :py:mod:`khoros` (``__init__.py``)
  module and the :py:mod:`khoros.core` module to the new page from the :doc:`primary-modules` page.
* Added the new :doc:`core-object-methods` page to the :doc:`index` page.
* Added navigational sentences at the bottom of the :doc:`primary-modules`, :doc:`supporting-modules` and
  :doc:`core-object-methods` pages.

Fixed
=====

Primary Modules
---------------
Fixes in the :doc:`primary modules <primary-modules>`.

* Fixed the "Exception objects instantiated but not raised" issue reported in GitHub.
  (`Issue #2 <https://github.com/jeffshurtliff/khoros/issues/2>`_)

:doc:`Return to Top <changelog>`

|

-----

******
v2.7.5
******
**Release Date: 2020-06-18**

Added
=====

General
-------
* Added the `v2_error_not_authorized.json` file to the `examples/example_output` directory.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added the ``default_content_type`` argument to the :py:func:`khoros.api.define_headers` function.

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:func:`khoros.api._normalize_headers` function to ensure that
  authentication/authorization tokens would not be altered.

:doc:`Return to Top <changelog>`

|

-----

******
v2.7.4
******
**Release Date: 2020-06-18**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.api._normalize_headers` function to normalize the HTTP headers.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:mod:`khoros.utils.tests.resources` module with the following functions:
    * :py:func:`khoros.utils.tests.resources.set_package_path`
    * :py:func:`khoros.utils.tests.resources.import_modules`
    * :py:func:`khoros.utils.tests.resources.initialize_khoros_object`
* Added the :py:mod:`khoros.utils.tests.test_http_headers` module for unit testing.

Documentation
-------------
Additions to the documentation.

* Added a section to the :doc:`primary-modules` page for the :py:mod:`khoros.objects.archives` module.
* Added sections to the :doc:`supporting-modules` page for the following modules:
    * :py:func:`khoros.utils.tests.resources`
    * :py:func:`khoros.utils.tests.test_board_creation`
    * :py:func:`khoros.utils.tests.test_grouphub_creation`
    * :py:func:`khoros.utils.tests.test_http_headers`

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Standardized the case-sensitivity of the HTTP headers to all be lower-case in the following functions:
    * :py:func:`khoros.api.define_headers`
    * :py:func:`khoros.api.make_v1_request`
    * :py:func:`khoros.auth.get_session_key`
    * :py:func:`khoros.objects.users.create`
* Included a function call for :py:func:`khoros.api._normalize_headers` in :py:func:`khoros.api.define_headers`.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the unit testing modules below to utilize the :py:mod:`khoros.utils.tests.resources` module:
    * :py:mod:`khoros.utils.tests.test_board_creation`
    * :py:mod:`khoros.utils.tests.test_grouphub_creation`

:doc:`Return to Top <changelog>`

|

-----

******
v2.7.3
******
**Release Date: 2020-06-17**

Added
=====

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:mod:`khoros.utils.tests.test_grouphub_creation` module for unit testing with ``pytest``.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added the ``debug_mode`` Boolean argument (``False`` by default) to the ``__init__`` method
  for the :py:class:`khoros.core.Khoros` class which populates within the ``_settings`` protected
  dictionary.

General
-------
* Added ``dist.old/`` to the ``.gitignore`` file in the root directory of the repository.

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Fixed how the payload in :py:func:`khoros.structures.grouphubs.structure_payload` is initially
  defined to avoid a :py:exc:`TypeError` exception from being raised during the
  :py:func:`khoros.structures.grouphubs._structure_simple_string_fields` function call.

:doc:`Return to Top <changelog>`

|

-----

******
v2.7.2
******
**Release Date: 2020-06-17**

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Fixed some bad logic in the :py:func:`khoros.structures.grouphubs.structure_payload` that was raising
  false positive exceptions.

Documentation
-------------
Fixes to the documentation.

* Changed the data type for ``membership_type`` from ``dict`` to ``str`` in the docstring for the
  :py:func:`khoros.structures.grouphubs.create`, :py:func:`khoros.structures.grouphubs.structure_payload`
  and :py:func:`khoros.structures.grouphubs._structure_membership_type` functions.

:doc:`Return to Top <changelog>`

|

-----

******
v2.7.1
******
**Release Date: 2020-06-17**

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Removed some print debugging found in the :py:func:`khoros.api.make_v1_request` function.
* Fixed a syntax error with raising the :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError` exception
  class within the :py:func:`khoros.api.make_v1_request` function.

General
-------
* Added several API v1 output examples in the ``examples/example_output`` directory.

:doc:`Return to Top <changelog>`

|

-----

******
v2.7.0
******
**Release Date: 2020-06-12**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the new :py:mod:`khoros.objects.archives` module with the following functions:
    * :py:func:`khoros.objects.archives.archive`
    * :py:func:`khoros.objects.archives.unarchive`
    * :py:func:`khoros.objects.archives.structure_archive_payload`
    * :py:func:`khoros.objects.archives._valid_entries_type`
    * :py:func:`khoros.objects.archives._convert_entries_to_dict`
    * :py:func:`khoros.objects.archives._format_single_archive_entry`
* Added the :py:func:`khoros.structures.base.structure_exists` function.
* Added the :py:func:`khoros.structures.boards.board_exists` function.
* Added the :py:func:`khoros.structures.categories.category_exists` function.
* Added the :py:func:`khoros.structures.grouphubs.grouphub_exists` function.
* Added the :py:func:`khoros.structures.nodes.node_exists` function.
* Added the following methods in the :ref:`core structure subclasses <core-object-methods:Core Structure Subclasses (khoros.core.Khoros)>`:
    * :py:meth:`khoros.core.Khoros.Board.board_exists`
    * :py:meth:`khoros.core.Khoros.Category.category_exists`
    * :py:meth:`khoros.core.Khoros.GroupHub.grouphub_exists`
    * :py:meth:`khoros.core.Khoros.Node.node_exists`

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added the :py:mod:`khoros.objects.archives` module to the ``__all__`` special variable in the
  :py:mod:`khoros.objects` ``__init__`` module and configured it to be imported by default.
* Added several additional keys and values to the ``structure_types_to_tables`` dictionary in the
  :py:class:`khoros.structures.base.Mapping` class.

:doc:`Return to Top <changelog>`

|

-----

******
v2.6.0
******
**Release Date: 2020-05-31**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:class:`khoros.core.Khoros.GroupHub` inner class with the following methods:
    * :py:meth:`khoros.core.Khoros.GroupHub.create`
    * :py:meth:`khoros.core.Khoros.GroupHub.structure_payload`
    * :py:meth:`khoros.core.Khoros.GroupHub.get_total_count`
    * :py:meth:`khoros.core.Khoros.GroupHub.update_title`
* Added the :py:meth:`khoros.core.Khoros._import_grouphub_class` and its accompanying method call.
* Added the :py:mod:`khoros.structures.grouphubs` module to the ``__all__`` special variable in the
  :py:mod:`khoros.structures` ``__init__`` module and configured the module to import by default.
* Added the :py:func:`khoros.structures.boards.get_board_id` function.
* Added the :py:meth:`khoros.core.Khoros.Board.structure_payload` and
  :py:meth:`khoros.core.Khoros.Board.get_board_id` methods.
* Added the :py:func:`khoros.api.format_avatar_payload` function.
* Added the :py:func:`khoros.api.combine_json_and_avatar_payload` function.
* Added the :py:mod:`khoros.structures.grouphubs` module with the following functions:
    * :py:func:`khoros.structures.grouphubs.create`
    * :py:func:`khoros.structures.grouphubs._create_group_hub_with_avatar`
    * :py:func:`khoros.structures.grouphubs._create_group_hub_without_avatar`
    * :py:func:`khoros.structures.grouphubs.structure_payload`
    * :py:func:`khoros.structures.grouphubs._structure_simple_string_fields`
    * :py:func:`khoros.structures.grouphubs._structure_membership_type`
    * :py:func:`khoros.structures.grouphubs._structure_discussion_styles`
    * :py:func:`khoros.structures.grouphubs._structure_parent_category`
    * :py:func:`khoros.structures.grouphubs.get_total_count`
    * :py:func:`khoros.structures.grouphubs.get_grouphub_id`
    * :py:func:`khoros.structures.grouphubs.refresh_enabled_discussion_styles`
    * :py:func:`khoros.structures.grouphubs._remove_disabled_discussion_styles`
    * :py:func:`khoros.structures.grouphubs.update_title`
    * :py:func:`khoros.structures.grouphubs._verify_group_hub_id`
* Added the :py:func:`khoros.structures.categories.get_total_count` function to replace the deprecated
  :py:func:`khoros.structures.categories.get_total_category_count` function.
* Added the :py:meth:`khoros.core.Khoros.Category.get_total_count` method to replace the deprecated
  :py:meth:`khoros.core.Khoros.Category.get_total_category_count` method.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:mod:`khoros.utils.tests.test_board_creation` unit test module with the following functions:
    * :py:func:`khoros.utils.tests.test_board_creation.set_package_path`
    * :py:func:`khoros.utils.tests.test_board_creation.import_boards_module`
    * :py:func:`khoros.utils.tests.test_board_creation.import_exceptions_module`
    * :py:func:`khoros.utils.tests.test_board_creation.initialize_khoros_object`
    * :py:func:`khoros.utils.tests.test_board_creation.get_required_fields`
    * :py:func:`khoros.utils.tests.test_board_creation.get_dict_for_required_fields`
    * :py:func:`khoros.utils.tests.test_board_creation.verify_data_fields`
    * :py:func:`khoros.utils.tests.test_board_creation.test_required_fields`
    * :py:func:`khoros.utils.tests.test_board_creation.test_valid_board_types`
    * :py:func:`khoros.utils.tests.test_board_creation.test_no_arguments`
    * :py:func:`khoros.utils.tests.test_board_creation.test_invalid_board_type`
    * :py:func:`khoros.utils.tests.test_board_creation.test_description`
* Added the :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError` exception class.
* Added the :py:func:`khoros.utils.helper._get_discussion_styles` function.

Documentation
-------------
Additions to the documentation.

* Added the :py:mod:`khoros.structures.grouphubs` module to the :doc:`Primary Modules <primary-modules>` page.
* Added the :py:mod:`khoros.utils.tests.test_board_creation` module to the
  :doc:`Supporting Modules <supporting-modules>` page.
* Added a docstring for :py:func:`khoros.utils.core_utils._is_zero_length`.
* Added the ``discussion_styles`` field to the example helper file on the :doc:`introduction` page.

General
-------
* Added the ``helper.yml`` file in the ``examples/`` directory of the repository using the syntax found on
  the :doc:`introduction` page of the :doc:`documentation <index>`.
* Added the ``discussion_styles`` list to the ``examples/helper.yml`` file.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Renamed the :py:func:`khoros.structures.base._get_node_id` function to be
  :py:func:`khoros.structures.base.get_structure_id` and converted it from a private to public function.
* Added the ``gh-p`` and ``ct-p`` entries in the ``node_url_identifiers`` list within the
  :py:class:`khoros.structures.base.Mapping` class.
* Refactored the :py:func:`khoros.structures.categories.get_category_id` function to leverage the
  :py:func:`khoros.structures.base.get_structure_id` function.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Updated the :py:func:`khoros.utils.helper.get_helper_settings` function to capture the enabled discussion
  styles via the :py:func:`khoros.utils.helper._get_discussion_styles` function.
* Updated the :py:mod:`khoros.core.Khoros` class to define the enabled discussion styles even if a helper
  configuration file is not supplied.

Documentation
-------------
Changes to the documentation.

* Added a caution message to the docstring for :py:func:`khoros.structures.boards.create`.

Deprecated
==========
* Deprecated the :py:func:`khoros.structures.categories.get_total_category_count` function as it has been
  replaced with the :py:func:`khoros.structures.categories.get_total_count` function.
* Deprecated the :py:meth:`khoros.core.Khoros.Category.get_total_category_count` method as it has been
  replaced with the :py:meth:`khoros.core.Khoros.Category.get_total_count` method.

:doc:`Return to Top <changelog>`

|

-----

.. include:: changelogs/changelog-1.1.0-thru-2.5.2.rst
