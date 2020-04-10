# -*- coding: utf-8 -*-
"""
:Module:            khoros.core
:Synopsis:          Collection of core functions and tools to work with the Khoros Community APIs
:Usage:             ``import khoros.core`` (Imported by default in primary package)``
:Example:           ``khoros = Khoros(community_url='community.example.com', community_name='mycommunity')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Apr 2020
"""

import sys
import copy
import logging

from . import auth, errors, liql, api
from .objects import base as objects_base
from .objects import users as users_module
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
            self._parse_helper_settings()

        # Add the authentication status
        if 'active' not in self.auth:
            self.auth['active'] = False

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
        self._validate_base_url()
        self._define_url_settings()

        # Populate the khoros.core dictionary with core settings
        self._populate_core_settings()

        # Populate the khoros.auth dictionary with authentication settings
        self._populate_auth_settings()

        # Populate the khoros.construct dictionary with query and syntax constructors
        self._populate_construct_settings()

        # Auto-connect to the environment if specified (default)
        if auto_connect:
            if 'session_auth' in self._settings['auth_type']:
                self._connect_with_session_key()
            else:
                errors.handlers.eprint("Unable to auto-connect to the instance with the given " +
                                       f"'{self._settings['auth_type']}' authentication type.")

        # Import inner object classes so their methods can be called from the primary object
        self.nodes = self._import_node_class()
        self.users = self._import_user_class()

    def _populate_core_settings(self):
        """This method populates the khoros.core dictionary with the core public settings used by the object."""
        _core_settings = ['community_url', 'base_url', 'v1_base', 'v2_base']
        for _setting in _core_settings:
            if _setting in self._settings:
                self.core[_setting] = self._settings[_setting]

    def _populate_auth_settings(self):
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

    def _populate_construct_settings(self):
        """This method populates the khoros.construct dictionary to assist in constructing API queries and responses."""
        assert 'prefer_json' in self._settings
        if 'prefer_json' in self._settings:
            return_formats = {True: '&restapi.response_format=json', False: ''}
            self.construct['response_format'] = return_formats.get(self._settings['prefer_json'])

    def _parse_helper_settings(self):
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

    def _validate_base_url(self):
        """This method ensures that the Community URL is defined appropriately."""
        if ('http://' not in self._settings['community_url']) and ('https://' not in self._settings['community_url']):
            self._settings['community_url'] = f"https://{self._settings['community_url']}"
        if self._settings['community_url'].endswith('/'):
            self._settings['community_url'] = self._settings['community_url'][:-1]

    def _define_url_settings(self):
        """This method defines the URL settings associated with the Khoros environment."""
        if 'community_name' in self._settings and self._settings['use_community_name'] is True:
            self._settings['base_url'] = f"{self._settings['community_url']}/{self._settings['community_name']}"
        else:
            self._settings['base_url'] = self._settings['community_url']
        self._settings['v1_base'] = f"{self._settings['community_url']}/restapi/vc"
        self._settings['v2_base'] = f"{self._settings['base_url']}/api/2.0"

    def _connect_with_session_key(self):
        """This method establishes a connection to the Khoros environment using basic / session key authentication."""
        if ('username' not in self._settings['session_auth']) or ('password' not in self._settings['session_auth']):
            error_msg = f"The username and/or password for session key authentication cannot be found."
            raise errors.exceptions.MissingAuthDataError(error_msg)
        self._settings['session_auth']['session_key'] = auth.get_session_key(self)
        self._settings['auth_header'] = auth.get_session_header(self._settings['session_auth']['session_key'])
        self.auth['session_key'] = self._settings['session_auth']['session_key']
        self.auth['header'] = self._settings['auth_header']
        self.auth['active'] = True

    def _import_node_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Node` inner class to be utilized in the core object."""
        return Khoros.Node(self)

    def _import_user_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.User` inner class to be utilized in the core object."""
        return Khoros.User(self)

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
            self._connect_with_session_key()
        else:
            msg = f"The '{connection_type}' authentication type is currently unsupported."
            raise errors.exceptions.CurrentlyUnsupportedError(msg)

    def query(self, query, return_json=True, pretty_print=False, track_in_lsi=False, always_ok=False,
              error_code='', format_statements=True):
        """This method performs a Community API v2 query using LiQL with the full LiQL syntax.

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
        """This method performs a LiQL query in the Community API v2 by specifying the query elements.

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

    def perform_v1_search(self, endpoint, filter_field, filter_value, return_json=False, fail_on_no_results=False):
        """This function performs a search for a particular field value using a Community API v1 call.

        :param endpoint: The API v1 endpoint against which to perform the search query
        :type endpoint: str
        :param filter_field: The name of the field being queried within the API v1 endpoint
        :type filter_field: str
        :param filter_value: The value associated with the field being queried
        :type filter_value: str, int
        :param return_json: Determines if the response should be returned in JSON format (``False`` by default)
        :type return_json: bool
        :param fail_on_no_results: Raises an exception if no results are returned (``False`` by default)
        :type fail_on_no_results: bool
        :returns: The API response (optionally in JSON format)
        :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
        """
        return api.perform_v1_search(self, endpoint, filter_field, filter_value, return_json, fail_on_no_results)

    class Node(object):
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Node` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        @staticmethod
        def get_node_id(url, node_type=None):
            """This function retrieves the Node ID for a given node within a URL.

            :param url: The URL from which to parse out the Node ID
            :type url: str
            :param node_type: The node type (e.g. ``blog``, ``tkb``, ``message``, etc.) for the object in the URL
            :type node_type: str, NoneType
            :returns: The Node ID retrieved from the URL
            :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
                     :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`,
                     :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
            """
            return objects_base.get_node_id(url, node_type)

        @staticmethod
        def get_node_type_from_url(url):
            """This function attempts to retrieve a node type by analyzing a supplied URL.

            :param url: The URL from which to extract the node type
            :type url: str
            :returns: The node type based on the URL provided
            :raises: :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
            """
            return objects_base.get_node_type_from_url(url)

    class User(object):
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.User` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def create(self, user_settings=None, login=None, email=None, password=None, first_name=None, last_name=None,
                   biography=None, sso_id=None, web_page_url=None, cover_image=None):
            """This function creates a new user in the Khoros Community environment.

            :param user_settings: Allows all user settings to be passed to the function within a single dictionary
            :type user_settings: dict, NoneType
            :param login: The username (i.e. ``login``) for the user (**required**)
            :type login: str, NoneType
            :param email: The email address for the user (**required**)
            :type email: str, NoneType
            :param password: The password for the user
            :type password: str, NoneType
            :param first_name: The user's first name (i.e. given name)
            :type first_name: str, NoneType
            :param last_name: The user's last name (i.e. surname)
            :type last_name: str, NoneType
            :param biography: The user's biography for their profile
            :type biography: str, NoneType
            :param sso_id: The Single Sign-On (SSO) ID for the user
            :type sso_id: str, NoneType
            :param web_page_url: The URL to the user's website
            :type web_page_url: str, NoneType
            :param cover_image: The cover image to be used on the user's profile
            :type cover_image: str, NoneType
            :returns: None
            :raises: :py:exc:`khoros.errors.exceptions.UserCreationError`
            """
            users_module.create(self.khoros_object, user_settings, login, email, password, first_name, last_name,
                                biography, sso_id, web_page_url, cover_image)
            return

        def delete(self, user_id, return_json=False):
            """This function deletes a user from the Khoros Community environment.

            :param user_id: The User ID of the user to be deleted
            :type user_id: str, int
            :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
            :type return_json: bool
            :returns: The API response (optionally in JSON format)
            """
            return users_module.delete(self.khoros_object, user_id, return_json)

        def get_user_id(self, user_settings=None, login=None, email=None, first_name=None, last_name=None,
                        allow_multiple=False, display_warnings=True):
            """This function looks up and retrieves the User ID for a user by leveraging supplied user information.

            .. note:: The priority of supplied fields are as follows: login, email, first and last name,
                      last name, first name

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :param first_name: The first name (i.e. given name) of the user
            :type first_name: str, NoneType
            :param last_name: The last name (i.e. surname) of the user
            :type last_name: str, NoneType
            :param allow_multiple: Allows a list of User IDs to be returned if multiple results are found
            :type allow_multiple: bool
            :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
            :type display_warnings: bool
            :returns: The User ID of the user as an integer or a list of User IDs if ``allow_multiple`` is ``True``
            """
            return users_module.get_user_id(self.khoros_object, user_settings, login, email, first_name, last_name,
                                            allow_multiple, display_warnings)

        def get_username(self, user_settings=None, user_id=None, email=None, first_name=None, last_name=None,
                         allow_multiple=False, display_warnings=True):
            """This function looks up and retrieves the username for a user by leveraging supplied user information.

            .. note:: The priority of supplied fields are as follows: User ID, email, first and last name, last name,
                      first name

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID of the user
            :type user_id: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :param first_name: The first name (i.e. given name) of the user
            :type first_name: str, NoneType
            :param last_name: The last name (i.e. surname) of the user
            :type last_name: str, NoneType
            :param allow_multiple: Allows a list of usernames to be returned if multiple results are found
            :type allow_multiple: bool
            :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
            :type display_warnings: bool
            :returns: The User ID of the user as an integer or a list of User IDs if ``allow_multiple`` is ``True``
            """
            return users_module.get_username(self.khoros_object, user_settings, user_id, email, first_name, last_name,
                                             allow_multiple, display_warnings)

        def get_login(self, user_settings=None, user_id=None, email=None, first_name=None, last_name=None,
                      allow_multiple=False, display_warnings=True):
            """This is an alternative method name for the :py:meth:`khoros.core.Khoros.User.get_username` method."""
            return users_module.get_login(self.khoros_object, user_settings, user_id, email, first_name, last_name,
                                          allow_multiple, display_warnings)

        def get_email(self, user_settings=None, user_id=None, login=None, first_name=None, last_name=None,
                      allow_multiple=False, display_warnings=True):
            """This function retrieves the email address for a user by leveraging supplied user information.

            .. note:: The priority of supplied fields are as follows: User ID, username, first and last name, last name,
                      first name

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID of the user
            :type user_id: str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param first_name: The first name (i.e. given name) of the user
            :type first_name: str, NoneType
            :param last_name: The last name (i.e. surname) of the user
            :type last_name: str, NoneType
            :param allow_multiple: Allows a list of email addresses to be returned if multiple results are found
            :type allow_multiple: bool
            :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
            :type display_warnings: bool
            :returns: The email address of the user as a string or a list of emails if ``allow_multiple`` is ``True``
            """
            return users_module.get_email(self.khoros_object, user_settings, user_id, login, first_name, last_name,
                                          allow_multiple, display_warnings)

        def query_users_table_by_id(self, select_fields, user_id):
            """This function queries the ``users`` table for one or more given SELECT fields for a specific User ID.

            :param select_fields: One or more SELECT field (e.g. ``login``, ``messages.count(*)``, etc.) to query
            :type select_fields: str, tuple, list, set
            :param user_id: The User ID associated with the user
            :type user_id: int, str
            :returns: The API response for the performed LiQL query
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.query_users_table_by_id(self.khoros_object, select_fields, user_id)

        def get_user_data(self, user_settings=None, user_id=None, login=None, email=None):
            """This function retrieves all user data for a given user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: A dictionary containing the user data for the user
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_user_data(self.khoros_object, user_settings, user_id, login, email)

        def get_album_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the number of albums for a user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of albums found for the user as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_album_count(self.khoros_object, user_settings, user_id, login, email)

        def get_followers_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of community members who have added the user as a friend in the community.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of community members who have added the user as a friend in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_followers_count(self.khoros_object, user_settings, user_id, login, email)

        def get_following_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of community members the user has added as a friend in the community.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of community members the user has added as a friend in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_following_count(self.khoros_object, user_settings, user_id, login, email)

        def get_images_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of images uploaded by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of images uploaded by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_images_count(self.khoros_object, user_settings, user_id, login, email)

        def get_public_images_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of public images uploaded by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of public images uploaded by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_public_images_count(self.khoros_object, user_settings, user_id, login, email)

        def get_messages_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of messages (topics and replies) posted by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of messages (topics and replies) posted by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_messages_count(self.khoros_object, user_settings, user_id, login, email)

        def get_roles_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of roles applied to the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of roles applied to the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_roles_count(self.khoros_object, user_settings, user_id, login, email)

        def get_solutions_authored_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of messages created by the user that are marked as accepted solutions.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of messages created by the user that are marked as accepted solutions in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_solutions_authored_count(self.khoros_object, user_settings, user_id, login, email)

        def get_topics_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of topic messages (excluding replies) posted by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of topic messages (excluding replies) posted by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_topics_count(self.khoros_object, user_settings, user_id, login, email)

        def get_replies_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of replies posted by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of replies posted by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_replies_count(self.khoros_object, user_settings, user_id, login, email)

        def get_videos_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of videos uploaded by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of videos uploaded by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_videos_count(self.khoros_object, user_settings, user_id, login, email)

        def get_kudos_given_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of kudos a user has given.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of kudos given by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_kudos_given_count(self.khoros_object, user_settings, user_id, login, email)

        def get_kudos_received_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This function gets the count of kudos a user has received.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The number of kudos received by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_kudos_received_count(self.khoros_object, user_settings, user_id, login, email)

        def get_online_user_count(self):
            """This function retrieves the number of users currently online.

            :returns: The user count for online users as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_online_user_count(self.khoros_object)

        def get_registration_data(self, user_settings=None, user_id=None, login=None, email=None):
            """This function retrieves the registration data for a given user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: A dictionary containing the registration data for the user
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_registration_data(self.khoros_object, user_settings, user_id, login, email)

        def get_registration_timestamp(self, user_settings=None, user_id=None, login=None, email=None):
            """This function retrieves the timestamp for when a given user registered for an account.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The registration timestamp in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_registration_timestamp(self.khoros_object, user_settings, user_id, login, email)

        def get_registration_status(self, user_settings=None, user_id=None, login=None, email=None):
            """This function retrieves the registration status for a given user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The registration status in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_registration_status(self.khoros_object, user_settings, user_id, login, email)

        def get_last_visit_timestamp(self, user_settings=None, user_id=None, login=None, email=None):
            """This function retrieves the timestamp for the last time the user logged into the community.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, NoneType
            :param user_id: The User ID associated with the user
            :type user_id: int, str, NoneType
            :param login: The username of the user
            :type login: str, NoneType
            :param email: The email address of the user
            :type email: str, NoneType
            :returns: The last visit timestamp in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return users_module.get_last_visit_timestamp(self.khoros_object, user_settings, user_id, login, email)

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

