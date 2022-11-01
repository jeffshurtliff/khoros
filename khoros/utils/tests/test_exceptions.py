# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_exceptions
:Synopsis:          This module is used by pytest to verify that the exceptions can be raised properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Oct 2022
"""

import pytest

from ...errors import exceptions


def test_raising_exceptions():
    """This function tests that exceptions are raised successfully.

    .. versionadded:: 5.1.2
    """
    # Test raising the InvalidStructureTypeError exception
    with pytest.raises(exceptions.InvalidStructureTypeError):
        raise exceptions.InvalidStructureTypeError()
    with pytest.raises(exceptions.InvalidStructureTypeError):
        raise exceptions.InvalidStructureTypeError(val='testing')

    # Test raising the InvalidCallbackURLError exception
    with pytest.raises(exceptions.InvalidCallbackURLError):
        raise exceptions.InvalidCallbackURLError()
    with pytest.raises(exceptions.InvalidCallbackURLError):
        raise exceptions.InvalidCallbackURLError(val='testing')

    # Test raising the MissingAuthDataError exception
    with pytest.raises(exceptions.MissingAuthDataError):
        raise exceptions.MissingAuthDataError()

    # Test raising the SessionAuthenticationError exception
    with pytest.raises(exceptions.SessionAuthenticationError):
        raise exceptions.SessionAuthenticationError()
    with pytest.raises(exceptions.SessionAuthenticationError):
        raise exceptions.SessionAuthenticationError(message='testing')

    # Test raising the SsoAuthenticationError exception
    with pytest.raises(exceptions.SsoAuthenticationError):
        raise exceptions.SsoAuthenticationError()
    with pytest.raises(exceptions.SsoAuthenticationError):
        raise exceptions.SsoAuthenticationError(message='testing')

    # Test raising the CurrentlyUnsupportedError exception
    with pytest.raises(exceptions.CurrentlyUnsupportedError):
        raise exceptions.CurrentlyUnsupportedError()
    with pytest.raises(exceptions.CurrentlyUnsupportedError):
        raise exceptions.CurrentlyUnsupportedError('testing')
    with pytest.raises(exceptions.CurrentlyUnsupportedError):
        raise exceptions.CurrentlyUnsupportedError(message='testing')

    # Test raising the DataMismatchError exception
    with pytest.raises(exceptions.DataMismatchError):
        raise exceptions.DataMismatchError()
    with pytest.raises(exceptions.DataMismatchError):
        raise exceptions.DataMismatchError(data='testing')
    with pytest.raises(exceptions.DataMismatchError):
        raise exceptions.DataMismatchError(data=['testing1', 'testing2'])

    # Test raising the InvalidParameterError exception
    with pytest.raises(exceptions.InvalidParameterError):
        raise exceptions.InvalidParameterError()
    with pytest.raises(exceptions.InvalidParameterError):
        raise exceptions.InvalidParameterError(val='testing')

    # Test raising the InvalidFieldError exception
    with pytest.raises(exceptions.InvalidFieldError):
        raise exceptions.InvalidFieldError()
    with pytest.raises(exceptions.InvalidFieldError):
        raise exceptions.InvalidFieldError(val='testing')

    # Test raising the InvalidURLError exception
    with pytest.raises(exceptions.InvalidURLError):
        raise exceptions.InvalidURLError()
    with pytest.raises(exceptions.InvalidURLError):
        raise exceptions.InvalidURLError(url='khoros.com')

    # Test raising the MissingRequiredDataError exception
    with pytest.raises(exceptions.MissingRequiredDataError):
        raise exceptions.MissingRequiredDataError()
    with pytest.raises(exceptions.MissingRequiredDataError):
        raise exceptions.MissingRequiredDataError('init')
    with pytest.raises(exceptions.MissingRequiredDataError):
        raise exceptions.MissingRequiredDataError('initialize', object='testing')

    # Test raising the UnknownFileTypeError exception
    with pytest.raises(exceptions.UnknownFileTypeError):
        raise exceptions.UnknownFileTypeError()
    with pytest.raises(exceptions.UnknownFileTypeError):
        raise exceptions.UnknownFileTypeError(file='testing.txt')

    # Test raising the APIConnectionError exception
    with pytest.raises(exceptions.APIConnectionError):
        raise exceptions.APIConnectionError()

    # Test raising the APIRequestError exception
    with pytest.raises(exceptions.APIRequestError):
        raise exceptions.APIRequestError()

    # Test raising the DELETERequestError exception
    with pytest.raises(exceptions.DELETERequestError):
        raise exceptions.DELETERequestError()

    # Test raising the FeatureNotConfiguredError exception
    with pytest.raises(exceptions.FeatureNotConfiguredError):
        raise exceptions.FeatureNotConfiguredError()
    with pytest.raises(exceptions.FeatureNotConfiguredError):
        raise exceptions.FeatureNotConfiguredError(identifier='testing')
    with pytest.raises(exceptions.FeatureNotConfiguredError):
        raise exceptions.FeatureNotConfiguredError(feature='testing')

    # Test raising the GETRequestError exception
    with pytest.raises(exceptions.GETRequestError):
        raise exceptions.GETRequestError()
    with pytest.raises(exceptions.GETRequestError):
        raise exceptions.GETRequestError(status_code=400)
    with pytest.raises(exceptions.GETRequestError):
        raise exceptions.GETRequestError(message='testing')
    with pytest.raises(exceptions.GETRequestError):
        raise exceptions.GETRequestError(status_code=400, message='testing')

    # Test raising the InvalidEndpointError exception
    with pytest.raises(exceptions.InvalidEndpointError):
        raise exceptions.InvalidEndpointError()

    # Test raising the InvalidLookupTypeError exception
    with pytest.raises(exceptions.InvalidLookupTypeError):
        raise exceptions.InvalidLookupTypeError()

    # Test raising the InvalidPayloadValueError exception
    with pytest.raises(exceptions.InvalidPayloadValueError):
        raise exceptions.InvalidPayloadValueError()
    with pytest.raises(exceptions.InvalidPayloadValueError):
        raise exceptions.InvalidPayloadValueError(value='test_value')
    with pytest.raises(exceptions.InvalidPayloadValueError):
        raise exceptions.InvalidPayloadValueError(value='test_value', field='test_field')

    # Test raising the InvalidRequestTypeError exception
    with pytest.raises(exceptions.InvalidRequestTypeError):
        raise exceptions.InvalidRequestTypeError()

    # Test raising the LookupMismatchError exception
    with pytest.raises(exceptions.LookupMismatchError):
        raise exceptions.LookupMismatchError()

    # Test raising the NotFoundResponseError exception
    with pytest.raises(exceptions.NotFoundResponseError):
        raise exceptions.NotFoundResponseError()

    # Test raising the PayloadMismatchError exception
    with pytest.raises(exceptions.PayloadMismatchError):
        raise exceptions.PayloadMismatchError()
    with pytest.raises(exceptions.PayloadMismatchError):
        raise exceptions.PayloadMismatchError(request_type='post')

    # Test raising the POSTRequestError exception
    with pytest.raises(exceptions.POSTRequestError):
        raise exceptions.POSTRequestError()
    with pytest.raises(exceptions.POSTRequestError):
        raise exceptions.POSTRequestError(status_code=400)
    with pytest.raises(exceptions.POSTRequestError):
        raise exceptions.POSTRequestError(message='testing')
    with pytest.raises(exceptions.POSTRequestError):
        raise exceptions.POSTRequestError(status_code=400, message='testing')

    # Test raising the PUTRequestError exception
    with pytest.raises(exceptions.PUTRequestError):
        raise exceptions.PUTRequestError()
    with pytest.raises(exceptions.PUTRequestError):
        raise exceptions.PUTRequestError(status_code=400)
    with pytest.raises(exceptions.PUTRequestError):
        raise exceptions.PUTRequestError(message='testing')
    with pytest.raises(exceptions.PUTRequestError):
        raise exceptions.PUTRequestError(status_code=400, message='testing')

    # Test raising the InvalidHelperFileTypeError exception
    with pytest.raises(exceptions.InvalidHelperFileTypeError):
        raise exceptions.InvalidHelperFileTypeError()

    # Test raising the InvalidHelperArgumentsError exception
    with pytest.raises(exceptions.InvalidHelperArgumentsError):
        raise exceptions.InvalidHelperArgumentsError()

    # Test raising the HelperFunctionNotFoundError exception
    with pytest.raises(exceptions.HelperFunctionNotFoundError):
        raise exceptions.HelperFunctionNotFoundError()

    # Test raising the InvalidOperatorError exception
    with pytest.raises(exceptions.InvalidOperatorError):
        raise exceptions.InvalidOperatorError()

    # Test raising the LiQLParseError exception
    with pytest.raises(exceptions.LiQLParseError):
        raise exceptions.LiQLParseError()
    with pytest.raises(exceptions.LiQLParseError):
        raise exceptions.LiQLParseError(message='testing')

    # Test raising the OperatorMismatchError exception
    with pytest.raises(exceptions.OperatorMismatchError):
        raise exceptions.OperatorMismatchError()

    # Test raising the TooManyResultsError exception
    with pytest.raises(exceptions.TooManyResultsError):
        raise exceptions.TooManyResultsError()

    # Test raising the InvalidMetadataError exception
    with pytest.raises(exceptions.InvalidMetadataError):
        raise exceptions.InvalidMetadataError()
    with pytest.raises(exceptions.InvalidMetadataError):
        raise exceptions.InvalidMetadataError(metadata='testing')

    # Test raising the MessageTypeNotFoundError exception
    with pytest.raises(exceptions.MessageTypeNotFoundError):
        raise exceptions.MessageTypeNotFoundError()
    with pytest.raises(exceptions.MessageTypeNotFoundError):
        raise exceptions.MessageTypeNotFoundError(msg_type='testing')
    with pytest.raises(exceptions.MessageTypeNotFoundError):
        raise exceptions.MessageTypeNotFoundError(url='khoros.com')

    # Test raising the InvalidMessagePayloadError exception
    with pytest.raises(exceptions.InvalidMessagePayloadError):
        raise exceptions.InvalidMessagePayloadError()

    # Test raising the InvalidNodeTypeError exception
    with pytest.raises(exceptions.InvalidNodeTypeError):
        raise exceptions.InvalidNodeTypeError()
    with pytest.raises(exceptions.InvalidNodeTypeError):
        raise exceptions.InvalidNodeTypeError(val='testing')

    # Test raising the NodeIDNotFoundError exception
    with pytest.raises(exceptions.NodeIDNotFoundError):
        raise exceptions.NodeIDNotFoundError()
    with pytest.raises(exceptions.NodeIDNotFoundError):
        raise exceptions.NodeIDNotFoundError(val='testing')

    # Test raising the NodeTypeNotFoundError exception
    with pytest.raises(exceptions.NodeTypeNotFoundError):
        raise exceptions.NodeTypeNotFoundError()
    with pytest.raises(exceptions.NodeTypeNotFoundError):
        raise exceptions.NodeTypeNotFoundError(val='testing')

    # Test raising the UnsupportedNodeTypeError exception
    with pytest.raises(exceptions.UnsupportedNodeTypeError):
        raise exceptions.UnsupportedNodeTypeError()
    with pytest.raises(exceptions.UnsupportedNodeTypeError):
        raise exceptions.UnsupportedNodeTypeError(node_type='test_type')
    with pytest.raises(exceptions.UnsupportedNodeTypeError):
        raise exceptions.UnsupportedNodeTypeError(node_type='test_type', operation='testing stuff')

    # Test raising the InvalidRoleError exception
    with pytest.raises(exceptions.InvalidRoleError):
        raise exceptions.InvalidRoleError()
    with pytest.raises(exceptions.InvalidRoleError):
        raise exceptions.InvalidRoleError(role='testing')

    # Test raising the InvalidRoleTypeError exception
    with pytest.raises(exceptions.InvalidRoleTypeError):
        raise exceptions.InvalidRoleTypeError()
    with pytest.raises(exceptions.InvalidRoleTypeError):
        raise exceptions.InvalidRoleTypeError(role_type='testing')

    # Test raising the UserCreationError exception
    with pytest.raises(exceptions.UserCreationError):
        raise exceptions.UserCreationError()
    with pytest.raises(exceptions.UserCreationError):
        raise exceptions.UserCreationError(user='testing')
    with pytest.raises(exceptions.UserCreationError):
        raise exceptions.UserCreationError(exc_msg='this is an error message')
