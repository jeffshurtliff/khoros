# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.version
:Synopsis:          This simple script contains the package version
:Usage:             ``from .utils import version``
:Example:           ``__version__ = version.get_full_version()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Mar 2020
"""

import warnings

import requests

__version__ = "1.2.0"


def get_full_version():
    """This function returns the current full version of the khoros package."""
    return __version__


def get_major_minor_version():
    """This function returns the current major.minor (i.e. X.Y) version of the khoros package."""
    return ".".join(__version__.split(".")[:2])


def get_latest_stable():
    """This function returns the latest stable version of the khoros package.

    :returns: The latest stable version in string format
    """
    pypi_data = requests.get('https://pypi.org/pypi/khoros/json').json()
    return pypi_data['info']['version']


def latest_version():
    """This function defines if the current version matches the latest stable version on PyPI.

    :returns: Boolean value indicating if the versions match
    """
    latest_stable = get_latest_stable()
    return True if __version__ == latest_stable else False


def warn_when_not_latest():
    """This function displays a :py:exc:`RuntimeWarning` if the running version doesn't match the latest stable version.

    :returns: None
    """
    try:
        if not latest_version():
            warn_msg = "The latest stable version of khoros is not running. " + \
                       "Consider running 'pip install khoros --upgrade' when feasible."
            warnings.warn(warn_msg, RuntimeWarning)
    except Exception:
        pass
    return
