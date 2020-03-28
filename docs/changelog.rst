##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v1.2.1
******
**Release Date: TBD**

Added
=====

General
-------
* Added *PyCharm Python Security Scanner* to the
  `pythonpackage.yml <https://github.com/jeffshurtliff/khorosjx/blob/master/.github/workflows/pythonpackage.yml>`_ file.

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
