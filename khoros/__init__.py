# -*- coding: utf-8 -*-
"""
:Package:        khoros
:Synopsis:       This is the ``__init__`` module for the khoros package
:Usage:          ``import khoros``
:Example:        ``khoros.initialize(base_url='community.example.com', community='mycommunity')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  29 Jan 2020
"""

from . import core
from .utils import version

# Define the package version by pulling from the khoros.utils.version module
__version__ = version.get_full_version()


def initialize(**kwargs):
    """This function initializes the package by defining a global dictionary of environmental variables.
    
    :param kwargs: Keyword arguments to popuate in the global dictionary
    :type kwargs: dict 
    :returns: None
    """
    # Define the global dictionary if it doesn't already exist
    try:
        settings
    except NameError:
        global settings
        settings = {}

    # Execute the khoros.core.initialize() function and retrieve the global variable
    core.initialize(kwargs)
    settings = core.settings
    return
