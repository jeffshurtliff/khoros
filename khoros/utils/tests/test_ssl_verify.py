# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_ssl_verify
:Synopsis:       This module is used by pytest to test the ability to disable SSL verification on API requests
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  02 Oct 2021
"""

from . import resources


def test_default_core_object_setting():
    """This function tests to verify the ``ssl_verify`` setting is ``True`` by default.

    .. versionadded:: 4.3.0
    """
    khoros = resources.initialize_khoros_object()
    assert khoros.core_settings.get('ssl_verify') is True       # nosec
    return


def test_core_object_with_param_setting():
    """This function tests to verify the ``ssl_verify`` setting is honored when explicitly defined.

    .. versionadded:: 4.3.0
    """
    defined_setting = {'ssl_verify': False}
    khoros = resources.initialize_khoros_object(use_defined_settings=True, defined_settings=defined_setting,
                                                append_to_default=True)
    assert khoros.core_settings.get('ssl_verify') is False      # nosec


def test_api_global_variable_assignment():
    """This function tests to verify that the ``ssl_verify_disabled`` global variable gets defined appropriately.

    .. versionadded:: 4.3.0
    """
    defined_setting = {'ssl_verify': False}
    khoros = resources.initialize_khoros_object(use_defined_settings=True, defined_settings=defined_setting,
                                                append_to_default=True)
    assert api.ssl_verify_disabled is True


def test_api_should_verify_function():
    """This function tests to verify that the :py:func:`khoros.api.should_verify_tls` function works properly.

    .. versionadded:: 4.3.0
    """
    defined_setting = {'ssl_verify': False}
    khoros = resources.initialize_khoros_object(use_defined_settings=True, defined_settings=defined_setting,
                                                append_to_default=True)
    assert api.should_verify_tls(khoros) is False
    assert api.should_verify_tls() is False


# Import modules and initialize the core object
api, exceptions = resources.import_modules('khoros.api', 'khoros.errors.exceptions')
