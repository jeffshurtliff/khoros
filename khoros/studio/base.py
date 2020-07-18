# -*- coding: utf-8 -*-
"""
:Module:            khoros.studio.base
:Synopsis:          This module handles the base functionality of the studio module.
:Usage:             ``import khoros.studio.base as studio_base``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def sdk_installed():
    """This function checks to see if the Lithium SDK is installed.

    .. versionadded:: 2.5.1

    :returns: Boolean value indicating whether or not the Lithium SDK is installed
    """
    try:
        output = core_utils.run_cmd('li')
        is_installed = True if output['return_code'] == 0 else False
    except FileNotFoundError:
        is_installed = False
    return is_installed


def get_sdk_version():
    """This function identifies the currently installed version of the Lithium SDK.

    .. versionadded:: 2.5.1

    :returns: The SDK version in string format or ``None`` if not installed
    """
    version = None
    if npm_installed() and sdk_installed():
        output = core_utils.run_cmd('npm list -g lithium-sdk', decode_output=True, strip_output=False)['stdout']
        output = core_utils.decode_binary(output)
        if '(empty)' not in output:
            version = output.split('lithium-sdk@')[1].split(' ')[0]
    return version


def node_installed():
    """This function checks whether or not Node.js is installed.

    .. versionadded:: 2.5.1

    :returns: Boolean value indicating whether or not Node.js is installed
    """
    node_version = get_node_version()
    return True if node_version else False


def get_node_version():
    """This function identifies and returns the installed Node.js version.

    .. versionadded:: 2.5.1

    :returns: The version as a string or ``None`` if not installed
    """
    try:
        version = core_utils.run_cmd('node -v', decode_output=True, strip_output=True)['stdout']
        if 'v' in version:
            version = version[1:]
    except FileNotFoundError:
        version = None
    return version


def npm_installed():
    """This function checks whether or not npm is installed.

    .. versionadded:: 2.5.1

    :returns: Boolean value indicating whether or not npm is installed
    """
    npm_version = get_npm_version()
    return True if npm_version else False


def get_npm_version():
    """This function identifies and returns the installed npm version.

    .. versionadded:: 2.5.1

    :returns: The version as a string or ``None`` if not installed
    """
    try:
        version = core_utils.run_cmd('npm -v', decode_output=True, strip_output=True)['stdout']
        if 'v' in version:
            version = version[1:]
    except FileNotFoundError:
        version = None
    return version
