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


def construct_multipart_payload(message_json, attachment_titles=None, file_paths=None, attachments=None):
    """This function constructs the full multipart payload for a message with one or more attachment.

    .. versionadded:: 2.3.0

    :param message_json: The message information in JSON format
    :type message_json: dict
    :param attachment_titles: One or more attachment titles (e.g. ``User Guide``, ``Config File``, etc.)
    :type attachment_titles: str, tuple, list, set
    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :param attachments: A consolidated dictionary mapping attachment titles to file paths
    :type attachments: dict
    :returns: The full payload for the multipart API call as a list of tuples

              .. note:: See the `Requests Documentation <https://rsa.im/2SvMsya>`_ for added context on the return data.

    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    attachments_json = format_attachment_payload(attachment_titles, file_paths, attachments)
    message_json['attachments'] = attachments_json
    files_payload = get_file_upload_info(attachment_titles, file_paths, attachments)
    # multipart_payload = [
    #     ('json', ('api.request', json.dumps(message_json), 'application/json')),
    # ]
    # for file_entry in files_payload:
    #     multipart_payload.append(file_entry)
    # print(f"Multipart Payload Getting Returned:\n{multipart_payload}")  # TODO: Remove print debugging
    # return multipart_payload
    message_json = {'api.request': message_json}
    print(f"MESSAGE JSON:\n{message_json}\n\nFILES PAYLOAD:\n{files_payload}")
    return message_json, files_payload


def format_attachment_payload(attachment_titles=None, file_paths=None, attachments=None):
    """This function formats the JSON payload for attachments to be used in an API call.

    .. versionadded:: 2.3.0

    :param attachment_titles: One or more attachment titles (e.g. ``User Guide``, ``Config File``, etc.)
    :type attachment_titles: str, tuple, list, set
    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :param attachments: A consolidated dictionary mapping attachment titles to file paths
    :type attachments: dict
    :returns: The list of items (in list format) that represent the ``items`` API value
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    if not attachment_titles and not file_paths and not attachment_titles:
        raise errors.exceptions.MissingRequiredDataError("Missing required attachment data")
    if not attachments:
        attachments = _consolidate_attachment_data(attachment_titles, file_paths)
    payload = {
        "list_item_type": "attachment"
    }
    list_items = get_list_items(attachments=attachments)
    payload["items"] = list_items
    return payload


def get_list_items(attachment_titles=None, file_paths=None, attachments=None):
    """This function constructs the ``items`` field for the ``attachments`` API call.

    .. versionadded:: 2.3.0

    :param attachment_titles: One or more attachment titles (e.g. ``User Guide``, ``Config File``, etc.)
    :type attachment_titles: str, tuple, list, set
    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :param attachments: A consolidated dictionary mapping attachment titles to file paths
    :type attachments: dict
    :returns: The list of items (in list format) that represent the ``items`` API value
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    if not attachment_titles and not file_paths and not attachments:
        raise errors.exceptions.MissingRequiredDataError("Missing required attachment data")
    if not attachments:
        attachments = _consolidate_attachment_data(attachment_titles, file_paths)
    list_items = []
    for title, path in attachments.items():
        item = {
            "type": "attachment",
            "field": f"{title}",
            "filename": f"{os.path.basename(path)}"
        }
        list_items.append(item)
    return list_items


def _consolidate_attachment_data(_attachment_titles, _file_paths):
    """This function consolidates the attachment titles and associated file paths into a single mapping dictionary.

    .. versionadded:: 2.3.0

    :param _attachment_titles: One or more attachment titles (e.g. ``User Guide``, ``Config File``, etc.)
    :type _attachment_titles: str, tuple, list, set
    :param _file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type _file_paths: str, tuple, list, set
    :returns: Dictionary that maps attachment titles to their file paths
    """
    _check_for_mismatch(_attachment_titles, _file_paths)
    _attachment_titles, _file_paths = _convert_strings_to_tuple(_attachment_titles, _file_paths)
    _attachment_titles, _file_paths = core_utils.convert_set(_attachment_titles), core_utils.convert_set(_file_paths)
    _attachment_data = {}
    for idx in range(len(_attachment_titles)):
        _attachment_data[_attachment_titles[idx]] = _file_paths[idx]
    return _attachment_data


def _check_for_mismatch(_attachment_titles, _file_paths):
    """This function checks to ensure there is not a mismatch between the attachment titles and associated file paths.

    .. versionadded:: 2.3.0

    :param _attachment_titles: One or more attachment titles (e.g. ``User Guide``, ``Config File``, etc.)
    :type _attachment_titles: str, tuple, list, set
    :param _file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type _file_paths: str, tuple, list, set
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    _types = [type(_attachment_titles), type(_file_paths)]
    _mismatch = False
    try:
        if (str not in _types) and (len(_attachment_titles) != len(_file_paths)):
            _mismatch = True
        elif str in _types:
            _type_length_dict = {}
            for _value in (_attachment_titles, _file_paths):
                _type_length_dict[type(_value)] = len(_value)
            for _val_type, _val_length in _type_length_dict.items():
                if _val_type != str and _val_length != 1:
                    print(f"Type: {_val_type}; Length: {_val_length}")
                    _mismatch = True
    except (TypeError, IndexError):
        _mismatch = True
    if _mismatch:
        raise errors.exceptions.DataMismatchError(data=('attachment_titles', 'file_paths'))
    return


def get_file_upload_info(attachment_titles=None, file_paths=None, attachments=None):
    """This function constructs the binary file(s) portion of the multipart API call.

    .. versionadded:: 2.3.0

    :param attachment_titles: One or more attachment titles (e.g. ``User Guide``, ``Config File``, etc.)
    :type attachment_titles: str, tuple, list, set
    :param file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type file_paths: str, tuple, list, set
    :param attachments: A consolidated dictionary mapping attachment titles to file paths
    :type attachments: dict
    :returns: A dictionary with the file upload information for the API call
    """
    if not attachment_titles and not file_paths and not attachments:
        raise errors.exceptions.MissingRequiredDataError("Missing required attachment data")
    if not attachments:
        attachments = _consolidate_attachment_data(attachment_titles, file_paths)
    files = []
    for title, path in attachments.items():
        file_info = ('file', (title, open(path, 'rb')))
        files.append(file_info)
    return files


def _convert_strings_to_tuple(_attachment_titles, _file_paths):
    """This function converts string variables into single-entry tuples for attachment titles and file paths.

    .. versionadded:: 2.3.0

    :param _attachment_titles: One or more attachment titles (e.g. ``User Guide``, ``Config File``, etc.)
    :type _attachment_titles: str, tuple, list, set
    :param _file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
    :type _file_paths: str, tuple, list, set
    :returns: A tuple of tuples for attachment titles and file paths
    """
    _tuples = []
    for _value in (_attachment_titles, _file_paths):
        if type(_value) == str:
            _tuples.append(core_utils.convert_single_value_to_tuple(_value))
        else:
            _tuples.append(_value)
    return tuple(_tuples)
