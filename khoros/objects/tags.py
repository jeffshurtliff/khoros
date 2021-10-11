# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.tags
:Synopsis:          This module includes functions that handle tags within a Khoros Community environment
:Usage:             ``from khoros.objects import tags``
:Example:           ``tags.add_single_tag_to_message('tutorial', 123)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Jun 2021
"""

from .. import api, liql, errors
from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)

ITERABLE_TYPES = (list, tuple, set)


def structure_single_tag_payload(tag_text):
    """This function structures the payload for a single tag.

    .. versionadded:: 2.8.0

    :param tag_text: The tag to be included in the payload
    :type tag_text: str
    :returns: The payload as a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError`
    """
    if not isinstance(tag_text, str):
        raise errors.exceptions.InvalidPayloadValueError("The tag text must be in string format")
    payload = {
        "data": {
            "type": "tag",
            "text": tag_text
        }
    }
    return payload


def add_single_tag_to_message(khoros_object, tag, msg_id, allow_exceptions=False):
    """This function adds a single tag to an existing message.

    .. versionadded:: 2.8.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param tag: The tag value to be added
    :type tag: str
    :param msg_id: The unique identifier for the message
    :type msg_id: str, int
    :param allow_exceptions: Determines if exceptions are permitted to be raised (``False`` by default)
    :type allow_exceptions: bool
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    payload = structure_single_tag_payload(tag)
    api_url = f"{khoros_object.core['v2_base']}/messages/{msg_id}/tags"
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object)
    if response['status'] != 'success':
        api_error = errors.handlers.get_error_from_json(response)
        if allow_exceptions:
            raise errors.exceptions.POSTRequestError(api_error)
        else:
            errors.handlers.eprint(api_error)
    return


def get_tags_for_message(khoros_object, msg_id):
    """This function retrieves the tags for a given message.

    .. versionadded:: 2.8.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param msg_id: The Message ID for the message from which to retrieve tags
    :type msg_id: str, int
    :returns: A list of tags associated with the message
    """
    tag_list = []
    query = f"SELECT text FROM tags WHERE messages.id = '{msg_id}'"     # nosec
    response = liql.perform_query(khoros_object, liql_query=query, verify_success=True)
    entries = api.get_items_list(response)
    for entry in entries:
        tag_list.append(entry['text'])
    return tag_list


def structure_tags_for_message(*tags, khoros_object=None, msg_id=None, overwrite=False, ignore_non_strings=False,
                               wrap_json=False):
    """This function structures tags to use within the payload for creating or updating a message.

    .. versionchanged:: 4.3.0
       Introduced the ``wrap_json`` parameter to wrap the tags in a dictionary within the ``items`` key.

    .. versionchanged:: 4.1.0
       The missing type declaration for the ``overwrite`` parameter has been added to the docstring.

    .. versionadded:: 2.8.0

    :param tags: One or more tags or list of tags to be structured
    :type tags: str, list, tuple, set
    :param khoros_object: The core :py:class:`khoros.Khoros` object

                          .. note:: The core object is only necessary when providing a Message ID as it will be
                                    needed to retrieve the existing tags from the message.

    :type khoros_object: class[khoros.Khoros], None
    :param msg_id: Message ID of an existing message so that its existing tags can be retrieved (optional)
    :type msg_id: str, int, None
    :param overwrite: Determines if tags should overwrite any existing tags (where applicable) or if the tags
                      should be appended to the existing tags (default)
    :type overwrite: bool
    :param ignore_non_strings: Determines if non-strings (excluding iterables) should be ignored rather than
                               converted to strings (``False`` by default)
    :type ignore_non_strings: bool
    :param wrap_json: Determines if the list of tags should be wrapped in the ``{"items": []}`` JSON structure
                      -- In other words, a dictionary rather than a list (``False`` by default)
    :type wrap_json: bool
    :returns: A list of properly formatted tags to act as the value for the ``tags`` field in the message payload
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    formatted_list, existing_tags = [], []
    if msg_id and not any((overwrite, khoros_object)):
        raise errors.exceptions.MissingRequiredDataError('The core Khoros object must be provided when supplying '
                                                         'a Message ID')
    elif msg_id and not overwrite:
        errors.handlers.verify_core_object_present(khoros_object)
        existing_tags = get_tags_for_message(khoros_object, msg_id)
    formatted_list = _format_tag_data(tags, ignore_non_strings)
    existing_tags = _format_tag_data(existing_tags, ignore_non_strings)
    complete_tags = core_utils.merge_and_dedup(formatted_list, existing_tags)
    complete_tags = {'items': complete_tags} if wrap_json else complete_tags
    return complete_tags


def _format_tag_data(_collection, _ignore_non_strings):
    """This function is used by :py:func:`khoros.objects.tags.structure_tags_for_message` to format the tag data.

    .. versionadded:: 2.8.0
    """
    _formatted_list = []
    _collection = _get_low_level_tags(_collection)
    for _tag_or_list in _collection:
        if not isinstance(_tag_or_list, str) and _ignore_non_strings:
            continue
        else:
            _tag_or_list = (str(_tag_or_list),)
        for _tag in _tag_or_list:
            _tag = {
                "type": "tag",
                "text": _tag
            }
            _formatted_list.append(_tag)
    return _formatted_list


def _get_low_level_tags(_collection):
    """This function expands a multi-level iterable to get the low-level tags.

    :param _collection: Iterable with one or more levels or a single tag
    :type _collection: list, tuple, set, str, int, float
    :returns: A list of all low-level tags (pre-formatted)
    """
    _low_level_tags, _iterables = [], []
    for _item in _collection:
        if type(_item) not in ITERABLE_TYPES:
            _low_level_tags.append(_item)
        else:
            _iterables.append(_item)
    while len(_iterables) > 0:
        _item = _iterables.pop()
        for _sub_item in _item:
            if type(_sub_item) not in ITERABLE_TYPES:
                _low_level_tags.append(_sub_item)
            else:
                _iterables.append(_sub_item)
    return _low_level_tags


def add_tags_to_message(khoros_object, tags, msg_id, allow_exceptions=False):
    """This function adds one or more tags to an existing message.

    .. versionadded:: 2.8.0

    ..caution:: This function is not the most effective way to add multiple tags to a message. It is recommended
                that the :py:func:`khoros.objects.messages.update` function be used instead with its ``tags``
                argument, which is more efficient and performance-conscious.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param tags: One or more tags to be added to the message
    :type tags: str, tuple, list, set
    :param msg_id: The unique identifier for the message
    :type msg_id: str, int
    :param allow_exceptions: Determines if exceptions are permitted to be raised (``False`` by default)
    :type allow_exceptions: bool
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    tags = (tags, ) if isinstance(tags, str) else tags
    for tag in tags:
        add_single_tag_to_message(khoros_object, str(tag), msg_id, allow_exceptions)
    return
