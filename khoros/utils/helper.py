# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.helper
:Synopsis:          Module that allows the khoros library to leverage a helper configuration file
:Usage:             ``from khoros.utils import helper``
:Example:           ``helper_settings = helper.get_settings('/tmp/helper.yml', 'yaml')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Mar 2020
"""

import yaml

from .. import errors


# Define function to import a YAML helper file
def import_yaml_file(file_path):
    """This function imports a YAML (.yml) helper config file.

    :param file_path: The file path to the YAML file
    :type file_path: str
    :returns: The parsed configuration data
    :raises: :py:exc:`FileNotFoundError`
    """
    with open(file_path, 'r') as yml_file:
        helper_cfg = yaml.load(yml_file, Loader=yaml.BaseLoader)
    return helper_cfg


# Define function to covert a YAML Boolean value to a Python Boolean value
def __convert_yaml_to_bool(_yaml_bool_value):
    """This function converts the 'yes' and 'no' YAML values to traditional Boolean values."""
    true_values = ['yes', 'true']
    if _yaml_bool_value.lower() in true_values:
        _bool_value = True
    else:
        _bool_value = False
    return _bool_value


# Define function to get the connection information
def __get_connection_info(_helper_cfg):
    """This function parses any connection information found in the helper file."""
    _connection_info = {}
    _connection_keys = ['community_url', 'tenant_id', 'default_auth_type']
    for _key in _connection_keys:
        if _key in _helper_cfg['connection']:
            _connection_info[_key] = _helper_cfg['connection'][_key]

    # Parse OAuth 2.0 information if found
    if 'oauth2' in _helper_cfg['connection']:
        _connection_info['oauth2'] = __get_oauth2_info(_helper_cfg)

    # Parse session authentication information if found
    if 'session_auth' in _helper_cfg['connection']:
        _connection_info['session_auth'] = __get_session_auth_info(_helper_cfg)
    return _connection_info


def __get_oauth2_info(_helper_cfg):
    """This function parses OAuth 2.0 information if found in the helper file."""
    _oauth2 = {}
    _oauth2_keys = ['client_id', 'client_secret', 'redirect_url']
    for _key in _oauth2_keys:
        if _key in _helper_cfg['connection']['oauth2']:
            _oauth2[_key] = _helper_cfg['connection']['oauth2'][_key]
        else:
            _oauth2[_key] = ''
    return _oauth2


def __get_session_auth_info(_helper_cfg):
    """This function parses session authentication information if found in the helper file."""
    _session_auth = {}
    _session_info = ['username', 'password']
    for _key in _session_info:
        if _key in _helper_cfg['connection']['session_auth']:
            _session_auth[_key] = _helper_cfg['connection']['session_auth'][_key]
        else:
            _session_auth[_key] = None
    return _session_auth


def __get_construct_info(_helper_cfg):
    """This function parses settings that can be leveraged in constructing API responses and similar tasks."""
    _construct_info = {}
    _top_level_keys = ['prefer_json']
    for _key in _top_level_keys:
        if _key in _helper_cfg:
            _key_val = _helper_cfg[_key]
            if _key_val in HelperParsing.yaml_boolean_values:
                _key_val = HelperParsing.yaml_boolean_values.get(_key_val)
            _construct_info[_key] = _key_val
        else:
            _construct_info[_key] = None
    return _construct_info


# Define function to retrieve the helper configuration settings
def get_helper_settings(file_path, file_type='yaml'):
    """This function returns a dictionary of the defined helper settings.

    :param file_path: The file path to the helper configuration file
    :type file_path: str
    :param file_type: Defines the helper configuration file as a ``yaml`` file (default) or a ``json`` file
    :type file_type: str
    :returns: Dictionary of helper variables
    :raises: :py:exc:`khoros.errors.exceptions.InvalidHelperFileTypeError`
    """
    # Initialize the helper_settings dictionary
    helper_settings = {}

    # Import the helper configuration file
    if file_type == 'yaml':
        helper_cfg = import_yaml_file(file_path)
    else:
        raise errors.exceptions.InvalidHelperFileTypeError

    # Populate the connection information in the helper dictionary
    if 'connection' in helper_cfg:
        helper_settings['connection'] = __get_connection_info(helper_cfg)

    # Populate the construct information in the helper dictionary
    helper_settings['construct'] = __get_construct_info(helper_cfg)

    # Return the helper_settings dictionary
    return helper_settings


# Define class for dictionaries to help in parsing the configuration files
class HelperParsing:
    """This class is used to help parse values imported from a YAML configuration file."""
    # Define dictionary to map YAML Boolean to Python Boolean
    yaml_boolean_values = {
        True: True,
        False: False,
        'yes': True,
        'no': False
    }
