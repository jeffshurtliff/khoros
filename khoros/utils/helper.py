# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.helper
:Synopsis:       Module that allows the khoros library to leverage a helper configuration file
:Usage:          ``from khoros.utils import helper``
:Example:        ``helper_settings = helper.get_settings('/tmp/helper.yml', 'yaml')``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  21 Feb 2020
"""

import yaml

from .. import errors


# Define function to import a YAML helper file
def import_yaml_file(file_path):
    """This function imports a YAML (.yml) helper config file.

    :param file_path: The file path to the YAML file
    :type file_path: str
    :returns: The parsed configuration data
    :raises: FileNotFoundError
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
    # Define the base URL as a global string variable
    _connection_info = {
        'community_url': _helper_cfg['connection']['community_url'],
        'tenant_id': _helper_cfg['connection']['tenant_id']
    }

    # Parse OAuth 2.0 information if found
    if 'oauth2' in _helper_cfg['connection']:
        _connection_info['oauth2'] = __get_oauth2_info(_helper_cfg)

    # Parse session authentication information if found
    if 'session_auth' in _helper_cfg['connection']:
        _connection_info['session_auth'] = __get_session_auth_info(_helper_cfg)
    return _connection_info


def __get_oauth2_info(_helper_cfg):
    """This function parses OAuth 2.0 information if found in the helper file."""
    _oauth2 = {
        'client_id': _helper_cfg['connection']['oauth2']['client_id'],
        'client_secret': _helper_cfg['connection']['oauth2']['client_secret'],
        'redirect_url': _helper_cfg['connection']['oauth2']['redirect_url']
    }
    return _oauth2


def __get_session_auth_info(_helper_cfg):
    """This function parses session authentication information if found in the helper file."""
    _session_auth = {
        'username': _helper_cfg['connection']['session_auth']['username'],
        'password': _helper_cfg['connection']['session_auth']['password']
    }
    return _session_auth


# Define function to retrieve the helper configuration settings
def get_helper_settings(file_path, file_type='yaml'):
    """This function returns a dictionary of the defined helper settings.

    :param file_path: The file path to the helper configuration file
    :type file_path: str
    :param file_type: Defines the helper configuration file as a ``yaml`` file (default) or a ``json`` file
    :type file_type: str
    :returns: Dictionary of helper variables
    :raises: InvalidHelperFileTypeError
    """
    # Initialize the helper_settings dictionary
    helper_settings = {}

    # Import the helper configuration file
    if file_type == 'yaml':
        helper_cfg = import_yaml_file(file_path)
    else:
        raise errors.exceptions.InvalidHelperFileTypeError

    # Populate and return the helper_settings dictionary
    if 'connection' in helper_cfg:
        helper_settings['connection'] = __get_connection_info(helper_cfg)
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
