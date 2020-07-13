##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v3.0.0
******
**Release Date: TBD**

Added
=====

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

Documentation
-------------
* Added the :doc:`changelog-1.1.0-thru-2.5.2.rst <changelogs/changelog-1.1.0-thru-2.5.2>` file
  and embedded it into this :doc:`changelog` page to have less content per RST document.
* Added :doc:`Return to Top <changelog>` links at the bottom of each version section.

Changed
=======

General
-------
* Updated the Sphinx configuration file (``conf.py``) to suppress the ``duplicate label`` warnings.
* Added version 3.0.x to the ``SECURITY.md`` file under Supported

:doc:`Return to Top <changelog>`

|

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

.. include:: changelogs/changelog-1.1.0-thru-2.5.2.rst
