# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.exceptions
:Synopsis:          Collection of exception classes relating to the khoros library
:Usage:             ``import khoros.errors.exceptions``
:Example:           ``raise khoros.errors.exceptions.BadCredentialsError()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Jan 2022
"""

#################
# Base Exception
#################


# Define base exception class
class KhorosError(Exception):
    """This is the base class for Khoros exceptions."""
    pass


############################
# Base Structure Exceptions
############################


class InvalidStructureTypeError(KhorosError):
    """This exception is used when an invalid node type is provided.

    .. versionadded:: 2.1.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The structure type that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('structure type ')[0]}'{kwargs['val']}'{default_msg.split('The')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


############################
# Authentication Exceptions
############################


class InvalidCallbackURLError(KhorosError):
    """This exception is used when an invalid Callback URL for OAuth 2.0 was not provided."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The OAuth 2.0 callback URL that was provided is invalid. The entire URL must be provided."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('URL ')[0]}'{kwargs['val']}'{default_msg.split('URL')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class MissingAuthDataError(KhorosError):
    """This exception is used when authentication data is not supplied and therefore a connection cannot occur."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The authentication data was not provided and a connection cannot be established."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class SessionAuthenticationError(KhorosError):
    """This exception is used when the session key authentication attempt failed."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The session key authentication attempt failed."
        custom_msg = default_msg.replace('.', ' with the following message:')
        if not (args or kwargs):
            args = (default_msg,)
        elif 'message' in kwargs:
            custom_msg = f"{custom_msg} {kwargs['message']}"
            args = (custom_msg,)
        super().__init__(*args)


class SsoAuthenticationError(KhorosError):
    """This exception is used when the SSO authentication attempt failed.

    .. versionadded:: 4.2.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The SSO authentication attempt failed."
        custom_msg = default_msg.replace('.', ' with the following message:')
        if not (args or kwargs):
            args = (default_msg,)
        elif 'message' in kwargs:
            custom_msg = f"{custom_msg} {kwargs['message']}"
            args = (custom_msg,)
        super().__init__(*args)


#####################
# General Exceptions
#####################


class CurrentlyUnsupportedError(KhorosError):
    """This exception is used when a feature or functionality being used is currently unsupported.

    .. versionchanged:: 4.5.0
       Introduced the ability for a fully customized message to be displayed.

    .. versionchanged:: 2.0.0
       The unsupported feature can be passed as a string argument to explicitly reference it in the exception.
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "This feature is currently unsupported at this time."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'message' in kwargs:
            args =(kwargs['message'],)
        else:
            custom_msg = f"The '{args[0]}' {default_msg.split('This ')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class DataMismatchError(KhorosError):
    """This exception is used when there is a mismatch between two data sources.

    .. versionadded:: 2.3.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "A data mismatch was found with the data sources."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'data' in kwargs:
            multi_types = [list, tuple, set]
            if type(kwargs['data']) == str:
                custom_msg = f"{default_msg.split('data')[0]}'{kwargs['val']}'{default_msg.split('with the')[1]}"
                custom_msg = custom_msg.replace('sources', 'source')
                args = (custom_msg,)
            elif type(kwargs['data']) in multi_types and len(kwargs['data']) == 2:
                custom_section = f"'{kwargs['data'][0]}' and '{kwargs['data'][1]}'"
                custom_msg = f"{default_msg.split('data sources')[0]}{custom_section}{default_msg.split('with the')[1]}"
                args = (custom_msg,)
        super().__init__(*args)


class InvalidFieldError(KhorosError):
    """This exception is used when an invalid field is provided.

    .. versionadded:: 2.1.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The field that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('field ')[0]}'{kwargs['val']}'{default_msg.split('The')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class InvalidURLError(KhorosError):
    """This exception is used when a provided URL is invalid.

    .. versionadded:: 2.1.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The provided URL is invalid"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'url' in kwargs:
            custom_msg = f"{default_msg.split('is')[0]}'{kwargs['url']}'{default_msg.split('URL')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class MissingRequiredDataError(KhorosError):
    """This exception is used when a function or method is missing one or more required arguments.

    .. versionchanged:: 4.0.0
       The exception can now accept the ``param`` keyword argument.

    .. versionadded:: 2.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "Missing one or more required parameters"
        init_msg = "The object failed to initialize as it is missing one or more required arguments."
        param_msg = "The required parameter 'PARAMETER_NAME' is not defined"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'init' in args or 'initialize' in args:
            if 'object' in kwargs:
                custom_msg = f"{init_msg.split('object')[0]}'{kwargs['object']}'{init_msg.split('The')[1]}"
                args = (custom_msg,)
            else:
                args = (init_msg,)
        elif 'param' in kwargs:
            args = (param_msg.replace('PARAMETER_NAME', kwargs['param']),)
        else:
            args = (default_msg,)
        super().__init__(*args)


class UnknownFileTypeError(KhorosError):
    """This exception is used when a file type of a given file cannot be identified.

    .. versionadded:: 2.2.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The file type of the given file path cannot be identified."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'file' in kwargs:
            custom_msg = f"{default_msg.split('path')[0]}'{kwargs['file']}'{default_msg.split('path')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


#########################
# Generic API Exceptions
#########################


class APIConnectionError(KhorosError):
    """This exception is used when the API query could not be completed due to connection aborts and/or timeouts."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API query could not be completed due to connection aborts and/or timeouts."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIRequestError(KhorosError):
    """This exception is used for generic API request errors when there isn't a more specific exception.

    .. versionchanged:: 4.5.0
       Fixed an issue with the default message.
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class DELETERequestError(KhorosError):
    """This exception is used for generic DELETE request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The DELETE request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class FeatureNotConfiguredError(KhorosError):
    """This exception is used when an API request fails because a feature is not configured.

    .. versionadded:: 4.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        exc_msg = "The feature is not configured."
        if 'identifier' in kwargs or 'feature' in kwargs:
            if 'identifier' in kwargs:
                exc_msg += f" Identifier: {kwargs['identifier']}"
            if 'feature' in kwargs:
                exc_msg = exc_msg.replace("feature", f"{kwargs['feature']} feature")
            args = (exc_msg,)
        elif not (args or kwargs):
            args = (exc_msg,)
        super().__init__(*args)


class GETRequestError(KhorosError):
    """This exception is used for generic GET request errors when there isn't a more specific exception.

    .. versionchanged:: 3.2.0
       Enabled the ability to optionally pass ``status_code`` and/or ``message`` arguments.
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The GET request did not return a successful response."
        custom_msg = "The GET request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidEndpointError(KhorosError):
    """This exception is used when an invalid API endpoint / service is provided."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied endpoint for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'people' and 'contents')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidLookupTypeError(KhorosError):
    """This exception is used when an invalid API lookup type is provided."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied lookup type for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'id' and 'email')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidPayloadValueError(KhorosError):
    """This exception is used when an invalid value is provided for a payload field.

    .. versionadded:: 2.6.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "An invalid payload value was provided."
        custom_msg = "The invalid payload value 'X' was provided for the 'Y' field."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'value' in kwargs:
            if 'field' in kwargs:
                custom_msg = custom_msg.replace('X', kwargs['value']).replace('Y', kwargs['field'])
            else:
                custom_msg = f"{custom_msg.replace('X', kwargs['value']).split(' for the')[0]}."
            args = (custom_msg,)
        super().__init__(*args)


class InvalidRequestTypeError(KhorosError):
    """This exception is used when an invalid API request type is provided."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied request type for the API is not recognized. (Examples of valid " + \
                      "request types include 'POST' and 'PUT')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class LookupMismatchError(KhorosError):
    """This exception is used when an a lookup value doesn't match the supplied lookup type."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied lookup type for the API does not match the value that was provided."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class NotFoundResponseError(KhorosError):
    """This exception is used when an API query returns a 404 response and there isn't a more specific class."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API query returned a 404 response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PayloadMismatchError(KhorosError):
    """This exception is used when more than one payload is supplied for an API request.

    .. versionadded:: 3.2.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "More than one payload was provided for the API call when only one is permitted."
        if not (args or kwargs):
            args = (default_msg,)
        elif kwargs['request_type']:
            custom_msg = default_msg.replace("API call", f"{kwargs['request_type'].upper()} request")
            args = (custom_msg,)
        super().__init__(*args)


class POSTRequestError(KhorosError):
    """This exception is used for generic POST request errors when there isn't a more specific exception.

    .. versionchanged:: 3.2.0
       Enabled the ability to optionally pass ``status_code`` and/or ``message`` arguments.
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The POST request did not return a successful response."
        custom_msg = "The POST request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PUTRequestError(KhorosError):
    """This exception is used for generic PUT request errors when there isn't a more specific exception.

    .. versionchanged:: 3.2.0
       Enabled the ability to optionally pass ``status_code`` and/or ``message`` arguments.
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The PUT request did not return a successful response."
        custom_msg = "The PUT request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


####################
# Helper Exceptions
####################


class InvalidHelperFileTypeError(KhorosError, ValueError):
    """This exception is used when an invalid file type is provided for the helper file."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The helper configuration file can only have the 'yaml' or 'json' file type."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidHelperArgumentsError(KhorosError):
    """This exception is used when the helper function was supplied arguments instead of keyword arguments."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The helper configuration file only accepts basic keyword arguments. (e.g. arg_name='arg_value')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class HelperFunctionNotFoundError(KhorosError):
    """This exception is used when a function referenced in the helper config file does not exist."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The function referenced in the helper configuration file could not be found."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


##################
# LiQL Exceptions
##################


class InvalidOperatorError(KhorosError):
    """This exception is used when an invalid operator is provided for the LiQL query."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "An invalid operator was provided for the LiQL query."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class LiQLParseError(KhorosError):
    """This exception is used when a function is unable to successfully parse a LiQL response.

    .. versionadded:: 3.2.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "Failed to parse the LiQL query response."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'message' in kwargs and kwargs['message']:
            custom_section = f" as the query failed with the following message: {kwargs['message']}"
            custom_msg = default_msg.replace('.', custom_section)
            args = (custom_msg,)
        super().__init__(*args)


class OperatorMismatchError(KhorosError):
    """This exception is used when the number of operators in the LiQL query does not match the number of fields."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The number of operators provided in the LiQL query does not match the number of fields/values."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class TooManyResultsError(KhorosError):
    """This exception is used when more results are returned than were expected in a LiQL query.

    .. versionchanged:: 3.2.0
       Fixed the default message to be appropriate as it was the same message found in another exception.

    .. versionadded:: 2.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "More results were returned in the LiQL response than were expected."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


#####################
# Message Exceptions
#####################


class InvalidMetadataError(KhorosError):
    """This exception is used when there is an issue involving message metadata.

    .. versionadded:: 4.5.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The message metadata is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'metadata' in kwargs:
            custom_msg = f"{default_msg.split('is')[0]}'{kwargs.get('metadata')}'{default_msg.split('is')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class MessageTypeNotFoundError(KhorosError):
    """This exception is used when a message type cannot be identified from a given URL."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The message type could not be identified in the provided URL."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'msg_type' in kwargs:
            custom_msg = f"{default_msg.split('message type ')[0]}'{kwargs['msg_type']}'{default_msg.split('type')[1]}"
            args = (custom_msg,)
        elif 'url' in kwargs:
            custom_msg = f"{default_msg.split('provided')[0]}following URL: {kwargs['url']}"
            args = (custom_msg,)
        super().__init__(*args)


class InvalidMessagePayloadError(KhorosError):
    """This exception is used when the payload for creating a message is invalid."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The message payload is invalid and cannot be utilized."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


##################
# Node Exceptions
##################


class InvalidNodeTypeError(KhorosError):
    """This exception is used when an invalid node type is provided."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The node type that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('node type ')[0]}'{kwargs['val']}'{default_msg.split('The')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class NodeIDNotFoundError(KhorosError):
    """This exception is used when a valid Node ID could not be found in a provided URL."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "A valid Node ID could not be identified in the given URL."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('URL')[0]}: {kwargs['val']}"
            args = (custom_msg,)
        super().__init__(*args)


class NodeTypeNotFoundError(KhorosError):
    """This exception is used when a valid node type could not be found in a provided URL."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "A valid node type could not be identified in the given URL."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('URL')[0]}: {kwargs['val']}"
            args = (custom_msg,)
        super().__init__(*args)


class UnsupportedNodeTypeError(KhorosError):
    """This exception is used when an unsupported node type has been provided.

    .. versionadded:: 3.2.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The node type is unsupported with the given operation."
        if 'node_type' in kwargs:
            custom_msg = f"{default_msg.split('node ')[0]}'{kwargs['node_type']}' node{default_msg.split('node')[1]}"
            if 'operation' in kwargs:
                custom_msg = custom_msg.replace('the given operation', kwargs['operation'])
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


##################
# Role Exceptions
##################


class InvalidRoleError(KhorosError):
    """This exception is used when an invalid role is provided."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The role is invalid"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'role' in kwargs:
            custom_msg = f"{default_msg.split('role ')[0]}'{kwargs['role']}'{default_msg.split('role')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class InvalidRoleTypeError(KhorosError):
    """This exception is used when an invalid role type is provided."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The role type is invalid"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'role_type' in kwargs:
            custom_msg = f"{default_msg.split('type ')[0]}'{kwargs['role_type']}'{default_msg.split('type ')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


##################
# User Exceptions
##################


class UserCreationError(KhorosError):
    """This exception is used when an attempt to create a user fails."""
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The user failed to be created."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'user' in kwargs:
            custom_msg = f"{default_msg.split('user ')[0]}'{kwargs['user']}'{default_msg.split('user')[1]}"
            args = (custom_msg,)
        if 'exc_msg' in kwargs:
            full_msg = f"{args[0].split('.')[0]} due to the following exception: {kwargs['exc_msg']}"
            args = (full_msg,)
        super().__init__(*args)
