# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.messages
:Synopsis:          This module includes functions that handle messages within a Khoros Community environment
:Usage:             ``from khoros.objects import messages``
:Example:           ``response = messages.create_message(khoros_obj, 'My First Message', 'Hello World',
                    node_id='support-tkb')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Jan 2022
"""

import json
import warnings

from . import attachments, users
from . import tags as tags_module
from .. import api, liql, errors
from ..structures import nodes
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)

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
           tags=None, ignore_non_string_tags=False, teaser=None, topic=None, videos=None, attachment_file_paths=None,
           full_payload=None, full_response=False, return_id=False, return_url=False, return_api_url=False,
           return_http_code=False, return_status=None, return_error_messages=None, split_errors=False,
           proxy_user_object=None):
    """This function creates a new message within a given node.

    .. versionchanged:: 4.5.0
       The Content-Type header is now explicitly defined as ``application/json`` when handling non-multipart requests.

    .. versionchanged:: 4.4.0
       Introduced the ``proxy_user_object`` parameter to allow messages to be created on behalf of other users.

    .. versionchanged:: 4.3.0
       It is now possible to pass the pre-constructed full JSON payload into the function via the ``full_payload``
       parameter as an alternative to defining each field individually.

    .. versionchanged:: 2.8.0
       The ``ignore_non_string_tags``, ``return_status``, ``return_error_messages`` and ``split_errors``
       arguments were introduced.

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
    :param ignore_non_string_tags: Determines if non-strings (excluding iterables) should be ignored rather than
                                   converted to strings (``False`` by default)
    :type ignore_non_string_tags: bool
    :param teaser: The message teaser (used with blog articles)
    :type teaser: str, None
    :param topic: The root message of the conversation in which the message appears
    :type topic: dict, None
    :param videos: The query to retrieve videos uploaded to the message
    :type videos: dict, None
    :param attachment_file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type attachment_file_paths: str, tuple, list, set, None
    :param full_payload: Pre-constructed full JSON payload as a dictionary (*preferred*) or a JSON string with the
                         following syntax:

                            .. code-block:: json

                               {
                                 "data": {
                                   "type": "message",

                                 }
                               }

                         .. note:: The ``type`` field shown above is essential for the payload to be valid.

    :type full_payload: dict, str, None
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
    :param return_status: Determines if the **Status** of the API response should be returned by the function
    :type return_status: bool, None
    :param return_error_messages: Determines if the **Developer Response Message** (if any) associated with the
           API response should be returned by the function
    :type return_error_messages: bool, None
    :param split_errors: Defines whether or not error messages should be merged when applicable
    :type split_errors: bool
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to create the
                              message on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: Boolean value indicating a successful outcome (default) or the full API response
    :raises: :py:exc:`TypeError`, :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    api_url = f"{khoros_object.core['v2_base']}/messages"
    if full_payload:
        payload = validate_message_payload(full_payload)
    else:
        payload = construct_payload(subject, body, node, node_id, node_url, canonical_url, context_id, context_url,
                                    is_answer, is_draft, read_only, seo_title, seo_description, teaser, tags,
                                    cover_image, images, labels, product_category, products, topic, videos,
                                    ignore_non_string_tags=ignore_non_string_tags, khoros_object=khoros_object)
        payload = validate_message_payload(payload)
    multipart = True if attachment_file_paths else False
    if multipart:
        payload = attachments.construct_multipart_payload(payload, attachment_file_paths)
    content_type = 'application/json' if not multipart else None
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object, multipart=multipart,
                                             content_type=content_type, proxy_user_object=proxy_user_object)
    return api.deliver_v2_results(response, full_response, return_id, return_url, return_api_url, return_http_code,
                                  return_status, return_error_messages, split_errors, khoros_object)


def validate_message_payload(payload):
    """This function validates the payload for a message to ensure that it can be successfully utilized.

    .. versionadded:: 4.3.0

    :param payload: The message payload to be validated as a dictionary (*preferred*) or a JSON string.
    :type payload: dict, str
    :returns: The payload as a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.InvalidMessagePayloadError`
    """
    if not payload and not isinstance(payload, dict) and not isinstance(payload, str):
        raise errors.exceptions.InvalidMessagePayloadError("The message payload is null.")
    if isinstance(payload, str):
        logger.warning("The message payload is defined as a JSON string and will be converted to a dictionary.")
        payload = json.loads(payload)
    if not isinstance(payload, dict):
        raise errors.exceptions.InvalidMessagePayloadError("The message payload must be a dictionary or "
                                                           "JSON string.")
    if 'data' not in payload:
        raise errors.exceptions.InvalidMessagePayloadError("The message payload must include the 'data' key.")
    if 'type' not in payload.get('data'):
        raise errors.exceptions.InvalidMessagePayloadError("The message payload must include the `type` key (with "
                                                           "'message' as the value) within the 'data' parent key.")
    if payload.get('data').get('type') != 'message':
        raise errors.exceptions.InvalidMessagePayloadError("The value for the 'type' key in the message payload "
                                                           "must be defined  as 'message' but was defined as "
                                                           f"'{payload.get('data').get('type')}' instead.")
    if 'subject' not in payload.get('data' or 'board' not in payload.get('data') or
                                    'id' not in payload.get('data').get('board')):
        raise errors.exceptions.InvalidMessagePayloadError("A node and subject must be defined.")
    return payload


def construct_payload(subject=None, body=None, node=None, node_id=None, node_url=None, canonical_url=None,
                      context_id=None, context_url=None, is_answer=None, is_draft=None, read_only=None, seo_title=None,
                      seo_description=None, teaser=None, tags=None, cover_image=None, images=None, labels=None,
                      product_category=None, products=None, topic=None, videos=None, parent=None, status=None,
                      moderation_status=None, attachments_to_add=None, attachments_to_remove=None, overwrite_tags=False,
                      ignore_non_string_tags=False, msg_id=None, khoros_object=None, action='create'):
    """This function constructs and properly formats the JSON payload for a messages API request.

    .. todo::
       Add support for the following parameters which are currently present but unsupported: ``cover_image``,
       ``images``, ``labels``, ``product_category``, ``products``, ``topic``, ``videos``, ``parent``, ``status``,
       ``attachments_to_add`` and ``attachments to remove``

    .. versionchanged:: 2.8.0
       Added the ``parent``, ``status``, ``moderation_status``, ``attachments_to_add``, ``attachments_to_remove``,
       ``overwrite_tags``, ``ignore_non_string_tags``, ``msg_id``, ``khoros_object`` and ``action`` arguments, and
       added the ``raises`` section to the docstring.

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
    :param parent: The parent of the message
    :type parent: str, None
    :param status: The message status for messages where conversation.style is ``idea`` or ``contest``

                   .. caution:: This property is not returned if the message has the default ``Unspecified`` status
                                assigned. It will only be returned for ideas with a status of ``Completed`` or with a
                                custom status created in Community Admin.

    :type status: dict, None
    :param moderation_status: The moderation status of the message

                              .. note:: Acceptable values are ``unmoderated``, ``approved``, ``rejected``,
                                        ``marked_undecided``, ``marked_approved`` and ``marked_rejected``.

    :type moderation_status: str, None

    :param attachments_to_add: The full path(s) to one or more attachments (e.g. ``path/to/file1.pdf``) to be
                               added to the message
    :type attachments_to_add: str, tuple, list, set, None
    :param attachments_to_remove: One or more attachments to remove from the message

                                  .. note:: Each attachment should specify the attachment id of the attachment to
                                            remove, which begins with ``m#_``. (e.g. ``m283_file1.pdf``)

    :type attachments_to_remove: str, tuple, list, set, None
    :param overwrite_tags: Determines if tags should overwrite any existing tags (where applicable) or if the tags
                           should be appended to the existing tags (default)
    :type overwrite_tags: bool
    :param ignore_non_string_tags: Determines if non-strings (excluding iterables) should be ignored rather than
                                   converted to strings (``False`` by default)
    :type ignore_non_string_tags: bool
    :param msg_id: Message ID of an existing message so that its existing tags can be retrieved (optional)
    :type msg_id: str, int, None
    :param khoros_object: The core :py:class:`khoros.Khoros` object

                          .. note:: The core object is only necessary when providing a Message ID as it will be
                                     needed to retrieve the existing tags from the message.

    :type khoros_object: class[khoros.Khoros], None
    :param action: Defines if the payload will be used to ``create`` (default) or ``update`` a message
    :type action: str
    :returns: The properly formatted JSON payload
    :raises: :py:exc:`TypeError`, :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    # Define the default payload structure
    payload = {
        "data": {
            "type": "message"
        }
    }

    # Ensure the required fields are defined if creating a message
    if action == 'create':
        _verify_required_fields(node, node_id, node_url, subject)

    # Define the destination
    if action == 'create' or any((node, node_id, node_url)):
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
            elif field_value[1] == bool:
                bool_value = bool(field_value[0]) if isinstance(field_value[0], str) else field_value[0]
                payload['data'][field_name] = bool_value

    # Add moderation status to payload when applicable
    payload = _add_moderation_status_to_payload(payload, moderation_status)

    # Add tags to payload when applicable
    if tags:
        payload = _add_tags_to_payload(payload, tags, _khoros_object=khoros_object, _msg_id=msg_id,
                                       _overwrite_tags=overwrite_tags, _ignore_non_strings=ignore_non_string_tags)

    # TODO: Add functionality for remaining non-string and non-Boolean arguments

    return payload


def update(khoros_object, msg_id=None, msg_url=None, subject=None, body=None, node=None, node_id=None, node_url=None,
           canonical_url=None, context_id=None, context_url=None, cover_image=None, is_draft=None, labels=None,
           moderation_status=None, parent=None, product_category=None, products=None, read_only=None, topic=None,
           status=None, seo_title=None, seo_description=None, tags=None, overwrite_tags=False,
           ignore_non_string_tags=False, teaser=None, attachments_to_add=None, attachments_to_remove=None,
           full_response=None, return_id=None, return_url=None, return_api_url=None, return_http_code=None,
           return_status=None, return_error_messages=None, split_errors=False, proxy_user_object=None):
    """This function updates one or more elements of an existing message.

    .. versionchanged:: 4.4.0
       Introduced the ``proxy_user_object`` parameter to allow messages to be updated on behalf of other users.

    .. versionadded:: 2.8.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param msg_id: The ID of the existing message
    :type msg_id: str, int, None
    :param msg_url: The URL of the existing message
    :type msg_url: str, None
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
    :param is_draft: Indicates whether or not the message is still a draft (i.e. unpublished)
    :type is_draft: bool, None
    :param labels: The query to retrieve labels applied to the message
    :type labels: dict, None
    :param moderation_status: The moderation status of the message

                              .. note:: Acceptable values are ``unmoderated``, ``approved``, ``rejected``,
                                        ``marked_undecided``, ``marked_approved`` and ``marked_rejected``.

    :type moderation_status: str, None
    :param parent: The parent of the message
    :type parent: str, None
    :param product_category: The product category (i.e. container for ``products``) associated with the message
    :type product_category: dict, None
    :param products: The product in a product catalog associated with the message
    :type products: dict, None
    :param read_only: Indicates whether or not the message should be read-only or have replies/comments blocked
    :type read_only: bool, None
    :param topic: The root message of the conversation in which the message appears
    :type topic: dict, None
    :param status: The message status for messages where conversation.style is ``idea`` or ``contest``

                   .. caution:: This property is not returned if the message has the default ``Unspecified`` status
                                assigned. It will only be returned for ideas with a status of Completed or with a
                                custom status created in Community Admin.

    :type status: dict, None
    :param seo_title: The title of the message used for SEO purposes
    :type seo_title: str, None
    :param seo_description: A description of the message used for SEO purposes
    :type seo_description: str, None
    :param tags: The query to retrieve tags applied to the message
    :type tags: dict, None
    :param overwrite_tags: Determines if tags should overwrite any existing tags (where applicable) or if the tags
                           should be appended to the existing tags (default)
    :type overwrite_tags: bool
    :param ignore_non_string_tags: Determines if non-strings (excluding iterables) should be ignored rather than
                                   converted to strings (``False`` by default)
    :type ignore_non_string_tags: bool
    :param teaser: The message teaser (used with blog articles)
    :type teaser: str, None
    :param attachments_to_add: The full path(s) to one or more attachments (e.g. ``path/to/file1.pdf``) to be
                               added to the message
    :type attachments_to_add: str, tuple, list, set, None
    :param attachments_to_remove: One or more attachments to remove from the message

                                  .. note:: Each attachment should specify the attachment id of the attachment to
                                            remove, which begins with ``m#_``. (e.g. ``m283_file1.pdf``)

    :type attachments_to_remove: str, tuple, list, set, None
    :param full_response: Defines if the full response should be returned instead of the outcome (``False`` by default)

                          .. caution:: This argument overwrites the ``return_id``, ``return_url``, ``return_api_url``
                                       and ``return_http_code`` arguments.

    :type full_response: bool, None
    :param return_id: Indicates that the **Message ID** should be returned (``False`` by default)
    :type return_id: bool, None
    :param return_url: Indicates that the **Message URL** should be returned (``False`` by default)
    :type return_url: bool, None
    :param return_api_url: Indicates that the **API URL** of the message should be returned (``False`` by default)
    :type return_api_url: bool, None
    :param return_http_code: Indicates that the **HTTP status code** of the response should be returned
                             (``False`` by default)
    :type return_http_code: bool, None
    :param return_status: Determines if the **Status** of the API response should be returned by the function
    :type return_status: bool, None
    :param return_error_messages: Determines if the **Developer Response Message** (if any) associated with the
           API response should be returned by the function
    :type return_error_messages: bool, None
    :param split_errors: Defines whether or not error messages should be merged when applicable
    :type split_errors: bool
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to update the
                              message on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: Boolean value indicating a successful outcome (default) or the full API response
    :raises: :py:exc:`TypeError`, :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    msg_id = _verify_message_id(msg_id, msg_url)
    api_url = f"{khoros_object.core['v2_base']}/messages/{msg_id}"
    payload = construct_payload(subject, body, node, node_id, node_url, canonical_url, context_id, context_url,
                                is_draft=is_draft, read_only=read_only, seo_title=seo_title, tags=tags, topic=topic,
                                seo_description=seo_description, teaser=teaser, cover_image=cover_image, labels=labels,
                                parent=parent, products=products, product_category=product_category, status=status,
                                moderation_status=moderation_status, attachments_to_add=attachments_to_add,
                                attachments_to_remove=attachments_to_remove, overwrite_tags=overwrite_tags,
                                ignore_non_string_tags=ignore_non_string_tags,  action='update')
    multipart = True if attachments_to_add else False
    if multipart:
        payload = attachments.construct_multipart_payload(payload, attachments_to_add, 'update')
    response = api.put_request_with_retries(api_url, payload, khoros_object=khoros_object, multipart=multipart,
                                            proxy_user_object=proxy_user_object)
    return api.deliver_v2_results(response, full_response, return_id, return_url, return_api_url, return_http_code,
                                  return_status, return_error_messages, split_errors, khoros_object)


def get_metadata(khoros_object, msg_id, metadata_key):
    """This function retrieves the value for a specific metadata key associated with a given message.

    .. versionadded:: 4.5.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param msg_id: The ID of the message for which the metadata will be retrieved
    :type msg_id: str, int
    :param metadata_key: The metadata key for which the value will be retrieved
    :type metadata_key: str
    :returns: The metadata value
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError',
             :py:exc:`khoros.errors.exceptions.InvalidMetadataError`,
             :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    if not msg_id or not metadata_key:
        raise errors.exceptions.MissingRequiredDataError('A message ID and a metadata key are required')
    uri = f'/messages/id/{msg_id}/metadata/key/{metadata_key}'
    response = khoros_object.v1.get(uri)
    if not response.get('response'):
        raise errors.exceptions.GETRequestError('The GET request to retrieve the message metadata was not successful')
    if response['response'].get('status') == 'error':
        if response['response']['error'].get('message'):
            raise errors.exceptions.InvalidMetadataError(response['response']['error'].get('message'))
        else:
            raise errors.exceptions.InvalidMetadataError()
    metadata_value = response['response']['value'].get('$')
    return metadata_value


def _verify_message_id(_msg_id, _msg_url):
    """This function verifies that a message ID has been defined or can be using the message URL.

    .. versionadded:: 2.8.0

    :param _msg_id: The message ID associated with a message
    :type _msg_id: str, int, None
    :param _msg_url: The URL associated with a message
    :type _msg_url: str, None
    :returns: The message ID
    :raises: :py:exc:`errors.exceptions.MissingRequiredDataError`,
             :py:exc:`errors.exceptions.MessageTypeNotFoundError`
    """
    if not any((_msg_id, _msg_url)):
        raise errors.exceptions.MissingRequiredDataError('A message ID or URL must be defined when updating messages')
    elif not _msg_id:
        _msg_id = get_id_from_url(_msg_url)
    return _msg_id


def _verify_required_fields(_node, _node_id, _node_url, _subject):
    """This function verifies that the required fields to create a message are satisfied.

    .. versionchanged:: 2.8.0
       Updated the if statement to leverage the :py:func:`isinstance` function.

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
    if (not _node and not _node_id and not _node_url) or (_node is not None and not isinstance(_node, dict)) \
            or not _subject:
        _requirements_satisfied = False
    elif _node and (not _node_id and not _node_url):
        _requirements_satisfied = False if 'id' not in _node else True
    if not _requirements_satisfied:
        raise errors.exceptions.MissingRequiredDataError("A node and subject must be defined when creating messages")
    return


def _add_moderation_status_to_payload(_payload, _moderation_status):
    """This function adds the moderation status field and value to the payload when applicable.

    .. versionadded:: 2.8.0

    :param _payload: The payload for the API call
    :type _payload: dict
    :param _moderation_status: The ``moderation_status`` field value
    :type _moderation_status: str, None
    :returns: The payload with the potentially added ``moderation_status`` key value pair
    """
    _valid_options = ['unmoderated', 'approved', 'rejected', 'marked_undecided', 'marked_approved', 'marked_rejected']
    if _moderation_status:
        if not isinstance(_moderation_status, str) or _moderation_status not in _valid_options:
            warnings.warn(f"The moderation status '{_moderation_status}' is not a valid option and will be ignored.",
                          RuntimeWarning)
        else:
            _payload['data']['moderation_status'] = _moderation_status
    return _payload


def _add_tags_to_payload(_payload, _tags, _khoros_object=None, _msg_id=None, _overwrite_tags=False,
                         _ignore_non_strings=False):
    """This function adds tags to the payload for an API call against the *messages* collection.

    :param _payload: The payload for the API call
    :type _payload: dict
    :param _tags: A list, tuple, set or string containing one or more tags to add to the message
    :type _tags: list, tuple, set, str
    :param _khoros_object: The core :py:class:`khoros.Khoros` object

                           .. note:: The core object is only necessary when providing a Message ID as it will be
                                     needed to retrieve the existing tags from the message.

    :type _khoros_object: class[khoros.Khoros], None
    :param _msg_id: Message ID of an existing message so that its existing tags can be retrieved (optional)
    :type _msg_id: str, int, None
    :param _overwrite_tags: Determines if tags should overwrite any existing tags (where applicable) or if the tags
                      should be appended to the existing tags (default)
    :type _overwrite_tags: bool
    :param _ignore_non_strings: Determines if non-strings (excluding iterables) should be ignored rather than
                               converted to strings (``False`` by default)
    :type _ignore_non_strings: bool
    :returns: The payload with tgs included when relevant
    """
    _formatted_tags = tags_module.structure_tags_for_message(_tags, khoros_object=_khoros_object, msg_id=_msg_id,
                                                             overwrite=_overwrite_tags,
                                                             ignore_non_strings=_ignore_non_strings)
    _payload['data']['tags'] = _formatted_tags
    return _payload


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


def is_read_only(khoros_object=None, msg_id=None, msg_url=None, api_response=None):
    """This function checks to see whether or not a message is read-only.

    .. versionadded:: 2.8.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None
    :param msg_id: The unique identifier for the message
    :type msg_id: str, int, None
    :param msg_url: THe URL of the message
    :type msg_url: str, None
    :param api_response: The JSON data from an API response
    :type api_response: dict, None
    :returns: Boolean value indicating whether or not the message is read-only
    :raises: :py:exc:`errors.exceptions.MissingRequiredDataError`,
             :py:exc:`errors.exceptions.MessageTypeNotFoundError`
    """
    if api_response:
        current_status = api_response['data']['read_only']
    else:
        errors.handlers.verify_core_object_present(khoros_object)
        msg_id = _verify_message_id(msg_id, msg_url)
        query = f'SELECT read_only FROM messages WHERE id = "{msg_id}"'     # nosec
        api_response = liql.perform_query(khoros_object, liql_query=query, verify_success=True)
        current_status = api_response['data']['items'][0]['read_only']
    return current_status


def set_read_only(khoros_object, enable=True, msg_id=None, msg_url=None, suppress_warnings=False):
    """This function sets (i.e. enables or disables) the read-only flag for a given message.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param enable: Determines if the read-only flag should be enabled (``True`` by default)
    :type enable: bool
    :param msg_id: The unique identifier for the message
    :type msg_id: str, int, None
    :param msg_url: The URL for the message
    :type msg_url: str, None
    :param suppress_warnings: Determines whether or not warning messages should be suppressed (``False`` by default)
    :type suppress_warnings: bool
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    def _get_warn_msg(_msg_id, _status):
        """This function returns the appropriate warning message to use when applicable."""
        return f"Read-only status is already {_status} for Message ID {_msg_id}"

    msg_id = _verify_message_id(msg_id, msg_url)
    current_status = is_read_only(khoros_object, msg_id)
    warn_msg = None
    if all((enable, current_status)):
        warn_msg = _get_warn_msg(msg_id, 'enabled')
    elif enable is False and current_status is False:
        warn_msg = _get_warn_msg(msg_id, 'disabled')
    if warn_msg and not suppress_warnings:
        errors.handlers.eprint(warn_msg)
    else:
        result = update(khoros_object, msg_id, msg_url, read_only=enable, full_response=True)
        if result['status'] == 'error':
            errors.handlers.eprint(errors.handlers.get_error_from_json(result))
        else:
            new_status = is_read_only(api_response=result)
            if new_status == current_status and not suppress_warnings:
                warn_msg = f"The API call was successful but the read-only status for Message ID {msg_id} is " \
                           f"still {new_status}."
                errors.handlers.eprint(warn_msg)
    return


def _get_required_user_mention_data(_khoros_object, _user_info, _user_id, _login):
    """This function retrieves the required data for constructing a user mention.

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _user_info: User information provided in a dictionary
    :type _user_info: dict, None
    :param _user_id: The User ID for the user
    :type _user_id: str, int, None
    :param _login: The username (i.e. login) for the user
    :type _login: str, None
    :returns: The User ID and username (i.e. login) for the user
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
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
    """This function retrieves the required data to construct a content mention.

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _content_info: Information on the content within a dictionary
    :type _content_info: dict, None
    :param _content_id: The ID of the content
    :type _content_id: str, int, None
    :param _title: The title of the content
    :type _title: str, None
    :param _url: The URL of the content
    :type _url: str, None
    :returns: The ID, title and URL of the content
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
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
