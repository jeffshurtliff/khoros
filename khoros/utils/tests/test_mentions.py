# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_mentions
:Synopsis:       This module is used by pytest to verify that user and content mentions work properly
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  11 Mar 2021
"""

import os
import re
import sys

import pytest

from khoros.objects import messages
from khoros.errors import exceptions
from khoros import Khoros

CORRECT_CONTENT_MENTION = '<li-message title="Click Here" uid="6560" url=' + \
                          '"https://community.khoros.com/t5/Community-FAQs/' + \
                          'Understanding-SEO-Friendly-URLs/ta-p/6560"></li-message>'
CORRECT_USER_MENTION = '<li-user uid="1" login="@admin"></li-user>'


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionadded:: 2.4.0
    """
    sys.path.insert(0, os.path.abspath('../..'))
    return


def expected_content_response(response):
    """This function replaces the TLD to match the example constant and then identifies if the response was expected.

    .. versionadded:: 2.4.0

    :param response: The response received from the function
    :type response: str
    :returns: Boolean value indicating if the response was expected
    """
    response = re.sub(r'https://.*\.com/t5', 'https://community.khoros.com/t5', response)
    return True if response == CORRECT_CONTENT_MENTION else False


def expected_user_response(response):
    """This function identifies if the response was expected.

    .. versionadded:: 2.4.0

    :param response: The response received from the function
    :type response: str
    :returns: Boolean value indicating if the response was expected
    """
    return True if response == CORRECT_USER_MENTION else False


def get_content_test_data(include_id=True, false_id=False, relative_url=False):
    """This function returns the test data to use in the various test functions.

    .. versionadded:: 2.4.0

    :param include_id: Determines if the Content ID should be returned (``True`` by default)
    :type include_id: bool
    :param false_id: Determines if an incorrect Content ID should be returned (``False`` by default)
    :type false_id: bool
    :param relative_url: Determines if a relative URL should be returned (``False`` by default)
    :returns: A tuple containing the appropriate test data
    """
    title = "Click Here"
    url = "https://community.khoros.com/t5/Community-FAQs/Understanding-SEO-Friendly-URLs/ta-p/6560"
    content_id = "6560"
    false_content_id = "12345"
    if relative_url:
        url = url.split('khoros.com')[1]
    data = [title, url]
    if include_id:
        if false_id:
            data.append(false_content_id)
        else:
            data.append(content_id)
    return tuple(data)


def get_user_test_data():
    """This function returns the test data to use in the user mention tests.

    .. versionadded:: 2.4.0

    :returns: The User ID and login as a tuple of two strings
    """
    user_id = '1'
    login = 'admin'
    return user_id, login


def test_content_mention_with_all_arguments():
    """This function tests the :py:func:`khoros.objects.messages.format_content_mention` when all required arguments
       have been supplied.

    .. versionadded:: 2.4.0

    :returns: None
    """
    title, url, content_id = get_content_test_data()
    response = messages.format_content_mention(content_id=content_id, title=title, url=url)
    assert response == CORRECT_CONTENT_MENTION      # nosec
    return


def test_content_mention_with_full_dict():
    """This function tests the :py:func:`khoros.objects.messages.format_content_mention` when all required dictionary
       keys and values have been supplied.

    .. versionadded:: 2.4.0

    :returns: None
    """
    title, url, content_id = get_content_test_data()
    content_info = {
        'id': content_id,
        'title': title,
        'url': url
    }
    response = messages.format_content_mention(content_info=content_info)
    assert response == CORRECT_CONTENT_MENTION      # nosec
    return


@pytest.mark.filterwarnings("error")
def test_content_mention_with_no_id_arg():
    """This function tests creating a content mention when no Content ID has been supplied as an argument.

    .. versionadded:: 2.4.0

    :returns: None
    """
    title, url = get_content_test_data(include_id=False)
    response = messages.format_content_mention(title=title, url=url)
    assert response == CORRECT_CONTENT_MENTION      # nosec
    return


@pytest.mark.filterwarnings("error")
def test_content_mention_with_no_id_dict():
    """This function tests creating a content mention when no Content ID has been supplied in the dictionary.

    .. versionadded:: 2.4.0

    :returns: None
    """
    title, url = get_content_test_data(include_id=False)
    content_info = {'title': title, 'url': url}
    response = messages.format_content_mention(content_info=content_info)
    assert response == CORRECT_CONTENT_MENTION      # nosec
    return


def test_content_mention_with_false_id_arg():
    """This function tests creating a content mention when an invalid Content ID is supplied as an argument.

    .. versionadded:: 2.4.0

    :returns: None
    """
    title, url, content_id = get_content_test_data(false_id=True)
    with pytest.warns(UserWarning):
        response = messages.format_content_mention(content_id=content_id, title=title, url=url)
    assert response == CORRECT_CONTENT_MENTION      # nosec
    return


def test_content_mention_with_false_id_dict():
    """This function tests creating a content mention when an invalid Content ID is supplied in the dictionary.

    .. versionadded:: 2.4.0

    :returns: None
    """
    title, url, content_id = get_content_test_data(false_id=True)
    content_info = {
        'id': content_id,
        'title': title,
        'url': url
    }
    with pytest.warns(UserWarning):
        response = messages.format_content_mention(content_info=content_info)
    assert response == CORRECT_CONTENT_MENTION      # nosec
    return


def test_bad_content_url():
    """This function tests creating a content mention when an invalid URL is supplied.

    .. versionadded:: 2.4.0

    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`
    """
    title = "Click Here"
    url = "https://khoros.com/platform/communities"

    # Testing with arguments
    with pytest.raises(exceptions.MessageTypeNotFoundError):
        messages.format_content_mention(title=title, url=url)

    # Testing with content dictionary
    content_info = {'title': title, 'url': url}
    with pytest.raises(exceptions.MessageTypeNotFoundError):
        messages.format_content_mention(content_info=content_info)
    return


def test_relative_content_url_without_object():
    """This function tests creating a content mention with a relative content URL and no Khoros object.

    .. versionadded:: 2.4.0

    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    title, url, content_id = get_content_test_data(relative_url=True)

    # Testing arguments with and without a Content ID
    with pytest.raises(exceptions.MissingRequiredDataError):
        messages.format_content_mention(title=title, url=url)
        messages.format_content_mention(content_id=content_id, title=title, url=url)

    # Testing dictionary with and without a Content ID
    content_info = {'title': title, 'url': url}
    with pytest.raises(exceptions.MissingRequiredDataError):
        messages.format_content_mention(content_info=content_info)
        content_info['id'] = content_id
        messages.format_content_mention(content_info=content_info)
    return


@pytest.mark.skip(reason="Session key doesn't work in GitHub Actions CI.")
def test_relative_content_url_with_object():
    """This function tests creating a content mention with a relative content URL but with a Khoros object.

    .. versionadded:: 2.4.0

    :returns: None
    """
    title, url, content_id = get_content_test_data(relative_url=True)
    khoros = Khoros()
    print()

    # Testing arguments without a Content ID
    response = messages.format_content_mention(khoros, title=title, url=url)
    assert expected_content_response(response)      # nosec

    # Testing arguments with a Content ID
    response = messages.format_content_mention(khoros, content_id=content_id, title=title, url=url)
    assert expected_content_response(response)      # nosec

    # Testing dictionary without a Content ID
    content_info = {'title': title, 'url': url}
    response = messages.format_content_mention(khoros, content_info)
    assert expected_content_response(response)      # nosec

    # Testing dictionary with a Content ID
    content_info['id'] = content_id
    response = messages.format_content_mention(khoros, content_info)
    assert expected_content_response(response)      # nosec
    return


def test_user_mention_with_arguments():
    """This function tests creating a user mention with all required arguments provided.

    .. versionadded:: 2.4.0

    :returns: None
    """
    user_id, login = get_user_test_data()
    response = messages.format_user_mention(user_id=user_id, login=login)
    assert expected_user_response(response)
    return


def test_user_mention_with_dictionary():
    """This function tests creating a user mention with all required dictionary key value pairs provided.

    .. versionadded:: 2.4.0

    :returns: None
    """
    user_id, login = get_user_test_data()
    user_info = {'id': user_id, 'login': login}
    response = messages.format_user_mention(user_info=user_info)
    assert expected_user_response(response)
    return


def test_user_mention_with_args_no_object():
    """This function tests creating a user mention with a single argument and no Khoros object.

    .. versionadded:: 2.4.0

    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
    """
    user_id, login = get_user_test_data()

    # Test with no login
    with pytest.raises(exceptions.MissingAuthDataError):
        messages.format_user_mention(user_id=user_id)

    # Test with no User ID
    with pytest.raises(exceptions.MissingAuthDataError):
        messages.format_user_mention(login=login)
    return


def test_user_mention_with_dictionary_no_object():
    """This function tests creating a user mention with a single key value pair and no Khoros object.

    .. versionadded:: 2.4.0

    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
    """
    user_id, login = get_user_test_data()
    user_info_id = {'id': user_id}
    user_info_login = {'login': login}

    # Test with no login
    with pytest.raises(exceptions.MissingAuthDataError):
        messages.format_user_mention(user_info=user_info_id)

    # Test with no User ID
    with pytest.raises(exceptions.MissingAuthDataError):
        messages.format_user_mention(user_info=user_info_login)
    return


@pytest.mark.skip(reason="Session key doesn't work in GitHub Actions CI.")
def test_user_mention_with_dict_and_object():
    """This function tests creating a user mention with one key value pair and with a Khoros object.

    .. versionadded:: 2.4.0

    :returns: None
    """
    user_id, login = get_user_test_data()
    user_info_id = {'id': user_id}
    user_info_login = {'login': login}
    khoros = Khoros()

    # Test with no login
    response = messages.format_user_mention(khoros, user_info_id)
    assert expected_user_response(response)

    # Test with no User ID
    response = messages.format_user_mention(khoros, user_info_login)
    assert expected_user_response(response)
    return


# TODO: Add test for not existent user
