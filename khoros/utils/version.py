# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.version
:Synopsis:          This simple script contains the package version
:Usage:             ``from .utils import version``
:Example:           ``__version__ = version.get_full_version()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     16 Jan 2022
"""

import json
import urllib.request

from . import log_utils

# Define special and global variables
__version__ = "4.5.0"
latest_version_reported = False
logger = log_utils.initialize_logging(__name__)


def get_full_version():
    """This function returns the current full version of the khoros package."""
    return __version__


def log_current_version(debug=False):
    """This function reports the current running version of the library in a debug log entry.

    .. versionadded:: 3.0.0

    :param debug: Defines if the message should be logged with the ``DEBUG`` log level. (``False`` by default)
    :type debug: bool
    :returns: None
    """
    log_msg = f'The current version of the library is {__version__}.'
    if debug:
        logger.debug(log_msg)
    else:
        logger.info(log_msg)
    return


def get_major_minor_version():
    """This function returns the current major.minor (i.e. X.Y) version of the khoros package."""
    return ".".join(__version__.split(".")[:2])


def get_latest_stable():
    """This function returns the latest stable version of the khoros package.

    .. versionchanged:: 3.4.0
       This function has been refactored to leverage the standard library instead of the ``requests`` library.

    .. versionchanged:: 3.0.0
       Error handling and logging was added to avoid an exception if PyPI cannot be queried successfully.

    :returns: The latest stable version in string format
    """
    try:
        response = urllib.request.urlopen('https://pypi.org/pypi/khoros/json')
        pypi_data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        latest_stable = pypi_data['info']['version']
        global latest_version_reported
        if not latest_version_reported:
            logger.debug(f'The latest stable version of the library on PyPI is {latest_stable}.')
            latest_version_reported = True
    except Exception as exc:
        exc_msg = f"{type(exc).__name__} - {exc}"
        logger.error("Unable to perform the query to retrieve the latest stable version of the library due "
                     f"to the following exception: {exc_msg}")
        latest_stable = '0.0.0'
    return latest_stable


def latest_version():
    """This function defines if the current version matches the latest stable version on PyPI.

    .. versionchanged:: 3.0.0
       The function was reduced to a single return statement.

    :returns: Boolean value indicating if the versions match
    """
    return True if get_full_version() == get_latest_stable() else False


def warn_when_not_latest():
    """This function displays a :py:exc:`RuntimeWarning` if the running version doesn't match the latest stable version.

    .. versionchanged:: 3.0.0
       The function was updated to use logging for the warning rather than the :py:mod:`warnings` module.

    :returns: None
    """
    if not latest_version():
        if get_latest_stable() != '0.0.0':
            warn_msg = "The latest stable version of khoros is not running. " + \
                       "Consider running 'pip install khoros --upgrade' when feasible."
            logger.warning(warn_msg)
    return


# Log the current version only when debug mode is enabled
log_current_version(debug=True)
