# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.tags
:Synopsis:          This module includes functions that handle tags within a Khoros Community environment
:Usage:             ``from khoros.objects import tags``
:Example:           ``tags.add_single_tag_to_message('tutorial', 123)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     29 Jun 2020
"""

from .. import api, errors


def structure_single_tag_payload(tag_text):
    """This function structures the payload for a single tag.

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


def add_tags_to_message(khoros_object, tags, msg_id, allow_exceptions=False):
    """This function adds one or more tags to an existing message.

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
    # TODO: Refactor this to work as directed by AdamN in Khoros Atlas
    tags = (tags, ) if isinstance(tags, str) else tags
    for tag in tags:
        add_single_tag_to_message(khoros_object, str(tag), msg_id, allow_exceptions)
    return
