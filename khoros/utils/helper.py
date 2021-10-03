# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.helper
:Synopsis:          Module that allows the khoros library to leverage a helper configuration file
:Usage:             ``from khoros.utils import helper``
:Example:           ``helper_settings = helper.get_settings('/tmp/helper.yml', 'yaml')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     23 Feb 2021
"""

import json

import yaml

from .. import errors
from . import log_utils
from .core_utils import get_file_type

# Initialize logging within the module
logger = log_utils.initialize_logging(__name__)


def import_helper_file(file_path, file_type):
    """This function imports a YAML (.yml) or JSON (.json) helper config file.

    .. versionchanged:: 3.3.0
       A log entry was added to report when the helper file has been imported successfully.

    .. versionchanged:: 2.2.0
       Changed the name and replaced the ``yaml.load`` function call with ``yaml.safe_load`` to be more secure.

    :param file_path: The file path to the YAML file
    :type file_path: str
    :param file_type: Defines the file type as either ``yaml`` or ``json``
    :type file_type: str
    :returns: The parsed configuration data
    :raises: :py:exc:`FileNotFoundError`, :py:exc:`khoros.errors.exceptions.InvalidHelperFileTypeError`
    """
    with open(file_path, 'r') as cfg_file:
        if file_type == 'yaml':
            helper_cfg = yaml.safe_load(cfg_file)
        elif file_type == 'json':
            helper_cfg = json.load(cfg_file)
        else:
            raise errors.exceptions.InvalidHelperFileTypeError()
    logger.info(f'The helper file {file_path} was imported successfully.')
    return helper_cfg


def _convert_yaml_to_bool(_yaml_bool_value):
    """This function converts the 'yes' and 'no' YAML values to traditional Boolean values."""
    true_values = ['yes', 'true']
    if _yaml_bool_value.lower() in true_values:
        _bool_value = True
    else:
        _bool_value = False
    return _bool_value


def _get_connection_info(_helper_cfg):
    """This function parses any connection information found in the helper file.

    .. versionchanged:: 2.2.0
       Removed one of the preceding underscores in the function name
    """
    _connection_info = {}
    _connection_keys = ['community_url', 'tenant_id', 'default_auth_type']
    for _key in _connection_keys:
        if _key in _helper_cfg['connection']:
            _connection_info[_key] = _helper_cfg['connection'][_key]

    # Parse OAuth 2.0 information if found
    if 'oauth2' in _helper_cfg['connection']:
        _connection_info['oauth2'] = _get_oauth2_info(_helper_cfg)

    # Parse session authentication information if found
    if 'session_auth' in _helper_cfg['connection']:
        _connection_info['session_auth'] = _get_session_auth_info(_helper_cfg)
    return _connection_info


def _get_oauth2_info(_helper_cfg):
    """This function parses OAuth 2.0 information if found in the helper file.

    .. versionchanged:: 2.2.0
       Removed one of the preceding underscores in the function name
    """
    _oauth2 = {}
    _oauth2_keys = ['client_id', 'client_secret', 'redirect_url']
    for _key in _oauth2_keys:
        if _key in _helper_cfg['connection']['oauth2']:
            _oauth2[_key] = _helper_cfg['connection']['oauth2'][_key]
        else:
            _oauth2[_key] = ''
    return _oauth2


def _get_session_auth_info(_helper_cfg):
    """This function parses session authentication information if found in the helper file.

    .. versionchanged:: 2.2.0
       Removed one of the preceding underscores in the function name
    """
    _session_auth = {}
    _session_info = ['username', 'password']
    for _key in _session_info:
        if _key in _helper_cfg['connection']['session_auth']:
            _session_auth[_key] = _helper_cfg['connection']['session_auth'][_key]
        else:
            _session_auth[_key] = None
    return _session_auth


def _get_discussion_styles(_helper_cfg):
    """This function defines (when present in the configuration) the enabled discussion styles in the environment.

    :param _helper_cfg: The configuration parsed from the helper configuration file
    :type _helper_cfg: dict
    :returns: List of enabled discussion styles in the environment
    """
    _discussion_styles = ['blog', 'contest', 'forum', 'idea', 'qanda', 'tkb']
    if 'discussion_styles' in _helper_cfg:
        if isinstance(_helper_cfg.get('discussion_styles'), list):
            _discussion_styles = _helper_cfg.get('discussion_styles')
    return _discussion_styles


def _get_construct_info(_helper_cfg):
    """This function parses settings that can be leveraged in constructing API responses and similar tasks.

    .. versionchanged:: 2.8.0
       The function was refactored to leverage the :py:func:`khoros.utils.helper._collect_values` function.

    .. versionchanged:: 2.2.0
       Removed one of the preceding underscores in the function name

    :param _helper_cfg: The configuration parsed from the helper configuration file
    :type _helper_cfg: dict
    :returns: A dictionary with the key value pair for the ``prefer_json`` key if found in the config file
    """
    _top_level_keys = ['prefer_json']
    return _collect_values(_top_level_keys, _helper_cfg)


def _collect_values(_top_level_keys, _helper_cfg, _helper_dict=None, _ignore_missing=False):
    """This function loops through a list of top-level keys to collect their corresponding values.

    .. versionchanged:: 3.4.0
       This function now supports the ``ssl_verify`` key and defines a default value when not found.

    .. versionadded:: 2.8.0

    :param _top_level_keys: One or more top-level keys that might be found in the helper config file
    :type _top_level_keys: list, tuple, set, str
    :param _helper_cfg: The configuration parsed from the helper configuration file
    :type _helper_cfg: dict
    :param _helper_dict: A predefined dictionary to which the key value pairs should be added
    :type _helper_dict: dict, None
    :param _ignore_missing: Indicates whether or not fields with null values should be ignored (``False`` by default)
    :type _ignore_missing: bool
    :returns: A dictionary with the identified key value pairs
    """
    _helper_dict = {} if not _helper_dict else _helper_dict
    _top_level_keys = (_top_level_keys, ) if isinstance(_top_level_keys, str) else _top_level_keys
    for _key in _top_level_keys:
        if _key in _helper_cfg:
            _key_val = _helper_cfg[_key]
            if _key_val in HelperParsing.yaml_boolean_values:
                _key_val = HelperParsing.yaml_boolean_values.get(_key_val)
            _helper_dict[_key] = _key_val
        elif _key == "ssl_verify":
            # Verify SSL certificates by default unless explicitly set to false
            _helper_dict[_key] = True
        else:
            if not _ignore_missing:
                _helper_dict[_key] = None
    return _helper_dict


def get_helper_settings(file_path, file_type='yaml', defined_settings=None):
    """This function returns a dictionary of the defined helper settings.

    .. versionchanged:: 4.3.0
       Fixed an issue where the ``ssl_verify`` field was being overridden even if defined elsewhere.

    .. versionchanged:: 3.4.0
       This function now supports the ``ssl_verify`` key and defines a default value when not found.

    .. versionchanged:: 2.8.0
       The function was updated to capture the ``translate_errors`` value when defined.

    .. versionchanged:: 2.2.0
       Support was added for JSON-formatted helper configuration files.

    :param file_path: The file path to the helper configuration file
    :type file_path: str
    :param file_type: Defines the helper configuration file as a ``yaml`` file (default) or a ``json`` file
    :type file_type: str
    :param defined_settings: Core object settings (if any) defined via the ``defined_settings`` parameter
    :type defined_settings: dict, None
    :returns: Dictionary of helper variables
    :raises: :py:exc:`khoros.errors.exceptions.InvalidHelperFileTypeError`
    """
    # Initialize the helper_settings dictionary
    helper_settings = {}

    # Convert the defined_settings parameter to an empty dictionary if null
    defined_settings = {} if not defined_settings else defined_settings

    if file_type != 'yaml' and file_type != 'json':
        file_type = get_file_type(file_path)

    # Import the helper configuration file
    helper_cfg = import_helper_file(file_path, file_type)

    # Populate the connection information in the helper dictionary
    if 'connection' in helper_cfg and 'connection' not in defined_settings:
        helper_settings['connection'] = _get_connection_info(helper_cfg)

    # Populate the construct information in the helper dictionary
    helper_settings['construct'] = _get_construct_info(helper_cfg)

    # Populate the enabled discussion styles in the helper dictionary
    helper_settings['discussion_styles'] = _get_discussion_styles(helper_cfg)

    # Populate the SSL certificate verification setting in the helper dictionary
    if 'ssl_verify' not in defined_settings:
        helper_settings.update(_collect_values('ssl_verify', helper_cfg))

    # Populate the error translation setting in the helper dictionary
    helper_settings.update(_collect_values('translate_errors', helper_cfg, _ignore_missing=True))

    # Return the helper_settings dictionary
    return helper_settings


class HelperParsing:
    """This class is used to help parse values imported from a YAML configuration file."""
    # Define dictionary to map YAML Boolean to Python Boolean
    yaml_boolean_values = {
        True: True,
        False: False,
        'yes': True,
        'no': False
    }
