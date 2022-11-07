# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.bulk_data
:Synopsis:          This module includes functions that relate to the Bulk Data API.
:Usage:             ``from khoros import bulk_data``
:Example:           ``base_url = bulk_data.get_base_url(community_id='example.prod')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Nov 2022
"""

import requests

from . import errors
from .utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_base_url(khoros_object=None, community_id=None, europe=False):
    """This function constructs and/or retrieves the base URL for the Bulk Data API.

    .. versionadded:: 5.0.0

    .. note:: The URL from the helper settings will be leveraged when available unless the ``community_id`` is
              explicitly defined as a function parameter.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None
    :param community_id: The Community ID to leverage in the URL
    :type community_id: str, None
    :param europe: Determines if the European URL should be utilized (``False`` by default)
    :type europe: bool
    :returns: The base URL for the Bulk Data API
    """
    base_url = None
    base_urls = {
        True: 'https://eu.api.lithium.com/lsi-data/v2/data/export/community/',
        False: 'https://api.lithium.com/lsi-data/v2/data/export/community/'
    }

    # Retrieve the base URL from the helper settings when defined
    if not community_id and khoros_object:
        try:
            base_url = khoros_object.bulk_data_settings['base_url']
        except (KeyError, AttributeError):
            # Attempt to define the community ID if found
            try:
                community_id = khoros_object.bulk_data_settings['community_id']
            except (KeyError, AttributeError):
                pass

    # Construct the base URL when not defined in the helper settings
    if not base_url:
        europe = False if europe is None else europe
        base_url = base_urls.get(europe)
        if community_id:
            base_url = f'{base_url}{community_id}'
    return base_url


def query(khoros_object=None, community_id=None, client_id=None, token=None, from_date=None, to_date=None, fields=None,
          europe=None, export_type=None, full_response=False):
    """This function performs a query against the Bulk Data API to retrieve CSV or JSON data.

    .. versionchanged:: 5.2.0
       Improved the error handling to display the response text in the raised exception when available.

    .. versionadded:: 5.0.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None
    :param community_id: The Community ID to leverage in the URL
    :type community_id: str, None
    :param client_id: The Client ID used to authenticate to the Bulk Data API
    :type client_id: str, None
    :param token: The access token used to authenticate to the Bulk Data API
    :type token: str, None
    :param from_date: The **From** Date in ``YYYYmmDD`` or ``YYYYmmDDhhMM`` format.
    :type from_date: str, None
    :param to_date: The **To** Date in ``YYYYmmDD`` or ``YYYYmmDDhhMM`` format.
    :type to_date: str, None
    :param fields: Optional fields to include in the data export as a comma-separated string or iterable
    :type fields: str, list, tuple, set, None
    :param europe: Determines if the European URL should be utilized (``False`` by default)
    :type europe: bool
    :param export_type: Determines if the data should be returned in ``csv`` (default) or ``json`` format
    :type export_type: str, None
    :param full_response: Determines if the full :py:mod:`requests` object should be returned (``False`` by default)
    :type full_response: bool
    :returns: The CSV or JSON data for the Bulk Data API request (or the full :py:mod:`requests` object)
    :raises: :py:exc:`TypeError`, :py:exc:`ValueError`,
             :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
             :py:exc:`khoros.errors.exceptions.APIRequestError`
    """
    # Get the base URL
    if khoros_object and khoros_object.bulk_data_settings.get('base_url'):
        base_url = khoros_object.bulk_data_settings.get('base_url')
    else:
        base_url = get_base_url(khoros_object, community_id, europe)

    # Get the client ID
    if not client_id:
        if khoros_object and khoros_object.bulk_data_settings.get('client_id'):
            client_id = khoros_object.bulk_data_settings.get('client_id')
        else:
            raise errors.exceptions.MissingAuthDataError('A valid Client ID is required to utilize the Bulk Data API.')

    # Get the auth token
    if not token:
        if khoros_object and khoros_object.bulk_data_settings.get('token'):
            token = khoros_object.bulk_data_settings.get('token')
        else:
            raise errors.exceptions.MissingAuthDataError('A valid access token is required to utilize the '
                                                         'Bulk Data API.')

    # Construct the API headers
    headers = _construct_headers(khoros_object, client_id, export_type)

    # Construct the authentication tuple
    auth = (token, '')

    # Construct the parameters
    params = _construct_parameters(from_date, to_date, fields)

    # Perform the API call
    response = requests.get(base_url, params=params, auth=auth, headers=headers)
    if not full_response:
        if response.status_code != 200:
            exc_msg = f'Bulk Data API request failed with a {response.status_code} response.'
            if response.text:
                exc_msg = exc_msg.replace('.', f': {response.text}')
            raise errors.exceptions.APIRequestError(exc_msg)
        if export_type.lower() == 'json':
            response = response.json()
        else:
            response = response.text
    return response


def filter_by_action(action_key, bulk_data):
    """This function filters a Bulk Data API export for only entries with a specific ``action.key`` value.

    .. versionadded:: 5.2.0

    :param action_key: The ``action.key`` value
    :type action_key: str
    :param bulk_data: The Bulk Data API export in JSON format (i.e. dictionary)
    :type bulk_data: dict
    :returns: The filtered JSON data as a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    filtered_data = []
    _validate_bulk_data_export(bulk_data)
    for entry in bulk_data['records']:
        if entry.get('action.key') == action_key:
            filtered_data.append(entry)
    filtered_data = {'records': filtered_data}
    return filtered_data


def filter_anonymous(bulk_data, remove_anonymous=None, remove_registered=None):
    """This function filters bulk data entries to keep only registered (default) or anonymous user activities.

    .. versionadded:: 5.2.0

    :param bulk_data: The Bulk Data API export in JSON format (i.e. dictionary)
    :type bulk_data: dict
    :param remove_anonymous: Determines if all anonymous user activities should be removed (Default)
    :type remove_anonymous: bool, None
    :param remove_registered: Determines if all registered user activities should be removed
    :type remove_registered: bool, None
    :returns: The filtered JSON data as a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`,
             :py:exc:`khoros.errors.exceptions.InvalidParameterError`
    """
    filtered_data = []
    _validate_bulk_data_export(bulk_data)
    if remove_anonymous is None and remove_registered is None:
        remove_anonymous = True
    if remove_anonymous and remove_registered:
        raise errors.exceptions.InvalidParameterError('You cannot remove both anonymous and registered users.')
    if not remove_anonymous and not remove_registered:
        raise errors.exceptions.InvalidParameterError('You must remove either anonymous or registered users.')
    for entry in bulk_data['records']:
        if (remove_anonymous and entry.get('user.registration_status') != 'ANONYMOUS') or \
                (remove_registered and entry.get('user.registration_status') == 'ANONYMOUS'):
            filtered_data.append(entry)
    filtered_data = {'records': filtered_data}
    return filtered_data


def count_actions(bulk_data, action_key):
    """This function counts the number of events for a specific action key in a collection of bulk data.

    .. versionadded:: 5.2.0

    :param bulk_data: The Bulk Data API export in JSON format (i.e. dictionary)
    :type bulk_data: dict
    :param action_key: The ``action.key`` value
    :type action_key: str
    :returns: The number of events as an integer
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    bulk_data = filter_by_action(action_key, bulk_data)
    return len(bulk_data['records'])


def count_logins(bulk_data):
    """This function counts the number of login events in a collection of bulk data.

    .. versionadded:: 5.2.0

    :param bulk_data: The Bulk Data API export in JSON format (i.e. dictionary)
    :type bulk_data: dict
    :returns: The number of login events as an integer
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    return count_actions(bulk_data, 'visits.member-entrance')


def count_views(bulk_data):
    """This function counts the number of view events in a collection of bulk data.

    .. versionadded:: 5.2.0

    :param bulk_data: The Bulk Data API export in JSON format (i.e. dictionary)
    :type bulk_data: dict
    :returns: The number of view events as an integer
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    return count_actions(bulk_data, 'view')


def _validate_bulk_data_export(_bulk_data):
    """This function validates exported bulk data to ensure it is a dictionary and in a recognizable format.

    .. versionadded:: 5.2.0

    :param _bulk_data: The exported Bulk Data API content
    :type _bulk_data: dict
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    if not isinstance(_bulk_data, dict):
        raise errors.exceptions.DataMismatchError('The Bulk Data must be provided as a dictionary to be filtered.')
    if 'records' not in _bulk_data:
        raise errors.exceptions.DataMismatchError('The Bulk Data is not in a recognized format.')


def _construct_parameters(_from_date=None, _to_date=None, _fields=None):
    """This function constructs the parameters to utilize in the API call.

    .. versionadded:: 5.0.0

    :param _from_date: The beginning date range parameter
    :type _from_date: str, None
    :param _to_date: The ending date range parameter
    :type _to_date: str, None
    :param _fields: The optional list of fields to include
    :type _fields: str, list, tuple, set, None
    :returns: The dictionary of parameters to use in the API call
    :raises: :py:exc:`TypeError`
    """
    # Validate and add the date parameters
    _validate_date_field(_from_date)
    _validate_date_field(_to_date)
    _params = {
        'fromDate': _from_date,
        'toDate': _to_date,
    }

    # Validate and add the fields parameter if applicable
    if _fields:
        if not isinstance(_fields, str):
            if isinstance(_fields, list) or isinstance(_fields, tuple) or isinstance(_fields, set):
                _fields = ','.join(_fields)
            else:
                raise TypeError('The fields parameter should be a comma-separated string or an iterable.')
        _params['fields'] = _fields
    return _params


def _validate_date_field(_date_value):
    """This function validates the ``fromDate`` and ``toDate`` fields to ensure they are in a valid format.

    .. versionadded:: 5.0.0

    :param _date_value: The date value to be evaluated (e.g. ``20220313``)
    :type _date_value: str
    :returns: None
    :raises: :py:exc:`ValueError`
    """
    if not isinstance(_date_value, str) or not _date_value.isnumeric() or \
            (len(_date_value) != 8 and len(_date_value) != 12):
        raise ValueError('The fromDate and toDate fields should be in yyyyMMdd or yyyyMMddHHmm format.')


def _construct_headers(_khoros_object=None, _client_id=None, _export_type=None):
    """This function constructs the headers to use in a Bulk Data API call.

    .. versionadded:: 5.0.0

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros], None
    :param _client_id: The Client ID to use when authenticating the API calls
    :type _client_id: str, None
    :param _export_type: Indicates the export type as either ``csv`` (default) or ``json``
    :type _export_type: str
    :returns: A dictionary containing the API headers
    :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
    """
    # Get the client ID
    if not _client_id:
        if _khoros_object and _khoros_object.bulk_data_settings.get('client_id'):
            _client_id = _khoros_object.bulk_data_settings.get('client_id')
        else:
            raise errors.exceptions.MissingAuthDataError('A valid Client ID is required to utilize the Bulk Data API.')

    # Get the Accept value depending on the export type
    if not _export_type:
        if _khoros_object and _khoros_object.bulk_data_settings.get('export_type'):
            _export_type = _khoros_object.bulk_data_settings.get('export_type')
        else:
            # Default to CSV export
            _export_type = 'csv'
    _accept_value = _get_export_header(_export_type)

    # Construct and return the header
    _headers = {
        'client-id': _client_id,
        'Accept': _accept_value
    }
    return _headers


def _get_export_header(_export_type='csv'):
    """This function retrieves the appropriate ``Accept`` header value depending on the export type.

    .. versionadded:: 5.0.0

    :param _export_type: Indicates the export type as either ``csv`` (default) or ``json``
    :type _export_type: str
    :returns: The appropriate ``Accept`` header value
    """
    if _export_type.lower() == 'json':
        _export_header_value = 'application/json'
    else:
        # TODO: Add warning log entry if not CSV
        _export_header_value = 'text/csv'
    return _export_header_value
