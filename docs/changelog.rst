##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

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
