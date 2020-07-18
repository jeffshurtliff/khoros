# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.archives
:Synopsis:          This module includes functions that handle archiving messages.
:Usage:             ``from khoros.objects import archives``
:Example:           ``archives.archive(khoros_obj, '123', suggested_url, return_status=True)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

import warnings

from .. import api, errors
from . import messages
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def archive(khoros_object, message_id=None, message_url=None, suggested_url=None, archive_entries=None,
            full_response=None, return_id=None, return_url=None, return_api_url=None, return_http_code=None,
            return_status=None, return_error_messages=None, split_errors=False):
    """This function archives one or more messages while providing an optional suggested URL as a placeholder.

    .. versionadded:: 2.7.0

    :param khoros_object:
    :param message_id: The message ID for the content to be archived
    :type message_id: str, int, None
    :param message_url: The URL of the message to be archived (as an alternative to the ``message_id`` argument)
    :type message_url: str, None
    :param suggested_url: The full URL to suggest to the user if the user tries to access the archived message
    :type suggested_url: str, None
    :param archive_entries: A dictionary mapping one or more message IDs with accompanying suggested URLs

                            .. note:: Alternatively, a list, tuple or set of message IDs can be supplied which
                                      will be converted into a dictionary with blank suggested URLs.

    :type archive_entries: dict, list, tuple, set, None
    :param full_response: Determines whether the full, raw API response should be returned by the function

                          .. caution:: This argument overwrites the ``return_id``, ``return_url``, ``return_api_url``,
                                       ``return_http_code``, ``return_status`` and ``return_error_messages`` arguments.

    :type full_response: bool, None
    :param return_id: Determines if the **ID** of the new group hub should be returned by the function
    :type return_id: bool, None
    :param return_url: Determines if the **URL** of the new group hub should be returned by the function
    :type return_url: bool, None
    :param return_api_url: Determines if the **API URL** of the new group hub should be returned by the function
    :type return_api_url: bool, None
    :param return_http_code: Determines if the **HTTP Code** of the API response should be returned by the function
    :type return_http_code: bool, None
    :param return_status: Determines if the **Status** of the API response should be returned by the function
    :type return_status: bool, None
    :param return_error_messages: Determines if any error messages associated with the API response should be
                                  returned by the function
    :type return_error_messages: bool, None
    :param split_errors: Defines whether or not error messages should be merged when applicable
    :type split_errors: bool
    :returns: Boolean value indicating a successful outcome (default), the full API response or one or more specific
              fields defined by function arguments
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    if not any((message_id, message_url, archive_entries)):
        raise errors.exceptions.MissingRequiredDataError("The message ID or URL must be provided to archive content.")
    if not message_id and message_url:
        message_id = messages.get_id_from_url(message_url)
    api_url = f"{khoros_object.core['v2_base']}/archives/archive"
    payload = structure_archive_payload(message_id, suggested_url, archive_entries)
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object)
    return api.deliver_v2_results(response, full_response, return_id, return_url, return_api_url, return_http_code,
                                  return_status, return_error_messages, split_errors)


def unarchive(khoros_object, message_id=None, message_url=None, new_board_id=None, archive_entries=None,
              full_response=None, return_id=None, return_url=None, return_api_url=None, return_http_code=None,
              return_status=None, return_error_messages=None, split_errors=False):
    """This function archives one or more messages while providing an optional suggested URL as a placeholder.

    .. versionadded:: 2.7.0

    :param khoros_object:
    :param message_id: The message ID for the content to be archived
    :type message_id: str, int, None
    :param message_url: The URL of the message to be archived (as an alternative to the ``message_id`` argument)
    :type message_url: str, None
    :param new_board_id: The board ID of what will be the new parent board of a message getting unarchived
    :type new_board_id: str, None
    :param archive_entries: A dictionary mapping one or more message IDs with accompanying board IDs

                            .. note:: Alternatively, a list, tuple or set of message IDs can be supplied which
                                      will be converted into a dictionary with blank board IDs.

    :type archive_entries: dict, list, tuple, set, None
    :param full_response: Determines whether the full, raw API response should be returned by the function

                          .. caution:: This argument overwrites the ``return_id``, ``return_url``, ``return_api_url``,
                                       ``return_http_code``, ``return_status`` and ``return_error_messages`` arguments.

    :type full_response: bool, None
    :param return_id: Determines if the **ID** of the new group hub should be returned by the function
    :type return_id: bool, None
    :param return_url: Determines if the **URL** of the new group hub should be returned by the function
    :type return_url: bool, None
    :param return_api_url: Determines if the **API URL** of the new group hub should be returned by the function
    :type return_api_url: bool, None
    :param return_http_code: Determines if the **HTTP Code** of the API response should be returned by the function
    :type return_http_code: bool, None
    :param return_status: Determines if the **Status** of the API response should be returned by the function
    :type return_status: bool, None
    :param return_error_messages: Determines if any error messages associated with the API response should be
                                  returned by the function
    :type return_error_messages: bool, None
    :param split_errors: Defines whether or not error messages should be merged when applicable
    :type split_errors: bool
    :returns: Boolean value indicating a successful outcome (default), the full API response or one or more specific
              fields defined by function arguments
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    if not any((message_id, message_url, archive_entries)):
        raise errors.exceptions.MissingRequiredDataError("The message ID or URL must be provided to archive content.")
    if not message_id and message_url:
        message_id = messages.get_id_from_url(message_url)
    api_url = f"{khoros_object.core['v2_base']}/archives/unarchive"
    payload = structure_archive_payload(message_id, new_board_id=new_board_id,
                                        archive_entries=archive_entries, unarchiving=True)
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object)
    return api.deliver_v2_results(response, full_response, return_id, return_url, return_api_url, return_http_code,
                                  return_status, return_error_messages, split_errors)


def structure_archive_payload(message_id, suggested_url=None, new_board_id=None, archive_entries=None,
                              unarchiving=False):
    """This function structures the payload for an archive-related API call.

    .. versionadded:: 2.7.0

    :param message_id: The message ID for the content to be archived
    :type message_id: str, int, None
    :param suggested_url: The full URL to suggest to the user if the user tries to access the archived message
    :type suggested_url: str, None
    :param new_board_id: The board ID of what will be the new parent board of a message getting unarchived
    :type new_board_id: str, None
    :param archive_entries: A dictionary mapping one or more message IDs with accompanying suggested URLs (archiving)
                            or new board IDs (unarchiving)

                            .. note:: Alternatively, a list, tuple or set of message IDs can be supplied which
                                      will be converted into a dictionary with blank suggested URLs (archiving) or
                                      blank new board IDs (unarchiving).

    :type archive_entries: dict, list, tuple, set, None
    :param unarchiving: Indicates that the payload is for an **unarchive** task (``False`` by default)
    :type unarchiving: bool
    :returns: The payload for the API call as a list of dictionaries containing message IDs and/or suggested URLs
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    payload = []
    if message_id:
        if suggested_url:
            payload.append(_format_single_archive_entry(message_id, suggested_url, _unarchiving=unarchiving))
        elif new_board_id:
            payload.append(_format_single_archive_entry(message_id, _new_board_id=new_board_id,
                                                        _unarchiving=unarchiving))
        else:
            payload.append(_format_single_archive_entry(message_id))
    if archive_entries:
        if not _valid_entries_type(archive_entries) and len(payload) == 0:
            raise errors.exceptions.MissingRequiredDataError("An invalid 'archive_dict' value was provided and a"
                                                             "message ID or message URL was not provided. Nothing"
                                                             "to archive.")
        elif not isinstance(archive_entries, dict):
            if any((isinstance(archive_entries, tuple), isinstance(archive_entries, list),
                    isinstance(archive_entries, set))):
                archive_entries = _convert_entries_to_dict(archive_entries)
        for entry_id, entry_url in archive_entries.items():
            payload.append(_format_single_archive_entry(entry_id, entry_url))
    return payload


def _valid_entries_type(_entries):
    """This function checks whether or not the ``archive_entries`` argument is a valid type.

    .. versionadded:: 2.7.0

    :param _entries: The ``archive_entries`` value from the parent function
    :returns: Boolean value indicating whether the value is a ``dict``, ``tuple``, ``list`` or ``set``
    """
    return any((isinstance(_entries, dict), isinstance(_entries, tuple),
                isinstance(_entries, list), isinstance(_entries, set)))


def _convert_entries_to_dict(_entries):
    """This function converts a list, tuple or set of archive entries into a dictionary.

    .. versionadded:: 2.7.0

    .. caution:: This is only permitted when the values

    :param _entries:
    :return:
    """
    _new_dict = {}
    for _entry in _entries:
        if isinstance(_entry, str) and not _entry.isnumeric():
            warnings.warn(f"The entry '{_entry}' is not a valid message ID and will be ignored.", RuntimeWarning)

        else:
            _new_dict[str(_entry)] = ""
    return _new_dict


def _format_single_archive_entry(_message_id, _suggested_url=None, _new_board_id=None, _unarchiving=False):
    """This function formats a single entry to be archived.

    .. versionadded:: 2.7.0

    :param _message_id: The ID of the message to be archived
    :type _message_id: str, int
    :param _suggested_url: The full URL to suggest to the user if the user tries to access the archived message
    :type _suggested_url: str, None
    :param _new_board_id: The board ID of a new parent board for a message getting unarchived
    :type _new_board_id: str, None
    :param _unarchiving: Indicates that the payload is for an **unarchive** task (``False`` by default)
    :type _unarchiving: bool
    :returns: The properly formatted archive entry
    """
    _archive_entry = {"messageID": str(_message_id)}
    if _suggested_url and isinstance(_suggested_url, str) and not _unarchiving:
        _archive_entry['suggestedUrl'] = _suggested_url
    elif (_new_board_id and isinstance(_new_board_id, str)) or \
            (_suggested_url and isinstance(_suggested_url, str) and _unarchiving):
        _archive_entry['boardId'] = _new_board_id
    return _archive_entry
