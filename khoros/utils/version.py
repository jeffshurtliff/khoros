# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.version
:Synopsis:          This simple script contains the package version
:Usage:             ``from .utils import version``
:Example:           ``__version__ = version.get_full_version()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Jan 2020
"""

__version__ = "1.0.0"


def get_full_version():
    """This function returns the current full version of the khoros package."""
    return __version__


def get_major_minor_version():
    """This function returns the current major.minor (i.e. X.Y) version of the khoros package."""
    return ".".join(__version__.split(".")[:2])
