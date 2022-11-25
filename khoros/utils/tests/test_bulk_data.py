# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_bulk_data
:Synopsis:       This module is used by pytest to test the Bulk Data API module
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  25 Nov 2022
"""

import requests

from . import resources


def test_base_url_without_helper():
    """This function tests the functionality of the :py:func:`khoros.bulk_data.get_base-url` function.

    .. versionadded:: 5.0.0
    """
    # Test without parameters
    base_url = bulk_data.get_base_url()
    assert base_url == 'https://api.lithium.com/lsi-data/v2/data/export/community/'

    # Test European URL
    base_url = bulk_data.get_base_url(europe=True)
    assert base_url == 'https://eu.api.lithium.com/lsi-data/v2/data/export/community/'

    # Test with explicitly defined Community ID
    amer_base_url = bulk_data.get_base_url(community_id='something.prod')
    eu_base_url = bulk_data.get_base_url(community_id='something.prod', europe=True)
    assert amer_base_url == 'https://api.lithium.com/lsi-data/v2/data/export/community/something.prod'
    assert eu_base_url == 'https://eu.api.lithium.com/lsi-data/v2/data/export/community/something.prod'


def test_core_object_settings():
    """This function tests to ensure the bulk_data element exists in the core object with all of its fields.

    .. versionadded:: 5.0.0
    """
    khoros_object = resources.initialize_khoros_object()
    assert khoros_object.bulk_data_settings
    for field in ['community_id', 'client_id', 'token', 'europe', 'base_url', 'export_type']:
        assert field in khoros_object.bulk_data_settings


def test_export_type_header():
    """This function tests the retrieval of the appropriate ``Accept`` header value depending on the export type.

    .. versionadded:: 5.0.0
    """
    assert bulk_data._get_export_header('csv') == 'text/csv'
    assert bulk_data._get_export_header('CSV') == 'text/csv'
    assert bulk_data._get_export_header('json') == 'application/json'
    assert bulk_data._get_export_header('JSON') == 'application/json'
    assert bulk_data._get_export_header('other') == 'text/csv'


def test_valid_header_construction():
    """This function tests the construction of the API call headers when valid parameters are provided.

    .. versionadded:: 5.0.0
    """
    khoros_object = resources.initialize_khoros_object()
    headers = bulk_data._construct_headers(khoros_object, '12345')
    assert isinstance(headers, dict) and 'client-id' in headers and 'Accept' in headers
    assert headers.get('Accept') == 'text/csv' or headers.get('Accept') == 'application/json'


def test_valid_parameter_construction():
    """This function tests to ensure the parameters get constructed appropriately with valid data.

    .. versionadded:: 5.0.0
    """
    # Define input values
    from_date = '20220313'
    to_date = '20220314'
    fields_string = 'document.id,action.key,event.time.ms'
    fields_list = ['document.id', 'action.key', 'event.time.ms']

    # Define expected output value
    expected_params = {
        'fromDate': '20220313',
        'toDate': '20220314',
        'fields': 'document.id,action.key,event.time.ms'
    }

    # Test to confirm that the function works properly
    assert bulk_data._construct_parameters(from_date, to_date, fields_string) == expected_params
    assert bulk_data._construct_parameters(from_date, to_date, fields_list) == expected_params


def test_bulk_data_query(monkeypatch):
    """This function tests the ability to query the Bulk Data API and retrieve a JSON response.

    .. versionadded:: 5.2.0
    """
    # Instantiate the core object
    khoros_object = resources.get_core_object()

    # Overwrite the requests.get functionality with the mock_post() function
    monkeypatch.setattr(requests, 'get', resources.mock_bulk_data_json)

    # Make the mock API call
    response = khoros_object.bulk_data.query(
        community_id='example.prod',
        client_id='ay0CXXXXXXXXXX/XXXX+XXXXXXXXXXXXX/XXXXX4KhQ=',
        token='2f25XXXXXXXXXXXXXXXXXXXXXXXXXa10dec04068',
        from_date='20221031',
        to_date='20221101',
        export_type='json'
    )

    # Verify that the API call was a success
    assert 'records' in response and isinstance(response['records'], list)


# Import modules and initialize the core object
bulk_data, exceptions = resources.import_modules('khoros.bulk_data', 'khoros.errors.exceptions')
