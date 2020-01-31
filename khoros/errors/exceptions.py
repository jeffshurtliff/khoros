# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.exceptions
:Synopsis:          Collection of exception classes relating to the khoros library
:Usage:             ``import khoros.errors.exceptions``
:Example:           ``raise khoros.errors.exceptions.BadCredentialsError``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     31 Jan 2020
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
        default_msg = "The authentication data was not provided and a connection cannot be established.."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)
