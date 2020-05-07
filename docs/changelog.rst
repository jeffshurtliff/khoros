##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v2.3.0
******
**Release Date: TBD**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.api.encode_multipart_data` function.
* Added the following functions to the :py:mod:`khoros.objects.messages` module:
    * :py:func:`khoros.objects.messages.create_message`
    * :py:func:`khoros.objects.messages.construct_payload`
    * :py:func:`khoros.objects.messages._verify_required_fields`
    * :py:func:`khoros.objects.messages.parse_v2_response`
    * :py:func:`khoros.objects.messages._confirm_field_supplied`
* Created the :py:mod:`khoros.objects.attachments` module with the following functions:
    * :py:func:`khoros.objects.attachments.construct_multipart_payload`
    * :py:func:`khoros.objects.attachments.format_attachment_payload`
    * :py:func:`khoros.objects.attachments.get_list_items`
    * :py:func:`khoros.objects.attachments.get_file_upload_info`
    * :py:func:`khoros.objects.attachments._format_single_file`
    * :py:func:`khoros.objects.attachments._format_multiple_files`
* Created the :py:mod:`khoros.objects.albums` module with the following functions:
    * :py:func:`khoros.objects.albums.create_album`
    * :py:func:`khoros.objects.albums.format_album_json`
    * :py:func:`khoros.objects.albums._null_to_blank`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.core_utils.convert_single_value_to_tuple` function.
* Added the :py:func:`khoros.utils.core_utils.convert_string_to_tuple` function.
* Added the :py:exc:`khoros.errors.exceptions.DataMismatchError` exception class.

Documentation
-------------
Additions to the documentation.

* Added the :py:mod:`khoros.objects.messages` module to the :doc:`Primary Modules <primary-modules>` page.
* Added the :py:mod:`khoros.objects.albums` module to the :doc:`Primary Modules <primary-modules>` page.
* Added the :py:mod:`khoros.objects.attachments` module to the :doc:`Primary Modules <primary-modules>` page.

General
-------
* Added ``requests-toolbelt==0.9.1`` to the ``requirements.txt`` file.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:class:`khoros.core.Khoros` class so that environment variables are ignored if a Helper
  configuration file is supplied when instantiating the core object.
* Added the ability to perform ``multipart/form-data`` API calls in functions below.
    * :py:func:`khoros.api.post_request_with_retries`
    * :py:func:`khoros.api.put_request_with_retries`
    * :py:func:`khoros.api._api_request_with_payload`
* Added the associated exception type (e.g. ``ValueError``) to the failure messages in
  :py:func:`khoros.api.get_request_with_retries` and :py:func:`khoros.api._api_request_with_payload`.
* Updated the :py:func:`khoros.api.get_request_with_retries` to use the
  :py:exc:`khoros.errors.exceptions.APIConnectionError` exception class rather than :py:exc:`ConnectionError`.
* Updated the :py:func:`khoros.api.get_request_with_retries` and :py:func:`khoros.api._api_request_with_payload`
  functions to only retry if relevant exception classes are raised in the try/except.
* Added functionality to :py:func:`khoros.api.post_request_with_retries` and
  :py:func:`khoros.api.put_request_with_retries` to display an error but still return the API response if unable
  to convert the response to JSON format when requested.
* Renamed the :py:func:`khoros.api.__api_request_with_payload` function to be
  :py:func:`khoros.api._api_request_with_payload` instead.
* Replaced :py:func:`print` statements in the :py:func:`khoros.api.get_request_with_retries` and
  :py:func:`khoros.api._api_request_with_payload` functions with :py:func:`khoros.errors.handlers.eprint`
  function calls.

Documentation
-------------
Changes to the documentation.

* Added a full docstring to the :py:func:`khoros.api._api_request_with_payload` function.

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Removed the Aurea reference from the failure message in :py:exc:`khoros.api._api_request_with_payload`.


|

******
v2.2.0
******
**Release Date: 2020-04-26**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the ability to use environmental variables to initialize the :py:mod:`khoros.core.Khoros` object.
    * Added the :py:meth:`khoros.core.Khoros._parse_env_settings` method to parse the environmental variables.
* Added the :py:meth:`khoros.core.Khoros._session_auth_credentials_defined` method to automatically set the
  ``auth_type`` value in the ``_settings`` attribute to be ``session_auth`` if a session authentication username
  and password have been defined.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:mod:`khoros.utils.environment` module with the following functions and constants:
    * :py:func:`khoros.utils.environment.get_env_variables`
    * :py:func:`khoros.utils.environment._env_variable_exists`
    * :py:func:`khoros.utils.environment._get_env_variable_value`
    * :py:func:`khoros.utils.environment.update_env_variable_names`
    * :py:func:`khoros.utils.environment._update_env_list`
    * :py:func:`khoros.utils.environment._update_env_mapping`
    * :py:func:`khoros.utils.environment._import_custom_names_file`
    * :py:const:`khoros.utils.environment.ENV_VARIABLE_NAMES`
* Added the :py:func:`khoros.utils.core_utils.get_file_type` function.
* Added the :py:exc:`khoros.errors.exceptions.UnknownFileTypeError` exception class.
* Added the :py:mod:`khoros.utils.tests.test_helper_file` unit test module.

Examples
--------
New additions to the example files for the library.

* Added the ``custom_env_variables.json`` file.
* Added the ``custom_env_variables.yml`` file.

Documentation
-------------
Additions to the documentation.

* Added the :py:mod:`khoros.utils.environment` module to the :doc:`Supporting Modules <supporting-modules>` page.
* Added the :py:mod:`khoros.utils.tests.test_helper_file` module to the
  :doc:`Supporting Modules <supporting-modules>` page.

General
-------
* Added the encrypted YAML Helper configuration file ``khoros_helper.yml.gpg`` in the
  ``khoros/utils/tests/`` directory for use with :py:mod:`pytest`.
* Added the shell script ``decrypt_helper.sh`` in the ``.github/scripts/`` directory per
  `GitHub guidelines <https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets>`_.
* Updated the ``pythonpackage.yml`` workflow for GitHub Actions to decrypt the helper configuration file (YAML)
  and utilize environment variables.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Made an adjustment to the :py:class:`khoros.core.Khoros` object class so that any values explicitly passed via
  the ``settings`` argument will overwrite any existing settings defined by default values and/or
  environmental variables.
* Added :py:mod:`khoros.structures.base` to the ``__all__`` special variable in :py:mod:`khoros.structures`.
* Added :py:mod:`khoros.objects.messages` to the ``__all__`` special variable in :py:mod:`khoros.objects` and added
  an ``import`` statement to import the module by default.
* Removed :py:mod:`khoros.objects.base` from the ``__all__`` special variable in :py:mod:`khoros.objects` and removed
  the ``import`` statement to prevent the module from being imported by default.

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>`.

* Replaced the ``yaml.load()`` function call with ``yaml.safe_load()`` in
  :py:func:`khoros.utils.helper.import_yaml_file` as it is a better security practice.
* Introduced support for JSON formatted helper configuration files in :py:mod:`khoros.utils.helper`.
* Removed the extra preceding underscore in private functions within :py:mod:`khoros.utils.helper`.

Documentation
-------------
Changes to the documentation.

* Added ``:special-members: __init__`` to the :py:mod:`khoros` and :py:mod:`khoros.core` modules to display the
  docstrings for the ``__init__`` method in the :py:class:`khoros.core.Khoros` object class.
* Replaced ``NoneType`` with ``None`` in function and method docstrings to use proper syntax and to comply with
  `PEP 287 <https://www.python.org/dev/peps/pep-0287/>`_.

|

******
v2.1.0
******
**Release Date: 2020-04-23**

Added
=====

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`khoros.liql.get_total_count` function.
* Added the :py:meth:`khoros.core.Khoros.get_total_count` method within the core Khoros object.
* Added the :py:mod:`khoros.structures` module.
* Added the :py:mod:`khoros.structures.base` module with the following functions and class:
    * :py:func:`khoros.structures.base.get_details`
    * :py:func:`khoros.structures.base._check_url_for_identifier`
    * :py:func:`khoros.structures.base.get_structure_field`
    * :py:func:`khoros.structures.base.is_category_url`
    * :py:func:`khoros.structures.base.is_node_url`
    * :py:func:`khoros.structures.base.verify_structure_type`
    * :py:func:`khoros.structures.base.get_structure_type_from_url`
    * :py:class:`khoros.structures.base.Mapping`
* Added the :py:mod:`khoros.structures.categories` module with the following functions:
    * :py:func:`khoros.structures.categories.get_category_id`
    * :py:func:`khoros.structures.categories.get_total_category_count`
    * :py:func:`khoros.structures.categories.get_category_details`
    * :py:func:`khoros.structures.categories.get_category_field`
    * :py:func:`khoros.structures.categories.get_url`
    * :py:func:`khoros.structures.categories.get_title`
    * :py:func:`khoros.structures.categories.get_description`
    * :py:func:`khoros.structures.categories.get_parent_type`
    * :py:func:`khoros.structures.categories.get_parent_id`
    * :py:func:`khoros.structures.categories.get_parent_url`
    * :py:func:`khoros.structures.categories.get_root_type`
    * :py:func:`khoros.structures.categories.get_root_id`
    * :py:func:`khoros.structures.categories.get_root_url`
    * :py:func:`khoros.structures.categories.get_language`
    * :py:func:`khoros.structures.categories.is_hidden`
    * :py:func:`khoros.structures.categories.get_views`
    * :py:func:`khoros.structures.categories.friendly_date_enabled`
    * :py:func:`khoros.structures.categories.get_friendly_date_max_age`
    * :py:func:`khoros.structures.categories.get_active_skin`
    * :py:func:`khoros.structures.categories.get_depth`
    * :py:func:`khoros.structures.categories.get_position`
    * :py:func:`khoros.structures.categories.get_creation_date`
* Added the :py:mod:`khoros.structures.communities` module with the following functions:
    * :py:func:`khoros.structures.communities.get_community_details`
    * :py:func:`khoros.structures.communities._check_for_multiple_tenants`
    * :py:func:`khoros.structures.communities.get_community_field`
    * :py:func:`khoros.structures.communities.get_tenant_id`
    * :py:func:`khoros.structures.communities.get_title`
    * :py:func:`khoros.structures.communities.get_description`
    * :py:func:`khoros.structures.communities.get_primary_url`
    * :py:func:`khoros.structures.communities.get_max_attachments`
    * :py:func:`khoros.structures.communities.get_permitted_attachment_types`
    * :py:func:`khoros.structures.communities.email_confirmation_required_to_post`
    * :py:func:`khoros.structures.communities.get_language`
    * :py:func:`khoros.structures.communities.get_ooyala_player_branding_id`
    * :py:func:`khoros.structures.communities.get_date_pattern`
    * :py:func:`khoros.structures.communities.friendly_date_enabled`
    * :py:func:`khoros.structures.communities.get_friendly_date_max_age`
    * :py:func:`khoros.structures.communities.get_active_skin`
    * :py:func:`khoros.structures.communities.get_sign_out_url`
    * :py:func:`khoros.structures.communities.get_creation_date`
    * :py:func:`khoros.structures.communities.top_level_categories_enabled`
    * :py:func:`khoros.structures.communities.show_community_node_in_breadcrumb`
    * :py:func:`khoros.structures.communities.show_breadcrumb_at_top_level`
    * :py:func:`khoros.structures.communities.top_level_categories_on_community_page`
* Added the :py:mod:`khoros.structures.nodes` module with the following functions and classes:
    * :py:func:`khoros.structures.nodes.get_node_id`
    * :py:func:`khoros.structures.nodes.get_node_type_from_url`
    * :py:func:`khoros.structures.nodes._get_node_type_identifier`
    * :py:func:`khoros.structures.nodes.get_total_node_count`
    * :py:func:`khoros.structures.nodes.get_node_details`
    * :py:func:`khoros.structures.nodes.get_node_field`
    * :py:func:`khoros.structures.nodes.get_url`
    * :py:func:`khoros.structures.nodes.get_type`
    * :py:func:`khoros.structures.nodes.get_discussion_style`
    * :py:func:`khoros.structures.nodes.get_title`
    * :py:func:`khoros.structures.nodes.get_description`
    * :py:func:`khoros.structures.nodes.get_parent_type`
    * :py:func:`khoros.structures.nodes.get_parent_id`
    * :py:func:`khoros.structures.nodes.get_parent_url`
    * :py:func:`khoros.structures.nodes.get_root_type`
    * :py:func:`khoros.structures.nodes.get_root_id`
    * :py:func:`khoros.structures.nodes.get_root_url`
    * :py:func:`khoros.structures.nodes.get_avatar_url`
    * :py:func:`khoros.structures.nodes.get_creation_date`
    * :py:func:`khoros.structures.nodes.get_depth`
    * :py:func:`khoros.structures.nodes.get_position`
    * :py:func:`khoros.structures.nodes.is_hidden`
    * :py:func:`khoros.structures.nodes.get_views`
    * :py:class:`khoros.structures.nodes.Mapping`
* Added the :py:class:`khoros.core.Khoros.Category` inner class with the following methods:
    * :py:meth:`khoros.core.Khoros.Category.get_category_id`
    * :py:meth:`khoros.core.Khoros.Category.get_total_category_count`
    * :py:meth:`khoros.core.Khoros.Category.get_category_details`
    * :py:meth:`khoros.core.Khoros.Category.get_category_field`
    * :py:meth:`khoros.core.Khoros.Category.get_url`
    * :py:meth:`khoros.core.Khoros.Category.get_title`
    * :py:meth:`khoros.core.Khoros.Category.get_description`
    * :py:meth:`khoros.core.Khoros.Category.get_parent_type`
    * :py:meth:`khoros.core.Khoros.Category.get_parent_id`
    * :py:meth:`khoros.core.Khoros.Category.get_parent_url`
    * :py:meth:`khoros.core.Khoros.Category.get_root_type`
    * :py:meth:`khoros.core.Khoros.Category.get_root_id`
    * :py:meth:`khoros.core.Khoros.Category.get_root_url`
    * :py:meth:`khoros.core.Khoros.Category.get_language`
    * :py:meth:`khoros.core.Khoros.Category.is_hidden`
    * :py:meth:`khoros.core.Khoros.Category.get_views`
    * :py:meth:`khoros.core.Khoros.Category.friendly_date_enabled`
    * :py:meth:`khoros.core.Khoros.Category.get_friendly_date_max_age`
    * :py:meth:`khoros.core.Khoros.Category.get_active_skin`
    * :py:meth:`khoros.core.Khoros.Category.get_depth`
    * :py:meth:`khoros.core.Khoros.Category.get_position`
    * :py:meth:`khoros.core.Khoros.Category.get_creation_date`
* Added the :py:class:`khoros.core.Khoros.Community` inner class with the following methods:
    * :py:meth:`khoros.core.Khoros.Community.get_community_details`
    * :py:meth:`khoros.core.Khoros.Community.get_tenant_id`
    * :py:meth:`khoros.core.Khoros.Community.get_title`
    * :py:meth:`khoros.core.Khoros.Community.get_description`
    * :py:meth:`khoros.core.Khoros.Community.get_primary_url`
    * :py:meth:`khoros.core.Khoros.Community.get_max_attachments`
    * :py:meth:`khoros.core.Khoros.Community.get_permitted_attachment_types`
    * :py:meth:`khoros.core.Khoros.Community.email_confirmation_required_to_post`
    * :py:meth:`khoros.core.Khoros.Community.get_language`
    * :py:meth:`khoros.core.Khoros.Community.get_ooyala_player_branding_id`
    * :py:meth:`khoros.core.Khoros.Community.get_date_pattern`
    * :py:meth:`khoros.core.Khoros.Community.friendly_date_enabled`
    * :py:meth:`khoros.core.Khoros.Community.get_friendly_date_max_age`
    * :py:meth:`khoros.core.Khoros.Community.get_active_skin`
    * :py:meth:`khoros.core.Khoros.Community.get_sign_out_url`
    * :py:meth:`khoros.core.Khoros.Community.get_creation_date`
    * :py:meth:`khoros.core.Khoros.Community.top_level_categories_enabled`
    * :py:meth:`khoros.core.Khoros.Community.show_community_node_in_breadcrumb`
    * :py:meth:`khoros.core.Khoros.Community.show_breadcrumb_at_top_level`
    * :py:meth:`khoros.core.Khoros.Community.top_level_categories_on_community_page`
* Added the following methods to the :py:class:`khoros.core.Khoros.Node` inner class:
    * :py:meth:`khoros.core.Khoros.Node.get_total_node_count`
    * :py:meth:`khoros.core.Khoros.Node.get_node_details`
    * :py:meth:`khoros.core.Khoros.Node.get_node_field`
    * :py:meth:`khoros.core.Khoros.Node.get_url`
    * :py:meth:`khoros.core.Khoros.Node.get_type`
    * :py:meth:`khoros.core.Khoros.Node.get_discussion_style`
    * :py:meth:`khoros.core.Khoros.Node.get_title`
    * :py:meth:`khoros.core.Khoros.Node.get_description`
    * :py:meth:`khoros.core.Khoros.Node.get_parent_type`
    * :py:meth:`khoros.core.Khoros.Node.get_parent_id`
    * :py:meth:`khoros.core.Khoros.Node.get_parent_url`
    * :py:meth:`khoros.core.Khoros.Node.get_root_type`
    * :py:meth:`khoros.core.Khoros.Node.get_root_id`
    * :py:meth:`khoros.core.Khoros.Node.get_root_url`
    * :py:meth:`khoros.core.Khoros.Node.get_avatar_url`
    * :py:meth:`khoros.core.Khoros.Node.get_creation_date`
    * :py:meth:`khoros.core.Khoros.Node.get_depth`
    * :py:meth:`khoros.core.Khoros.Node.get_position`
    * :py:meth:`khoros.core.Khoros.Node.is_hidden`
    * :py:meth:`khoros.core.Khoros.Node.get_views`
* Added the :py:meth:`khoros.core.Khoros._import_category_class` method and accompanying method call.
* Added the :py:meth:`khoros.core.Khoros._import_community_class` method and accompanying method call.
* Added the :py:const:`khoros.liql.COLLECTIONS` constant.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`khoros.utils.core_utils.display_warning` function.
* Added the following exception classes:
    * :py:exc:`khoros.errors.exceptions.InvalidFieldError`
    * :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`
    * :py:exc:`khoros.errors.exceptions.InvalidURLError`

Documentation
-------------
Additions to the documentation.

* Added the :py:mod:`khoros.structures` module and its submodules to the :doc:`Primary Modules <primary-modules>` page.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Updated the :py:mod:`khoros.objects` to import all submodules by default.
* Moved the :py:func:`khoros.objects.base.get_node_id` function to the :py:mod:`khoros.structures.nodes` module
  and added a :py:exc:`DeprecationWarning`.
* Moved the :py:func:`khoros.objects.base.get_node_type_from_url` function to the :py:mod:`khoros.structures.nodes`
  module and added a :py:exc:`DeprecationWarning`.
* Moved the :py:func:`khoros.objects.base.__get_node_type_identifier` function to the :py:mod:`khoros.structures.nodes`
  module and added a :py:exc:`DeprecationWarning`.
* Moved the :py:class:`khoros.objects.base.Mapping` class to the :py:mod:`khoros.structures.nodes` module and added
  a :py:exc:`DeprecationWarning`.
* Added the :py:const:`khoros.structures.nodes.Mapping.avatar_size_mapping` dictionary.

Fixed
=====

Primary Modules
---------------
Fixes to the :doc:`primary modules <primary-modules>`.

* Removed some print debugging that hadn't been removed in the :py:func:`khoros.api.query_successful` function.

Documentation
-------------
Fixes to the documentation.

* Fixed the module name in the header docstring for the :py:mod:`khoros.objects` module.
* Fixed a typo in the docstring for the :py:func:`khoros.objects.users.query_users_table_by_id` function.

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Fixed the :py:mod:`khoros.utils.tests.test_node_id_extract` to use the new :py:mod:`khoros.structures.nodes` module.

|

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
