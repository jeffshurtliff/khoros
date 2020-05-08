# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.messages
:Synopsis:          This module includes functions that handle messages within a Khoros Community environment
:Usage:             ``from khoros.objects import messages``
:Example:           ``response = messages.create_message(khoros_obj, 'My First Message', 'Hello World',
                    node_id='support-tkb')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 May 2020
"""

from . import attachments
from .. import api, liql, errors
from ..structures import nodes

REQUIRED_FIELDS = ['board', 'subject']
CONTEXT_KEYS = ['id', 'url']
SEO_KEYS = ['title', 'description', 'canonical_url']


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
    outcome = api.query_successful(response)
    if return_id or return_url or return_api_url or return_http_code:
        return_values = {
            'return_id': parse_v2_response(response, message_id=True),
            'return_url': parse_v2_response(response, message_url=True),
            'return_api_url': parse_v2_response(response, message_api_uri=True),
            'return_http_code': parse_v2_response(response, http_code=True)
        }
        data_to_return = []
        return_booleans = {'return_id': return_id, 'return_url': return_url,
                           'return_http_code': return_http_code, 'return_api_url': return_api_url}
        for return_key, return_value in return_booleans.items():
            if return_value:
                data_to_return.append(return_values.get(return_key))
        outcome = tuple(data_to_return)
        if len(data_to_return) == 1:
            outcome = outcome[0]
    return response if full_response else outcome


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
    parsed_data = {}
    fields = {
        'status': (status, ('status',)),
        'response_msg': (response_msg, ('message',)),
        'http_code': (http_code, ('http_code',)),
        'message_id': (message_id, ('data', 'id')),
        'message_url': (message_url, ('data', 'view_href')),
        'message_api_uri': (message_api_uri, ('data', 'href'))
    }
    _confirm_field_supplied(fields)
    for field, info in fields.items():
        requested, json_path = info[0], info[1]
        if requested:
            if len(json_path) == 1:
                value = json_response[json_path[0]]
            else:
                value = json_response[json_path[0]][json_path[1]]
            parsed_data[field] = value
    if 'message_api_uri' in parsed_data and v2_base != '':
        parsed_data['message_api_uri'] = f"{v2_base}/{parsed_data.get('message_api_uri')}"
    if not return_dict:
        parsed_data = tuple(list(parsed_data.values()))
        if len(parsed_data) == 1:
            parsed_data = parsed_data[0]
    return parsed_data
