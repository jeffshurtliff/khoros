# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.attachments
:Synopsis:          This module includes functions that handle attachments for messages
:Usage:             ``from khoros.objects import attachments``
:Example:           ``payload = format_attachment_payload(titles, file_paths)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 May 2020
"""

import os
import json

from .. import errors
from ..utils import core_utils


def construct_multipart_payload(message_json, file_paths):
    """This function constructs the full multipart payload for a message with one or more attachment.

    .. versionadded:: 2.3.0

    :param message_json: The message information in JSON format
    :type message_json: dict
    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :returns: The full payload for the multipart API call as a dictionary

              .. note:: See the `Requests Documentation <https://rsa.im/2SvMsya>`_ for added context on the return data.

    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    message_json['data']['attachments'] = format_attachment_payload(file_paths)
    files_payload = get_file_upload_info(file_paths)
    full_payload = {'api.request': (None, json.dumps(message_json, default=str), 'application/json')}
    full_payload.update(files_payload)
    return full_payload


def format_attachment_payload(file_paths):
    """This function formats the JSON payload for attachments to be used in an API call.

    .. versionadded:: 2.3.0

    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :returns: The list of items (in list format) that represent the ``items`` API value
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    payload = {
        "list_item_type": "attachment"
    }
    list_items = get_list_items(file_paths)
    payload["items"] = list_items
    return payload


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


def get_file_upload_info(file_paths):
    """This function constructs the binary file(s) portion of the multipart API call.

    .. versionadded:: 2.3.0

    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :returns: A dictionary with the file upload information for the API call
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    files, count = {}, 1
    for path in file_paths:
        # TODO: Dynamically define the MIME type
        files[f'attachment{count}'] = (f'{os.path.basename(path)}', open(path, 'rb'))
        count += 1
    return files
