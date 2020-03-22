# -*- coding: utf-8 -*-
"""
:Module:            khoros.core
:Synopsis:          Collection of core functions and tools to work with the Khoros Community APIs
:Usage:             ``import khoros.core`` (Imported by default in primary package)``
:Example:           ``khoros = Khoros(community_url='community.example.com', community_name='mycommunity')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Mar 2020
"""

import sys
import copy
import logging

from . import auth, errors, liql
from .utils.helper import get_helper_settings

# Initialize logging
logging.getLogger("khoros").addHandler(logging.NullHandler())


class Khoros(object):
    """This is the class for the core object leveraged in this library."""
    # Define default configuration information
    DEFAULT_SETTINGS = {
        'community_url': 'https://community.khoros.com',
        'tenant_id': 'lithosphere',
        'use_community_name': False
    }
    DEFAULT_AUTH = {
        'auth_type': 'session_auth'
    }

    # Define the function that initializes the object instance
    def __init__(self, settings=None, community_url=None, tenant_id=None, community_name=None, auth_type=None,
                 session_auth=None, oauth2=None, sso=None, helper=None, auto_connect=True, use_community_name=False,
                 prefer_json=True):
        """This method initializes the Khoros object.

        :param settings: Predefined settings that the object should use
        :type settings: dict, NoneType
        :param community_url: The base URL of the Khoros community instance (e.g. ``community.khoros.com``)
        :type community_url: str, NoneType
        :param tenant_id: The tenant ID for the Khoros community instance (e.g. ``lithosphere``)
        :type tenant_id: str, NoneType
        :param community_name: The community name (e.g. ``community-name``) for the Khoros community instance
        :type community_name: str, NoneType
        :param auth_type: The authentication type to use when connecting to the instance (``session_auth`` by default)
        :type auth_type: str, NoneType
        :param session_auth: The ``username`` and ``password`` values for session key authentication
        :type session_auth: dict, NoneType
        :param oauth2: The ``client_id``, ``client_secret`` and ``redirect_url`` values for OAuth 2.0 authentication
        :type oauth2: dict, NoneType
        :param sso: The values for single sign-on (SSO) authentication
        :type sso: dict, NoneType
        :param helper: The path (and optional file type) to the YAML or JSON helper configuration file
        :type helper: str, tuple, list, dict, NoneType
        :param auto_connect: Determines if a connection should be established when initialized (``True`` by default)
        :type auto_connect: bool
        :param use_community_name: Defines if the community name should be used in the API URLs (``False`` by default)
        :type use_community_name: bool
        :param prefer_json: Defines preference that API responses be returned in JSON format (``True`` by default)
        :type prefer_json: bool
        """
        # Initialize the dictionaries if not passed to the class
        if settings is None:
            settings = {}
        
        # Initialize other dictionaries that will be used by the class object
        self.auth = {}
        self.core = {}
        self.construct = {}

        # Add supplied elements to the settings dictionary
        _individual_arguments = {
            'community_url': community_url,
            'community_name': community_name,
            'tenant_id': tenant_id,
            'auth_type': auth_type,
            'session_auth': session_auth,
            'oauth2': oauth2,
            'sso': sso,
            'auto_connect': auto_connect,
            'use_community_name': use_community_name,
            'prefer_json': prefer_json
        }
        for _arg_key, _arg_val in _individual_arguments.items():
            if _arg_val:
                settings[_arg_key] = _arg_val

        # Creates the private _settings attribute using the default settings as a base
        self._settings = copy.copy(Khoros.DEFAULT_SETTINGS)
        self._settings.update(Khoros.DEFAULT_AUTH)
        self._settings.update(settings)

        # Capture the helper settings if applicable
        if helper is not None:
            self._settings['helper'] = helper
            if type(helper) == tuple or type(helper) == list:
                file_path, file_type = helper
            elif type(helper) == str:
                file_path, file_type = (helper, 'yaml')
            elif type(helper) == dict:
                file_path, file_type = helper.values()
            else:
                raise TypeError("The 'helper' argument can only be supplied as tuple, string, list or dict.")
            self._helper_settings = get_helper_settings(file_path, file_type)

            # Parse the helper settings
            self.__parse_helper_settings()

        # Add the authentication status
        if 'active' not in self.auth:
            auth['active'] = False

        # Update the default authentication type if necessary
        self.auth['type'] = self._settings['auth_type']
        if auth_type is not None:
            accepted_auth_types = ['session_auth', 'oauth2', 'sso']
            auth_map = {
                'session_auth': session_auth,
                'oauth2': oauth2,
                'sso': sso
            }
            if str(auth_type) in accepted_auth_types:
                self._settings['auth_type'] = auth_type
                self.auth['type'] = auth_type
                if auth_map.get(auth_type) is None and auth_type not in self._helper_settings['connection']:
                    error_msg = f"The '{auth_type}' authentication type was specified but no associated data was found."
                    raise errors.exceptions.MissingAuthDataError(error_msg)
            else:
                error_msg = f"'{auth_type}' is an invalid authentication type. Reverting to default. ('session_auth')"
                errors.handlers.eprint(error_msg)
                self._settings.update(Khoros.DEFAULT_AUTH)
                self.auth['type'] = self._settings['auth_type']
        elif sso is not None:
            self._settings['auth_type'] = 'sso'
            self.auth['type'] = self._settings['auth_type']
        elif oauth2 is not None:
            self._settings['auth_type'] = 'oauth2'
            self.auth['type'] = self._settings['auth_type']
        else:
            if session_auth is not None:
                self._settings['auth_type'] = 'session_auth'
            elif 'session_auth' not in self._helper_settings['connection']:
                error_msg = f"No data was found for the default '{auth_type}' authentication type."
                raise errors.exceptions.MissingAuthDataError(error_msg)

        # Capture the version information
        self.sys_version_info = tuple([i for i in sys.version_info])

        # Establish logging
        self.logging = logging

        # Validate the settings
        self.__validate_base_url()
        self.__define_url_settings()

        # Populate the khoros.core dictionary with core settings
        self.__populate_core_settings()

        # Populate the khoros.auth dictionary with authentication settings
        self.__populate_auth_settings()

        # Populate the khoros.construct dictionary with query and syntax constructors
        self.__populate_construct_settings()

        # Auto-connect to the environment if specified (default)
        if auto_connect:
            if 'session_auth' in self._settings['auth_type']:
                self.__connect_with_session_key()
            else:
                errors.handlers.eprint("Unable to auto-connect to the instance with the given " +
                                       f"'{self._settings['auth_type']}' authentication type.")

    def __populate_core_settings(self):
        """This method populates the khoros.core dictionary with the core public settings used by the object."""
        _core_settings = ['community_url', 'base_url', 'v1_base', 'v2_base']
        for _setting in _core_settings:
            if _setting in self._settings:
                self.core[_setting] = self._settings[_setting]

    def __populate_auth_settings(self):
        """This method populates the khoros.auth dictionary to be leveraged in authentication/authorization tasks."""
        _auth_settings = ['auth_type', 'oauth2', 'session_auth', 'sso']
        _setting_keys = {
            'oauth2': ['client_id', 'client_secret', 'redirect_url'],
            'sso': ['sso_token']
        }
        for _setting in _auth_settings:
            if _setting in self._settings:
                if _setting in _setting_keys:
                    for _setting_key in _setting_keys.get(_setting):
                        if _setting_key in self._settings[_setting]:
                            self.auth[_setting_key] = self._settings[_setting][_setting_key]

    def __populate_construct_settings(self):
        """This method populates the khoros.construct dictionary to assist in constructing API queries and responses."""
        assert 'prefer_json' in self._settings
        if 'prefer_json' in self._settings:
            return_formats = {True: '&restapi.response_format=json', False: ''}
            self.construct['response_format'] = return_formats.get(self._settings['prefer_json'])

    def __parse_helper_settings(self):
        """This method parses the settings in the helper configuration file when provided."""
        # Parse the helper settings and add them to the primary settings
        if 'connection' in self._helper_settings:
            _helper_keys = ['connection', 'construct']
            _auth_keys = ['oauth2', 'session_auth', 'sso']
            for _helper_key in _helper_keys:
                if _helper_key == 'connection':
                    _connection_keys = ['community_url', 'tenant_id', 'default_auth_type', 'oauth2',
                                        'session_auth', 'sso']
                    for _connection_key in _connection_keys:
                        if _connection_key in self._helper_settings['connection']:
                            _new_key = 'auth_type' if _connection_key == 'default_auth_type' else _connection_key
                            self._settings[_new_key] = self._helper_settings['connection'][_connection_key]
                elif _helper_key == 'construct':
                    _construct_keys = ['prefer_json']
                    for _construct_key in _construct_keys:
                        if _construct_key in self._helper_settings['construct']:
                            self._settings[_construct_key] = self._helper_settings['construct'][_construct_key]

    def __validate_base_url(self):
        """This method ensures that the Community URL is defined appropriately."""
        if ('http://' not in self._settings['community_url']) and ('https://' not in self._settings['community_url']):
            self._settings['community_url'] = f"https://{self._settings['community_url']}"
        if self._settings['community_url'].endswith('/'):
            self._settings['community_url'] = self._settings['community_url'][:-1]

    def __define_url_settings(self):
        """This method defines the URL settings associated with the Khoros environment."""
        if 'community_name' in self._settings and self._settings['use_community_name'] is True:
            self._settings['base_url'] = f"{self._settings['community_url']}/{self._settings['community_name']}"
        else:
            self._settings['base_url'] = self._settings['community_url']
        self._settings['v1_base'] = f"{self._settings['community_url']}/restapi/vc"
        self._settings['v2_base'] = f"{self._settings['base_url']}/api/2.0"

    def __connect_with_session_key(self):
        """This method establishes a connection to the Khoros environment using basic / session key authentication."""
        if ('username' not in self._settings['session_auth']) or ('password' not in self._settings['session_auth']):
            error_msg = f"The username and/or password for session key authentication cannot be found."
            raise errors.exceptions.MissingAuthDataError(error_msg)
        self._settings['session_auth']['session_key'] = auth.get_session_key(self)
        self._settings['auth_header'] = auth.get_session_header(self._settings['session_auth']['session_key'])
        self.auth['session_key'] = self._settings['session_auth']['session_key']
        self.auth['header'] = self._settings['auth_header']
        self.auth['active'] = True

    # The public functions below provide ways to interact with the Khoros object
    def connect(self, connection_type=None):
        """This method establishes a connection to the environment using a specified authentication type.

        :param connection_type: The type of authentication method (e.g. ``session_auth``)
        :type connection_type: str
        :returns: None
        """
        if connection_type is None:
            connection_type = self._settings['auth_type']
        if connection_type == 'session_auth':
            self.__connect_with_session_key()
        else:
            msg = f"The '{connection_type}' authentication type is currently unsupported."
            raise errors.exceptions.CurrentlyUnsupportedError(msg)

    def query(self, query, return_json=True, pretty_print=False, track_in_lsi=False, always_ok=False,
              error_code='', format_statements=True):
        """This function performs a Community API v2 query using LiQL with the full LiQL syntax.

        :param query: The full LiQL query in its standard syntax (not URL-encoded)
        :type query: str
        :param return_json: Determines if the API response should be returned in JSON format (``True`` by default)
        :type return_json: bool
        :param pretty_print: Defines if the response should be "pretty printed" (``False`` by default)
        :type pretty_print: bool
        :param track_in_lsi: Defines if the query should be tracked within LSI (``False`` by default)
        :type track_in_lsi: bool
        :param always_ok: Defines if the HTTP response should **always** be ``200 OK`` (``False`` by default)
        :type always_ok: bool
        :param error_code: Allows an error code to optionally be supplied for testing purposes (ignored by default)
        :type error_code: str
        :param format_statements: Determines if statements (e.g. ``SELECT``, ``FROM``, et.) should be formatted to be in
                                  all caps (``True`` by default)
        :type format_statements: bool
        :returns: The query response from the API in JSON format (unless defined otherwise)
        :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
        """
        query_url = liql.get_query_url(self.core, query, pretty_print, track_in_lsi, always_ok,
                                       error_code, format_statements)
        response = liql.perform_query(self, query_url, return_json)
        return response

    def search(self, select_fields, from_source, where_filter="", order_by=None, order_desc=True, limit=0,
               return_json=True, pretty_print=False, track_in_lsi=False, always_ok=False, error_code='',
               format_statements=True):
        """This function performs a LiQL query in the Community API v2 by specifying the query elements.

        :param select_fields: One or more fields to be selected within the SELECT statement (e.g. ``id``)
        :type select_fields: str, tuple, list, set
        :param from_source: The source of the data to use in the FROM statement (e.g. ``messages``)
        :type from_source: str
        :param where_filter: The filters (if any) to use in the WHERE clause (e.g. ``id = '2'``)
        :type where_filter: str, tuple, list, dict, set
        :param order_by: The field(s) by which to order the response data (optional)
        :type order_by: str, tuple, set, dict, list
        :param order_desc: Defines if the ORDER BY directionality is DESC (default) or ASC
        :type order_desc: bool
        :param limit: Allows an optional limit to be placed on the response items (ignored by default)
        :type limit: int
        :param return_json: Determines if the API response should be returned in JSON format (``True`` by default)
        :type return_json: bool
        :param pretty_print: Defines if the response should be "pretty printed" (``False`` by default)
        :type pretty_print: bool
        :param track_in_lsi: Defines if the query should be tracked within LSI (``False`` by default)
        :type track_in_lsi: bool
        :param always_ok: Defines if the HTTP response should **always** be ``200 OK`` (``False`` by default)
        :type always_ok: bool
        :param error_code: Allows an error code to optionally be supplied for testing purposes (ignored by default)
        :type error_code: str
        :param format_statements: Determines if statements (e.g. ``SELECT``, ``FROM``, et.) should be formatted to be in
                                  all caps (``True`` by default)
        :type format_statements: bool
        :returns: The query response from the API in JSON format (unless defined otherwise)
        :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
                 :py:exc:`khoros.errors.exceptions.OperatorMismatchError`,
                 :py:exc:`khoros.errors.exceptions.InvalidOperatorError`
        """
        query = liql.parse_query_elements(select_fields, from_source, where_filter, order_by, order_desc, limit)
        response = self.query(query, return_json, pretty_print, track_in_lsi, always_ok, error_code, format_statements)
        return response

    def signout(self):
        """This method invalidates the active session key or SSO authentication session."""
        session_terminated = auth.invalidate_session(self)
        if session_terminated:
            self.auth['active'] = False
        return

    def __del__(self):
        """This method fully destroys the instance."""
        self.close()

    def close(self):
        """This core method destroys the instance."""
        pass
