# -*- coding: utf-8 -*-
"""
:Package:        khoros.errors
:Synopsis:       This module includes custom exceptions
:Usage:          ``import khoros.errors`` (Imported by default in primary package)
:Example:        ``raise errors.exceptions.MissingAuthDataError``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  21 Feb 2020
"""
# Define all modules that will be imported with the "import *" method
__all__ = ['exceptions', 'handlers']

# Always import the warnings package and the exceptions module
from . import exceptions, handlers
