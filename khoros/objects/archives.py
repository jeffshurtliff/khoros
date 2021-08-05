# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.archives
:Synopsis:          This module includes functions that handle archiving messages.
:Usage:             ``from khoros.objects import archives``
:Example:           ``archives.archive(khoros_obj, '123', suggested_url, return_status=True)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     05 Aug 2021
"""

import warnings

from .. import api, errors
from . import messages
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def archive(khoros_object, message_id=None, message_url=None, suggested_url=None, archive_entries=None,
            aggregate_results=False, include_raw=False):
    """This function archives one or more messages while providing an optional suggested URL as a placeholder.

    .. versionchanged:: 4.1.0
       Made some minor docstring and code adjustments and also removed the following parameters due to the unique
       response format: ``full_response``, ``return_id``, ``return_url``, ``return_api_url``, ``return_http_code``,
       ``return_status``, ``return_error_messages`` and ``split_errors``

       An issue with the :py:func:`khoros.objects.archives.structure_archive_payload` function call was also resolved.

       The optional ``aggregate_results`` parameter has also been introduced.

    .. versionadded:: 2.7.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param message_id: The message ID for the content to be archived
    :type message_id: str, int, None
    :param message_url: The URL of the message to be archived (as an alternative to the ``message_id`` argument)
    :type message_url: str, None
    :param suggested_url: The full URL to suggest to the user when navigating to the archived message
    :type suggested_url: str, None
    :param archive_entries: A dictionary mapping one or more message IDs with accompanying suggested URLs

                            .. note:: Alternatively, a list, tuple or set of message IDs can be supplied which
                                      will be converted into a dictionary with blank suggested URLs.

    :type archive_entries: dict, list, tuple, set, None
    :param aggregate_results: Aggregates the operation results into an easy-to-parse dictionary (``False`` by default)
    :type aggregate_results: bool
    :param include_raw: Includes the raw API response in the aggregated data dictionary under the ``raw`` key
                        (``False`` by default)

                        .. note:: This parameter is only relevant when the ``aggregate_results`` parameter is ``True``.

    :type include_raw: bool
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
    api_url = f"{khoros_object.core.get('v2_base')}/archives/archive"
    payload = structure_archive_payload(message_id, suggested_url, archive_entries=archive_entries)
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object,
                                             content_type='application/json')
    results = api.deliver_v2_results(response, full_response=True)
    return aggregate_results_data(results, include_raw) if aggregate_results else results


def unarchive(khoros_object, message_id=None, message_url=None, new_board_id=None, archive_entries=None,
              aggregate_results=False, include_raw=False):
    """This function unarchives one or more messages and moves them to a given board.

    .. versionchanged:: 4.1.0
       Made some minor docstring and code adjustments and also removed the following parameters due to the unique
       response format: ``full_response``, ``return_id``, ``return_url``, ``return_api_url``, ``return_http_code``,
       ``return_status``, ``return_error_messages`` and ``split_errors``

       The optional ``aggregate_results`` parameter has also been introduced.

    .. versionadded:: 2.7.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    :param aggregate_results: Aggregates the operation results into an easy-to-parse dictionary (``False`` by default)
    :type aggregate_results: bool
    :param include_raw: Includes the raw API response in the aggregated data dictionary under the ``raw`` key
                        (``False`` by default)

                        .. note:: This parameter is only relevant when the ``aggregate_results`` parameter is ``True``.

    :type include_raw: bool
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
    api_url = f"{khoros_object.core.get('v2_base')}/archives/unarchive"
    payload = structure_archive_payload(message_id, new_board_id=new_board_id,
                                        archive_entries=archive_entries, unarchiving=True)
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object,
                                             content_type='application/json')
    results = api.deliver_v2_results(response, full_response=True)
    return aggregate_results_data(results, include_raw) if aggregate_results else results


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


def aggregate_results_data(results, include_raw=False):
    """This function aggregates the results of an archive/unarchive operation into an easy-to-parse dictionary.

    .. versionchanged:: 4.1.1
       This function can now properly handle the ``ARCHIVED`` status when returned.

    .. versionadded:: 4.1.0

    :param results: The results from an archive or unarchive operation
    :type results: list, dict
    :param include_raw: Includes the raw API response in the aggregated data dictionary under the ``raw`` key
                        (``False`` by default)
    :type include_raw: bool
    :returns: A dictionary with fields for ``status``, ``archived``, ``unarchived``, ``failed`` and ``unknown`` or the
              raw response when the API call completely fails, with the optional raw data when requested
    """
    # Initially define the aggregate data
    aggregate_data = {'status': 'success'}
    archived_values = ['ARCHIVING', 'ARCHIVED']
    archived, unarchived, failed, unknown = [], [], [], 0

    # Return the raw error response if the entire API call failed
    if isinstance(results, dict) and results.get('status') == 'error':
        # TODO: Record a log entry for the failed API call
        aggregate_data.update(results)
    elif isinstance(results, list):
        for message in results:
            if isinstance(message, dict) and message.get('archivalStatus') in archived_values:
                archived.append(f"{message.get('msgUid')}")
            elif isinstance(message, dict) and message.get('unarchivalStatus') == 'UNARCHIVING':
                unarchived.append(f"{message.get('msgUid')}")
            elif isinstance(message, dict) and message.get('msgUid'):
                failed.append(f"{message.get('msgUid')}")
            else:
                # TODO: Record a log entry for the unknown result
                unknown += 1

        # Update the aggregate data with the parsed results and return the dictionary
        aggregate_data['archived'] = archived
        aggregate_data['unarchived'] = unarchived
        aggregate_data['failed'] = failed
        aggregate_data['unknown'] = unknown
        if include_raw:
            aggregate_data['raw'] = results
        return aggregate_data


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

    .. versionchanged:: 4.1.0
       The ``messageID`` key was incorrect and has been fixed to be ``messageId`` instead.

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
    _archive_entry = {"messageId": str(_message_id)}
    if _suggested_url and isinstance(_suggested_url, str) and not _unarchiving:
        _archive_entry['suggestedUrl'] = _suggested_url
    elif (_new_board_id and isinstance(_new_board_id, str)) or \
            (_suggested_url and isinstance(_suggested_url, str) and _unarchiving):
        _archive_entry['boardId'] = _new_board_id
    return _archive_entry
