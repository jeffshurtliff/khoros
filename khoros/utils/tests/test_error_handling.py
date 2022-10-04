# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_error_handling
:Synopsis:          This module is used by pytest to verify that error handling works properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Oct 2022
"""

import pytest

from . import resources
from ...errors import handlers, exceptions, translations


def test_eprint():
    """This function tests printing an error message to the stderr output.

    .. versionadded:: 5.1.2
    """
    handlers.eprint('This is an error message')


def test_get_html_error():
    """This function tests the ability to parse an HTML error to get an error message.

    .. versionadded:: 5.1.2
    """
    # TODO: Add a true error message from the API
    html_error = "<html><body><h1>404 Not Found</h1><b>Error description</b><u></u></body></html>"
    v1_error = 'The Community API v1 call failed with the following error:\n\t404 Not Found'
    assert handlers.get_error_from_html(html_error) == '404 Not Found'
    assert handlers.get_error_from_html(html_error, v1=True) == v1_error


def test_verify_core_object_present():
    """This function tests the ability to verify that a Khoros core object is present.

    .. versionadded:: 5.1.2
    """
    with pytest.raises(exceptions.MissingRequiredDataError):
        khoros_object = None
        handlers.verify_core_object_present(khoros_object)


def test_translate_error():
    """This function tests the ability to translate obscure messages.

    .. versionadded:: 5.1.2
    """
    error_msg = 'page.post.error.attachment_bad_extension'
    translated_error_excerpt = 'The attachment does not have an extension permitted'
    assert translated_error_excerpt in translations.translate_error(error_msg)


def test_translation_check():
    """This function tests the ability to check if error translation is enabled.

    .. versionadded:: 5.1.2
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Call the function and verify that it is a Boolean response
    setting = translations.translation_enabled(khoros_object=khoros_object)
    assert isinstance(setting, bool)


def test_parse_translation_error():
    """This function tests the ability to parse an error message to remove extraneous escape characters.

    .. versionadded:: 5.1.2
    """
    error_msg_with_escape_char = 'This is an error message\n'
    error_msg = 'This is an error message'
    parsed_msg = translations.parse_message(error_msg_with_escape_char)
    assert parsed_msg == error_msg
