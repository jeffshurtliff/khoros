# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.messages
:Synopsis:          This module includes functions that identify environment variables for the khoros library
:Usage:             ``from khoros.utils import environment``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Apr 2021
"""

import os
import json
import importlib

from .. import errors
from ..utils.core_utils import get_file_type

ENV_VARIABLE_NAMES = ['KHOROS_URL', 'KHOROS_TENANT_ID', 'KHOROS_DEFAULT_AUTH', 'KHOROS_OAUTH_ID', 'KHOROS_OAUTH_SECRET',
                      'KHOROS_OAUTH_REDIRECT_URL', 'KHOROS_SESSION_USER', 'KHOROS_SESSION_PW', 'KHOROS_PREFER_JSON',
                      'KHOROS_LIQL_PRETTY', 'KHOROS_LIQL_TRACK_LSI', 'KHOROS_LIQL_ALWAYS_OK', 'KHOROS_TRANSLATE_ERRORS']

ENV_SETTINGS_MAPPING = {
    'KHOROS_URL': ('community_url',),
    'KHOROS_TENANT_ID': ('tenant_id',),
    'KHOROS_DEFAULT_AUTH': ('auth_type',),
    'KHOROS_OAUTH_ID': ('oauth2', 'client_id'),
    'KHOROS_OAUTH_SECRET': ('oauth2', 'client_secret'),
    'KHOROS_OAUTH_REDIRECT_URL': ('oauth2', 'redirect_url'),
    'KHOROS_SESSION_USER': ('session_auth', 'username'),
    'KHOROS_SESSION_PW': ('session_auth', 'password'),
    'KHOROS_PREFER_JSON': ('prefer_json',),
    'KHOROS_TRANSLATE_ERRORS': ('translate_errors',),
    # TODO: Add LiQL environment variables
}

# Define global variables for the variable names and mapping that can be overwritten by custom values
env_variable_names = ENV_VARIABLE_NAMES
env_settings_mapping = ENV_SETTINGS_MAPPING


def _env_variable_exists(env_variable):
    """This function checks to see if an environment variable is already defined.

    .. versionadded:: 2.2.0

    :param env_variable: The name of the environment variable for which to check
    :type env_variable: str
    :returns: Boolean value indicating if the environment variable already exists
    """
    found = False
    try:
        found = True if os.environ[env_variable] else False
    except KeyError:
        pass
    return found


def _get_env_variable_value(env_variable):
    """This function returns the value of a given environment variable name.

    .. versionadded:: 2.2.0

    :param env_variable: The name of the environment variable to return
    :type env_variable: str
    :returns: The value of the environment variable or ``None`` if the variable name does not exist
    """
    return os.getenv(env_variable)


def get_env_variables():
    """This function retrieves any defined environment variables associate with the khoros library.

    .. versionadded:: 2.2.0

    :returns: A dictionary with any relevant, defined environment variables
    """
    env_settings = {}
    for var_name in env_variable_names:
        if _env_variable_exists(var_name):
            env_settings[var_name] = _get_env_variable_value(var_name)
    return env_settings


def _update_env_list(_orig_name, _custom_name):
    """This function replaces a value in the ``env_variable_names`` global variable with a custom value.

    .. versionadded:: 2.2.0

    :param _orig_name: The original value to replace
    :type _orig_name: str
    :param _custom_name: The custom value that will replace the original value
    :type _custom_name: str
    :returns: None
    """
    if _orig_name in env_variable_names:
        env_variable_names.remove(_orig_name)
        env_variable_names.append(_custom_name)
    return


def _update_env_mapping(_orig_name, _custom_name):
    """This function replaces a dictionary key in the ``env_variable_mapping`` global variable with a custom name.

    .. versionadded:: 2.2.0

    :param _orig_name: The original value to replace
    :type _orig_name: str
    :param _custom_name: The custom value that will replace the original value
    :type _custom_name: str
    :returns: None
    """
    if _orig_name in env_settings_mapping:
        env_settings_mapping[_custom_name] = env_settings_mapping.pop(_orig_name)
    return


def update_env_variable_names(custom_names):
    """This function updates the original environment variable names with custom names when applicable.

    .. versionadded:: 2.2.0

    :param custom_names: A dictionary (or file path to a YAML or JSON file) that maps the original and custom names
    :type custom_names: dict, str
    :returns: None
    """
    if custom_names:
        if type(custom_names) == str:
            custom_names = _import_custom_names_file(custom_names)
        if type(custom_names) == dict:
            for orig_name, custom_name in custom_names.items():
                _update_env_list(orig_name, custom_name)
                _update_env_mapping(orig_name, custom_name)
    return


# Define function to import a YAML helper file
def _import_custom_names_file(file_path):
    """This function imports a YAML (.yml) helper config file.

    .. versionchanged:: 4.0.0
       The :py:mod:`importlib` module is now utilized to import the ``PyYAML`` package where necessary.

    .. versionadded:: 2.2.0

    :param file_path: The file path to the YAML file
    :type file_path: str
    :returns: The parsed configuration data
    :raises: :py:exc:`FileNotFoundError`, :py:exc:`khoros.errors.exceptions.UnknownFileTypeError`
    """
    file_type = get_file_type(file_path)
    with open(file_path, 'r') as cfg_file:
        if file_type == 'yaml':
            yaml = importlib.import_module('yaml')
            custom_names_cfg = yaml.safe_load(cfg_file)
        elif file_type == 'json':
            custom_names_cfg = json.load(cfg_file)
        else:
            raise errors.exceptions.UnknownFileTypeError(file=file_path)
    return custom_names_cfg
