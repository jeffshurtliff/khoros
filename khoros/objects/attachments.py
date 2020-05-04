# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.attachments
:Synopsis:          This module includes functions that handle attachments for messages
:Usage:             ``from khoros.objects import attachments``
:Example:           ``payload = format_attachment_payload(titles, file_paths)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 May 2020
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
    :returns: The full payload for the multipart API call as a list of tuples

              .. note:: See the `Requests Documentation <https://rsa.im/2SvMsya>`_ for added context on the return data.

    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    file_paths = core_utils.convert_string_to_tuple(file_paths)
    attachments_json = format_attachment_payload(file_paths)
    message_json['attachments'] = attachments_json
    files_payload = get_file_upload_info(file_paths)
    message_json = {'api.request': message_json}
    print(f"MESSAGE JSON:\n{message_json}\n\nFILES PAYLOAD:\n{files_payload}")
    return message_json, files_payload


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
    print(f"FILE PATHS:\n{file_paths}")     # TODO: Remove print debugging
    if len(file_paths) == 1:
        files = _format_single_file(file_paths[0])
    else:
        files = _format_multiple_files(file_paths)
    return files


def _format_single_file(_file_path):
    """This function formats a single file for use in an API call.

    :param _file_path: The individual file path
    :type _file_path: str
    :returns: Dictionary with the properly formatted API payload
    :raises: :py:exc:`FileNotFoundError`
    """
    _files = {
        'file': {'attachment1', open(_file_path, 'rb')}
    }
    return _files


def _format_multiple_files(_file_paths):
    """THis function formats multiple files for use in an API call.

    :param _file_paths: The list of file paths
    :type _file_paths: list, tuple, set
    :returns: List of 2-tuples that have been properly formatted as API payload
    :raises: :py:exc:`FileNotFoundError`
    """
    file_paths = core_utils.convert_string_to_tuple(_file_paths)
    _files, _count = [], 1
    for _path in _file_paths:
        _files.append(('file', (f'attachment{_count}', open(_path, 'rb'))))
        _count += 1
    return _files
