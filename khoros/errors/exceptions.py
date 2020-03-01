# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.exceptions
:Synopsis:          Collection of exception classes relating to the khoros library
:Usage:             ``import khoros.errors.exceptions``
:Example:           ``raise khoros.errors.exceptions.BadCredentialsError``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Mar 2020
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
