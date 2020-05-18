# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.messages
:Synopsis:          This module includes functions that handle messages within a Khoros Community environment
:Usage:             ``from khoros.objects import messages``
:Example:           ``response = messages.create_message(khoros_obj, 'My First Message', 'Hello World',
                    node_id='support-tkb')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     09 May 2020
"""

import warnings

from . import attachments, users
from .. import api, liql, errors
from ..structures import nodes

REQUIRED_FIELDS = ['board', 'subject']
CONTEXT_KEYS = ['id', 'url']
SEO_KEYS = ['title', 'description', 'canonical_url']
MESSAGE_SEO_URLS = {
    'Blog Article': 'ba-p',
    'Blog Comment': 'bc-p',
    'Contest Item': 'cns-p',
    'Idea': 'idi-p',
    'Message': 'm-p',
    'Question': 'qaq-p',
    'TKB Article': 'ta-p',
    'Topic': 'td-p'
}


def create(khoros_object, subject=None, body=None, node=None, node_id=None, node_url=None, canonical_url=None,
           context_id=None, context_url=None, cover_image=None, images=None, is_answer=None, is_draft=None,
           labels=None, product_category=None, products=None, read_only=None, seo_title=None, seo_description=None,
           tags=None, teaser=None, topic=None, videos=None, attachment_file_paths=None, full_response=False,
           return_id=False, return_url=False, return_api_url=False, return_http_code=False):
    """This function creates a new message within a given node.

    .. versionadded:: 2.3.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param subject: The title or subject of the message
    :type subject: str, None
    :param body: The body of the message in HTML format
    :type body: str, None
    :param node: A dictionary containing the ``id`` key and its associated value indicating the destination
    :type node: dict, None
    :param node_id: The ID of the node in which the message will be published
    :type node_id: str, None
    :param node_url: The URL of the node in which the message will be published

                     .. note:: This argument is necessary in the absence of the ``node`` and ``node_id`` arguments.

    :type node_url: str, None
    :param canonical_url: The search engine-friendly URL to the message
    :type canonical_url: str, None
    :param context_id: Metadata on a message to identify the message with an external identifier of your choosing
    :type context_id: str, None
    :param context_url: Metadata on a message representing a URL to associate with the message (external identifier)
    :type context_url: str, None
    :param cover_image: The cover image set for the message
    :type cover_image: dict, None
    :param images: The query to retrieve images uploaded to the message
    :type images: dict, None
    :param is_answer: Designates the message as an answer on a Q&A board
    :type is_answer: bool, None
    :param is_draft: Indicates whether or not the message is still a draft (i.e. unpublished)
    :type is_draft: bool, None
    :param labels: The query to retrieve labels applied to the message
    :type labels: dict, None
    :param product_category: The product category (i.e. container for ``products``) associated with the message
    :type product_category: dict, None
    :param products: The product in a product catalog associated with the message
    :type products: dict, None
    :param read_only: Indicates whether or not the message should be read-only or have replies/comments blocked
    :type read_only: bool, None
    :param seo_title: The title of the message used for SEO purposes
    :type seo_title: str, None
    :param seo_description: A description of the message used for SEO purposes
    :type seo_description: str, None
    :param tags: The query to retrieve tags applied to the message
    :type tags: dict, None
    :param teaser: The message teaser (used with blog articles)
    :type teaser: str, None
    :param topic: The root message of the conversation in which the message appears
    :type topic: dict, None
    :param videos: The query to retrieve videos uploaded to the message
    :type videos: dict, None
    :param attachment_file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type attachment_file_paths: str, tuple, list, set, None
    :param full_response: Defines if the full response should be returned instead of the outcome (``False`` by default)

                          .. caution:: This argument overwrites the ``return_id``, ``return_url``, ``return_api_url``
                                       and ``return_http_code`` arguments.

    :type full_response: bool
    :param return_id: Indicates that the **Message ID** should be returned (``False`` by default)
    :type return_id: bool
    :param return_url: Indicates that the **Message URL** should be returned (``False`` by default)
    :type return_url: bool
    :param return_api_url: Indicates that the **API URL** of the message should be returned (``False`` by default)
    :type return_api_url: bool
    :param return_http_code: Indicates that the **HTTP status code** of the response should be returned
                             (``False`` by default)
    :type return_http_code: bool
    :returns: Boolean value indicating a successful outcome (default) or the full API response
    :raises: :py:exc:`TypeError`, :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    api_url = f"{khoros_object.core['v2_base']}/messages"
    payload = construct_payload(subject, body, node, node_id, node_url, canonical_url, context_id, context_url,
                                is_answer, is_draft, read_only, seo_title, seo_description, teaser, tags, cover_image,
                                images, labels, product_category, products, topic, videos)
    multipart = True if attachment_file_paths else False
    if multipart:
        payload = attachments.construct_multipart_payload(payload, attachment_file_paths)
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object, multipart=multipart)
    return api.deliver_v2_results(response, full_response, return_id, return_url, return_api_url, return_http_code)


def construct_payload(subject=None, body=None, node=None, node_id=None, node_url=None, canonical_url=None,
                      context_id=None, context_url=None, is_answer=None, is_draft=None, read_only=None, seo_title=None,
                      seo_description=None, teaser=None, tags=None, cover_image=None, images=None, labels=None,
                      product_category=None, products=None, topic=None, videos=None):
    """This function constructs and properly formats the JSON payload for a messages API request.

    .. versionadded:: 2.3.0

    :param subject: The title or subject of the message
    :type subject: str, None
    :param body: The body of the message in HTML format
    :type body: str, None
    :param node: A dictionary containing the ``id`` key and its associated value indicating the destination
    :type node: dict, None
    :param node_id: The ID of the node in which the message will be published
    :type node_id: str, None
    :param node_url: The URL of the node in which the message will be published

                     .. note:: This argument is necessary in the absence of the ``node`` and ``node_id`` arguments.

    :type node_url: str, None
    :param canonical_url: The search engine-friendly URL to the message
    :type canonical_url: str, None
    :param context_id: Metadata on a message to identify the message with an external identifier of your choosing
    :type context_id: str, None
    :param context_url: Metadata on a message representing a URL to associate with the message (external identifier)
    :type context_url: str, None
    :param is_answer: Designates the message as an answer on a Q&A board
    :type is_answer: bool, None
    :param is_draft: Indicates whether or not the message is still a draft (i.e. unpublished)
    :type is_draft: bool, None
    :param read_only: Indicates whether or not the message should be read-only or have replies/comments blocked
    :type read_only: bool, None
    :param seo_title: The title of the message used for SEO purposes
    :type seo_title: str, None
    :param seo_description: A description of the message used for SEO purposes
    :type seo_description: str, None
    :param teaser: The message teaser (used with blog articles)
    :type teaser: str, None
    :param tags: The query to retrieve tags applied to the message
    :type tags: dict, None
    :param cover_image: The cover image set for the message
    :type cover_image: dict, None
    :param images: The query to retrieve images uploaded to the message
    :type images: dict, None
    :param labels: The query to retrieve labels applied to the message
    :type labels: dict, None
    :param product_category: The product category (i.e. container for ``products``) associated with the message
    :type product_category: dict, None
    :param products: The product in a product catalog associated with the message
    :type products: dict, None
    :param topic: The root message of the conversation in which the message appears
    :type topic: dict, None
    :param videos: The query to retrieve videos uploaded to the message
    :type videos: dict, None
    :returns: The properly formatted JSON payload
    """
    # Define the default payload structure
    payload = {
        "data": {
            "type": "message"
        }
    }

    # Ensure the required fields are defined
    _verify_required_fields(node, node_id, node_url, subject)

    # Define the destination
    if not node:
        if node_id:
            node = {"id": f"{node_id}"}
        else:
            node = {"id": f"{nodes.get_node_id(url=node_url)}"}
    payload['data']['board'] = node

    # Add supplied data where appropriate if string or Boolean
    supplied_data = {
        'body': (body, str),
        'subject': (subject, str),
        'canonical_url': (canonical_url, str),
        'context_id': (context_id, str),
        'context_url': (context_url, str),
        'is_answer': (is_answer, bool),
        'is_draft': (is_draft, bool),
        'read_only': (read_only, bool),
        'seo_title': (seo_title, str),
        'seo_description': (seo_description, str),
        'teaser': (teaser, str)
    }
    for field_name, field_value in supplied_data.items():
        if field_value[0]:
            if field_value[1] == str:
                payload['data'][field_name] = f"{field_value[0]}"
            elif field_value[1] == bool and type(field_value[0]) == str:
                # noinspection PyTypeChecker
                payload['data'][field_name] = bool(field_value[0])

    # TODO: Add functionality for non-string and non-Boolean arguments

    return payload


def _verify_required_fields(_node, _node_id, _node_url, _subject):
    """This function verifies that the required fields to create a message are satisfied.

    .. versionadded:: 2.3.0

    :param _node: A dictionary containing the ``id`` key and its associated value indicating the destination
    :type _node: dict
    :param _node_id: The ID of the node in which the message will be published
    :type _node_id: str
    :param _node_url: The URL of the node in which the message will be published

                     .. note:: This argument is necessary in the absence of the ``node`` and ``node_id`` arguments.

    :type _node_url: str
    :param _subject: The title or subject of the message
    :type _subject: str
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    _requirements_satisfied = True
    if (not _node and not _node_id and not _node_url) or (_node is not None and type(_node) != dict) or not _subject:
        _requirements_satisfied = False
    elif _node and (not _node_id and not _node_url):
        _requirements_satisfied = False if 'id' not in _node else True
    if not _requirements_satisfied:
        raise errors.exceptions.MissingRequiredDataError("A node and subject must be defined when creating messages")
    return


def _confirm_field_supplied(_fields_dict):
    """This function checks to ensure that at least one field has been enabled to retrieve.

    .. versionadded:: 2.3.0
    """
    _field_supplied = False
    for _field_value in _fields_dict.values():
        if _field_value[0]:
            _field_supplied = True
            break
    if not _field_supplied:
        raise errors.exceptions.MissingRequiredDataError("At least one field must be enabled to retrieve a response.")
    return


def parse_v2_response(json_response, return_dict=False, status=False, response_msg=False, http_code=False,
                      message_id=False, message_url=False, message_api_uri=False, v2_base=''):
    """This function parses an API response for a message operation (e.g. creating a message) and returns parsed data.

    .. deprecated:: 2.5.0
       Use the :py:func:`khoros.api.parse_v2_response` function instead.

    .. versionadded:: 2.3.0

    :param json_response: The API response in JSON format
    :type json_response: dict
    :param return_dict: Defines if the parsed data should be returned within a dictionary
    :type return_dict: bool
    :param status: Defines if the **status** value should be returned
    :type status: bool
    :param response_msg: Defines if the **developer response** message should be returned
    :type response_msg: bool
    :param http_code: Defines if the **HTTP status code** should be returned
    :type http_code: bool
    :param message_id: Defines if the **message ID** should be returned
    :type message_id: bool
    :param message_url: Defines if the **message URL** should be returned
    :type message_url: bool
    :param message_api_uri: Defines if the ** message API URI** should be returned
    :type message_api_uri: bool
    :param v2_base: The base URL for the API v2
    :type v2_base: str
    :returns: A string, tuple or dictionary with the parsed data
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    warnings.warn(f"This function is deprecated and 'khoros.api.parse_v2_response' should be used.", DeprecationWarning)
    return api.parse_v2_response(json_response, return_dict, status, response_msg, http_code, message_id, message_url,
                                 message_api_uri, v2_base)


def get_id_from_url(url):
    """This function retrieves the message ID from a given URL.

    .. versionadded:: 2.4.0

    :param url: The URL from which the ID will be parsed
    :type url: str
    :returns: The ID associated with the message in string format
    :raises: :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`
    """
    for msg_type in MESSAGE_SEO_URLS.values():
        if msg_type in url:
            return (url.split(f'{msg_type}/')[1]).split('#')[0]
    raise errors.exceptions.MessageTypeNotFoundError(url=url)


def _get_required_user_mention_data(_khoros_object, _user_info, _user_id, _login):
    _missing_data_error = "A User ID or login must be supplied to construct an user @mention"
    _info_fields = ['id', 'login']
    if not any((_user_info, _user_id, _login)):
        raise errors.exceptions.MissingRequiredDataError(_missing_data_error)
    elif not _user_id and not _login:
        if not any(_field in _info_fields for _field in _user_info):
            raise errors.exceptions.MissingRequiredDataError(_missing_data_error)
        else:
            if 'id' in _user_info:
                _user_id = _user_info.get('id')
            if 'login' in _user_info:
                _login = _user_info.get('login')
    if not _user_id or not _login:
        if not _khoros_object:
            raise errors.exceptions.MissingAuthDataError()
        if not _user_id:
            _user_id = users.get_user_id(_khoros_object, login=_login)
        elif not _login:
            _login = users.get_login(_khoros_object, user_id=_user_id)
    return _user_id, _login


def format_user_mention(khoros_object=None, user_info=None, user_id=None, login=None):
    """This function formats the ``<li-user>`` HTML tag for a user @mention.

    .. versionadded:: 2.4.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object

                          .. note:: This argument is necessary if only one of the user values (i.e. ``user_id`` or
                                    ``login``) are passed in the function, as a lookup will need to be performed to
                                    define the missing value.

    :type khoros_object: class[khoros.Khoros], None
    :param user_info: A dictionary containing the ``'id'`` and/or ``'login'`` key(s) with the user information

                      .. note:: This argument is necessary if the User ID and/or Login are not explicitly passed
                                using the ``user_id`` and/or ``login`` function arguments.

    :type user_info: dict, None
    :param user_id: The unique user identifier (i.e. User ID) for the user
    :type user_id: str, int, None
    :param login: The login (i.e. username) for the user
    :type login: str, None
    :returns: The properly formatted ``<li-user>`` HTML tag in string format
    :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    user_id, login = _get_required_user_mention_data(khoros_object, user_info, user_id, login)
    mention_tag = f'<li-user uid="{user_id}" login="@{login}"></li-user>'
    return mention_tag


def _report_missing_id_and_retrieve(_content_id, _url):
    """This function displays a ``UserWarning`` message if needed and then retrieves the correct ID from the URL.

    .. versionadded:: 2.4.0

    :param _content_id: The missing or incorrect ID of the message
    :type _content_id: str, int, None
    :param _url: The full URL of the message
    :type _url: str
    :returns: The appropriate ID of the message where possible
    :raises: :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`
    """
    if _content_id is not None:
        warnings.warn(f"The given ID '{_content_id}' is not found in the URL {_url} and will be verified.",
                      UserWarning)
    return get_id_from_url(_url)


def _check_for_bad_content_id(_content_id, _url):
    """This function confirms that a supplied Content ID is found within the provided URL.

    .. versionadded:: 2.4.0

    :param _content_id: The ID of the message
    :type _content_id: str, int, None
    :param _url: The full URL of the message
    :type _url: str
    :returns: The appropriate ID of the message where possible
    :raises: :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`
    """
    if _content_id is None or str(_content_id) not in _url:
        _content_id = _report_missing_id_and_retrieve(_content_id, _url)
    return _content_id


def _get_required_content_mention_data(_khoros_object, _content_info, _content_id, _title, _url):
    _missing_data_error = "A title and URL must be supplied to construct an user @mention"
    _content_info = {} if _content_info is None else _content_info
    _info_fields = ['title', 'url']
    _info_arguments = (_content_info, _content_id, _title, _url)
    _required_fields_in_dict = all(_field in _content_info for _field in _info_fields)
    _required_fields_in_args = all((_title, _url))
    if not _required_fields_in_dict and not _required_fields_in_args:
        raise errors.exceptions.MissingRequiredDataError(_missing_data_error)
    elif _required_fields_in_dict:
        _title = _content_info.get('title')
        _url = _content_info.get('url')
        _content_id = _content_info.get('id') if 'id' in _content_info else _content_id
    else:
        _content_id = _content_info.get('id') if not _content_id else _content_id
    _content_id = _check_for_bad_content_id(_content_id, _url)
    return _content_id, _title, _url


def format_content_mention(khoros_object=None, content_info=None, content_id=None, title=None, url=None):
    """This function formats the ``<li-message>`` HTML tag for a content @mention.

    .. versionadded:: 2.4.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object

                          .. note:: This argument is necessary if the URL (i.e. ``url`` argument) is not an absolute
                                    URL, as the base community URL will need to be retrieved from the object.

    :type khoros_object: class[khoros.Khoros], None
    :param content_info: A dictionary containing the ``'id'`` and/or ``'login'`` key(s) with the user information

                         .. note:: This argument is necessary if the Title and URL are not explicitly passed
                                   using the ``title`` and ``url`` function arguments.

    :type content_info: dict, None
    :param content_id: The Message ID (aka Content ID) associated with the content mention

                       .. note:: This is an optional argument as the ID can be retrieved from the URL.

    :type content_id: str, int, None
    :param title: The display title for the content mention (e.g. ``"Click Here"``)
    :type title: str, None
    :param url: The fully-qualified URL of the message being mentioned
    :type url: str, None
    :returns: The properly formatted ``<li-message>`` HTML tag in string format
    :raises: :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`,
             :py:exc:`khoros.errors.exceptions.InvalidURLError`
    """
    content_id, title, url = _get_required_content_mention_data(khoros_object, content_info, content_id, title, url)
    if url.startswith('/t5'):
        if not khoros_object:
            raise errors.exceptions.MissingRequiredDataError('The core Khoros object is required when a '
                                                             'fully-qualified URL is not provided.')
        url = f"{khoros_object.core['base_url']}{url}"
    mention_tag = f'<li-message title="{title}" uid="{content_id}" url="{url}"></li-message>'
    return mention_tag
