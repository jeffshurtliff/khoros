# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.exceptions
:Synopsis:          Collection of exception classes relating to the khoros library
:Usage:             ``import khoros.errors.exceptions``
:Example:           ``raise khoros.errors.exceptions.BadCredentialsError``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Mar 2020
"""

#################
# Base Exception
#################


# Define base exception classes
class KhorosError(Exception):
    """This is the base class for Khoros exceptions."""
    pass


############################
# Authentication Exceptions
############################


# Define exception for missing authentication data
class InvalidCallbackURLError(KhorosError):
    """This exception is used when an invalid Callback URL for OAuth 2.0 was not provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The OAuth 2.0 callback URL that was provided is invalid. The entire URL must be provided."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('URL ')[0]}'{kwargs['val']}'{default_msg.split('URL')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


# Define exception for missing authentication data
class MissingAuthDataError(KhorosError):
    """This exception is used when authentication data is not supplied and therefore a connection cannot occur."""
    def __init__(self, *args, **kwargs):
        default_msg = "The authentication data was not provided and a connection cannot be established."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


# Define exception for missing authentication data
class SessionAuthenticationError(KhorosError):
    """This exception is used when the session key authentication attempt failed."""
    def __init__(self, *args, **kwargs):
        default_msg = "The session key authentication attempt failed."
        if not (args or kwargs):
            args = (default_msg,)
        # TODO: Add alternate message if variable is passed to the exception class
        super().__init__(*args)


#####################
# General Exceptions
#####################


class CurrentlyUnsupportedError(KhorosError):
    """This exception is used when a feature or functionality being used is currently unsupported."""
    def __init__(self, *args, **kwargs):
        default_msg = "This function is currently unsupported at this time."
        if not (args or kwargs):
            args = (default_msg,)
        # TODO: Add alternate message if variable is passed to the exception class
        super().__init__(*args)


#########################
# Generic API Exceptions
#########################


class APIConnectionError(KhorosError):
    """This exception is used when the API query could not be completed due to connection aborts and/or timeouts."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API query could not be completed due to connection aborts and/or timeouts."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class GETRequestError(KhorosError):
    """This exception is used for generic GET request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The GET request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidEndpointError(KhorosError):
    """This exception is used when an invalid API endpoint / service is provided."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied endpoint for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'people' and 'contents')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidLookupTypeError(KhorosError):
    """This exception is used when an invalid API lookup type is provided."""

    def __init__(self, *args, **kwargs):
        default_msg = "The supplied lookup type for the API is not recognized. (Examples of valid " + \
                      "lookup types include 'id' and 'email')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidRequestTypeError(KhorosError):
    """This exception is used when an invalid API request type is provided."""

    def __init__(self, *args, **kwargs):
        default_msg = "The supplied request type for the API is not recognized. (Examples of valid " + \
                      "request types include 'POST' and 'PUT')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class LookupMismatchError(KhorosError):
    """This exception is used when an a lookup value doesn't match the supplied lookup type."""
    def __init__(self, *args, **kwargs):
        default_msg = "The supplied lookup type for the API does not match the value that was provided."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class NotFoundResponseError(KhorosError):
    """This exception is used when an API query returns a 404 response and there isn't a more specific class."""
    def __init__(self, *args, **kwargs):
        default_msg = "The API query returned a 404 response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class POSTRequestError(KhorosError):
    """This exception is used for generic POST request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The POST request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PUTRequestError(KhorosError):
    """This exception is used for generic PUT request errors when there isn't a more specific exception."""
    def __init__(self, *args, **kwargs):
        default_msg = "The PUT request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


####################
# Helper Exceptions
####################


class InvalidHelperFileTypeError(KhorosError, ValueError):
    """This exception is used when an invalid file type is provided for the helper file."""
    def __init__(self, *args, **kwargs):
        default_msg = "The helper configuration file can only have the 'yaml' or 'json' file type."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class InvalidHelperArgumentsError(KhorosError, ValueError):
    """This exception is used when the helper function was supplied arguments instead of keyword arguments."""
    def __init__(self, *args, **kwargs):
        default_msg = "The helper configuration file only accepts basic keyword arguments. (e.g. arg_name='arg_value')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class HelperFunctionNotFoundError(KhorosError, FileNotFoundError):
    """This exception is used when a function referenced in the helper config file does not exist."""
    def __init__(self, *args, **kwargs):
        default_msg = "The function referenced in the helper configuration file could not be found."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


##################
# LiQL Exceptions
##################


# Define exception for missing authentication data
class InvalidOperatorError(KhorosError):
    """This exception is used when authentication data is not supplied and therefore a connection cannot occur."""
    def __init__(self, *args, **kwargs):
        default_msg = "An invalid operator was provided for the LiQL query."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


# Define exception for missing authentication data
class OperatorMismatchError(KhorosError):
    """This exception is used when authentication data is not supplied and therefore a connection cannot occur."""
    def __init__(self, *args, **kwargs):
        default_msg = "The number of operators provided in the LiQL query does not match the number of fields/values."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)
