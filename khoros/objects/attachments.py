# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.attachments
:Synopsis:          This module includes functions that handle attachments for messages
:Usage:             ``from khoros.objects import attachments``
:Example:           ``payload = format_attachment_payload(titles, file_paths)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

import os
import json

from .. import errors
from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def construct_multipart_payload(message_json, file_paths, action='create'):
    """This function constructs the full multipart payload for a message with one or more attachment.

    .. versionchanged:: 2.8.0
       Support was added for updating existing messages.

    .. versionadded:: 2.3.0

    :param message_json: The message information in JSON format
    :type message_json: dict
    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :param action: Indicates if the payload will be used to ``create`` (default) or ``update`` a message
    :type action: str
    :returns: The full payload for the multipart API call as a dictionary

              .. note:: See the `Requests Documentation <https://rsa.im/2SvMsya>`_ for added context on the return data.

    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    files_payload = get_file_upload_info(file_paths, action)
    if action == 'update':
        message_json['data'].update(format_attachment_payload(file_paths, 'update'))
        full_payload = _format_full_payload('data', message_json['data'], files_payload)
    else:
        message_json['data']['attachments'] = format_attachment_payload(file_paths)
        full_payload = _format_full_payload('api.request', message_json, files_payload)
    return full_payload


def _format_full_payload(_json_field_name, _json_payload, _files_payload):
    """This function formats the full payload for a ``multipart/form-data`` API request including attachments.

    .. versionadded:: 2.8.0

    :param _json_field_name: The name of the highest-level JSON field used in the JSON payload
    :type _json_field_name: str
    :param _json_payload: The JSON payload data as a dictionary
    :type _json_payload: dict
    :param _files_payload: The payload for the attachments containing the IO stream for the file(s)
    :type _files_payload: dict
    :returns: The full payload as a dictionary
    :raises: :py:exc:`TypeError`
    """
    _full_payload = {
        _json_field_name: (None, json.dumps(_json_payload, default=str), 'application/json')
    }
    _full_payload.update(_files_payload)
    return _full_payload


def format_attachment_payload(file_paths, action='create'):
    """This function formats the JSON payload for attachments to be used in an API call.

    .. versionchanged:: 2.8.0
       Support was added for updating existing messages.

    .. versionadded:: 2.3.0

    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :param action: Indicates if the payload will be used to ``create`` (default) or ``update`` a message
    :type action: str
    :returns: The list of items (in list format) that represent the ``items`` API value
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    if action == 'update':
        payload = _structure_attachments_to_add(len(file_paths))
    else:
        payload = {
            "list_item_type": "attachment"
        }
        list_items = get_list_items(file_paths)
        payload["items"] = list_items
    return payload


def _structure_attachments_to_add(_attachment_count):
    """This function formats the JSON for the ``attachments_to_add`` field when updating existing messages.

    .. versionadded:: 2.8.0

    :param _attachment_count: The number of attachments being added
    :type _attachment_count: int
    :returns: The properly formatted JSON data as a dictionary
    :raises: :py:exc:`TypeError`
    """
    _attachments = []
    if _attachment_count > 0:
        for _count in range(1, (_attachment_count + 1)):
            _attachment = {
                "type": "attachment",
                "field": f"attachment{_count}"
            }
            _attachments.append(_attachment)
    return {"attachments_to_add": _attachments}


def get_list_items(file_paths):
    """This function constructs the ``items`` field for the ``attachments`` API call.

    .. versionadded:: 2.3.0

    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :returns: The list of items (in list format) that represent the ``items`` API value
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    list_items, count = [], 1
    for path in file_paths:
        item = {
            "type": "attachment",
            "field": f"attachment{count}",
            "filename": f"{os.path.basename(path)}"
        }
        list_items.append(item)
        count += 1
    return list_items


def get_file_upload_info(file_paths, action='create'):
    """This function constructs the binary file(s) portion of the multipart API call.

    .. versionchanged:: 2.8.0
       Support was added for updating an existing message.

    .. versionadded:: 2.3.0

    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :param action: Indicates if the payload will be used to ``create`` (default) or ``update`` a message
    :type action: str
    :returns: A dictionary with the file upload information for the API call
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    files, count = {}, 1
    for path in file_paths:
        # TODO: Dynamically define the MIME type
        if action == 'update':
            files[f'attachment{count}'] = open(path, 'rb')
        else:
            files[f'attachment{count}'] = (f'{os.path.basename(path)}', open(path, 'rb'))
        count += 1
    return files
