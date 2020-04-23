# -*- coding: utf-8 -*-
"""
:Module:            khoros.core
:Synopsis:          Collection of core functions and tools to work with the Khoros Community APIs
:Usage:             ``import khoros.core`` (Imported by default in primary package)``
:Example:           ``khoros = Khoros(community_url='community.example.com', community_name='mycommunity')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Apr 2020
"""

import sys
import copy
import logging

from . import auth, errors, liql, api
from . import objects as objects_module
from . import structures as structures_module
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
        self.categories = self._import_category_class()
        self.communities = self._import_community_class()
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

    def _import_category_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Category` inner class to be utilized in the
        core object."""
        return Khoros.Category(self)

    def _import_community_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Community` inner class to be utilized in the
        core object."""
        return Khoros.Community(self)

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
        response = liql.perform_query(self, query_url, return_json=return_json)
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

    def get_total_count(self, collection, where_filter="", verify_success=True):
        """This function retrieves the total asset count from a given collection (e.g. ``categories``).

        :param collection: The collection object to use in the FROM clause of the LiQL query (e.g. ``users``)
        :type collection: str
        :param where_filter: An optional filter to use as the WHERE clause in the LiQL query
        :type where_filter: str
        :param verify_success: Determines if the API query should be verified as successful (``True`` by default)
        :type verify_success: bool
        :returns: The total count as an integer
        :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
        """
        return liql.get_total_count(self, collection, where_filter, verify_success)

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

    class Category(object):
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Category` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        @staticmethod
        def get_category_id(url):
            """This function retrieves the Category ID for a given category when provided its URL.

            :param url: The URL from which to parse out the Category ID
            :type url: str
            :returns: The Category ID retrieved from the URL
            :raises: :py:exc:`khoros.errors.exceptions.InvalidURLError`
            """
            return structures_module.categories.get_category_id(url)

        def get_total_category_count(self):
            """This function returns the total number of categories within the Khoros Community environment.

            :returns: The total number of categories as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.categories.get_total_category_count(self.khoros_object)

        def get_category_details(self, identifier, first_item=True):
            """This function returns a dictionary of community configuration settings.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str
            :param first_item: Filters the response data to the first item returned (``True`` by default)
            :type first_item: bool
            :returns: The community details within a dictionary
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_category_details(self.khoros_object, identifier, first_item)

        def get_category_field(self, field, identifier=None, category_details=None):
            """This function returns a specific community field from the Khoros Community API.

            .. versionadded:: 2.1.0

            :param field: The field whose value to return from the :py:class:`khoros.structures.base.Mapping` class
            :type field: str
            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type category_details: dict, NoneType
            :returns: The requested field in its native format
            :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_category_field(self.khoros_object, field, identifier,
                                                                   category_details)

        def get_url(self, category_id=None, category_details=None):
            """This function retrieves the URL of a given category.

            .. versionadded:: 2.1.0

            :param category_id: The ID of the category to be evaluated (optional if ``category_details`` provided)
            :type category_id: str, NoneType
            :param category_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type category_details: dict, NoneType
            :returns: The full URL of the category
            :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_url(self.khoros_object, category_id, category_details)

        def get_title(self, identifier=None, full_title=True, short_title=False, category_details=None):
            """This function retrieves the full and/or short title of the category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param full_title: Return the full title of the environment (``True`` by default)
            :type full_title: bool
            :param short_title: Return the short title of the environment (``False`` by default)
            :type short_title: bool
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The title(s) of the environment as a string or a tuple of strings
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_title(self.khoros_object, identifier, full_title, short_title,
                                                          category_details)

        def get_description(self, identifier=None, category_details=None):
            """This function retrieves the description for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The description in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_description(self.khoros_object, identifier, category_details)

        def get_parent_type(self, identifier=None, category_details=None):
            """This function retrieves the parent type for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The parent type in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_parent_type(self.khoros_object, identifier, category_details)

        def get_parent_id(self, identifier=None, category_details=None):
            """This function retrieves the parent ID for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The parent ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_parent_id(self.khoros_object, identifier, category_details)

        def get_parent_url(self, identifier=None, category_details=None):
            """This function retrieves the parent URL for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The parent URL in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_parent_url(self.khoros_object, identifier, category_details)

        def get_root_type(self, identifier=None, category_details=None):
            """This function retrieves the root category type for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The root category type in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_root_type(self.khoros_object, identifier, category_details)

        def get_root_id(self, identifier=None, category_details=None):
            """This function retrieves the root category ID for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The root category ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_root_id(self.khoros_object, identifier, category_details)

        def get_root_url(self, identifier=None, category_details=None):
            """This function retrieves the root category URL for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The root category URL in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_root_url(self.khoros_object, identifier, category_details)

        def get_language(self, identifier=None, category_details=None):
            """This function retrieves the defined language for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The language (e.g. ``en``) in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_language(self.khoros_object, identifier, category_details)

        def is_hidden(self, identifier=None, category_details=None):
            """This function identifies whether or not a given category is hidden.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: Boolean value indicating if the category is hidden
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.is_hidden(self.khoros_object, identifier, category_details)

        def get_views(self, identifier=None, category_details=None):
            """This function retrieves the total view count for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The total number of views
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_views(self.khoros_object, identifier, category_details)

        def friendly_date_enabled(self, identifier=None, category_details=None):
            """This function identifies if friendly dates are enabled for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: Boolean indicating if friendly dates are enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.friendly_date_enabled(self.khoros_object, identifier, category_details)

        def get_friendly_date_max_age(self, identifier=None, category_details=None):
            """This function retrieves the maximum age where friendly dates should be used (if enabled) for a category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: Integer representing the number of days the friendly date feature should be leveraged if enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_friendly_date_max_age(self, identifier, category_details)

        def get_active_skin(self, identifier=None, category_details=None):
            """This function retrieves the skin being used with a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The name of the active skin in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_active_skin(self.khoros_object, identifier, category_details)

        def get_depth(self, identifier=None, category_details=None):
            """This function retrieves the depth of a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The depth of the category as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_depth(self.khoros_object, identifier, category_details)

        def get_position(self, identifier=None, category_details=None):
            """This function retrieves the position of a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The position of the category as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_position(self.khoros_object, identifier, category_details)

        def get_creation_date(self, identifier=None, category_details=None):
            """This function retrieves the creation date of a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, NoneType
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, NoneType
            :returns: The creation of the category in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Allow a format to be specified and the ability to parse as a datetime object if needed
            return structures_module.categories.get_creation_date(self.khoros_object, identifier, category_details)

    class Community(object):
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Community` inner class object.

            .. versionadded:: 2.1.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object
        
        def get_community_details(self):
            """This function returns a dictionary of community configuration settings.

            .. versionadded:: 2.1.0

            :returns: The community details within a dictionary
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_community_details(self.khoros_object)

        def get_community_field(self, field, community_details=None):
            """This function retrieves a particular field from the community collection in the API.

            .. versionadded:: 2.1.0

            :param field: The field whose value to return from the :py:class:`khoros.structures.base.Mapping` class
            :type field: str
            :param community_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type community_details: dict, NoneType
            :returns: The requested field in its native format
            :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.communities.get_community_field(self.khoros_object, field, community_details)

        def get_tenant_id(self, community_details=None):
            """This function retrieves the tenant ID of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The tenant ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_tenant_id(self.khoros_object, community_details)

        def get_title(self, full_title=True, short_title=False, community_details=None):
            """This function retrieves the full and/or short title of the environment.

            .. versionadded:: 2.1.0

            :param full_title: Return the full title of the environment (``True`` by default)
            :type full_title: bool
            :param short_title: Return the short title of the environment (``False`` by default)
            :type short_title: bool
            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The title(s) of the environment as a string or a tuple of strings
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_title(self.khoros_object, full_title, short_title,
                                                           community_details)

        def get_description(self, community_details=None):
            """This function retrieves the description of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The description in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_description(self.khoros_object, community_details)

        def get_primary_url(self, community_details=None):
            """This function retrieves the primary URL of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The primary URL in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_primary_url(self.khoros_object, community_details)

        def get_max_attachments(self, community_details=None):
            """This function retrieves the maximum number of attachments permitted per message within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The value as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_max_attachments(self.khoros_object, community_details)

        def get_permitted_attachment_types(self, community_details=None):
            """This function retrieves the attachment file types permitted within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The permitted file types within a list
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_permitted_attachment_types(self.khoros_object, community_details)

        def email_confirmation_required_to_post(self, community_details=None):
            """This function identifies if an email configuration is required before posting in the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: Boolean value indicating if email configuration is required before posting
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.email_confirmation_required_to_post(self.khoros_object, community_details)

        def get_language(self, community_details=None):
            """This function retrieves the language (e.g. ``en``) utilized in the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The language code as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_language(self.khoros_object, community_details)

        def get_ooyala_player_branding_id(self, community_details=None):
            """This function retrieves the branding ID for the Ooyala Player utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The branding ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_ooyala_player_branding_id(self.khoros_object, community_details)

        def get_date_pattern(self, community_details=None):
            """This function retrieves the date pattern (e.g. ``yyyy-MM-dd``) utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The date pattern in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_date_pattern(self.khoros_object, community_details)

        def friendly_date_enabled(self, community_details=None):
            """This function if the friendly date functionality is utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: Boolean value indicating if the feature is enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.friendly_date_enabled(self.khoros_object, community_details)

        def get_friendly_date_max_age(self, community_details=None):
            """This function identifies if the friendly date functionality is utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: Boolean value indicating if the feature is enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_friendly_date_max_age(self.khoros_object, community_details)

        def get_active_skin(self, community_details=None):
            """This function retrieves the primary active skin that is utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The skin name as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_active_skin(self.khoros_object, community_details)

        def get_sign_out_url(self, community_details=None):
            """This function retrieves the Sign Out URL for the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The Sign Out URL as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_sign_out_url(self.khoros_object, community_details)

        def get_creation_date(self, community_details=None):
            """This function retrieves the timestamp for the initial creation of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: The creation date as a string (e.g. ``2020-02-03T22:41:36.408-08:00``)
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            # TODO: Allow a format to be specified and the ability to parse as a datetime object if needed
            return structures_module.communities.get_creation_date(self.khoros_object, community_details)

        def top_level_categories_enabled(self, community_details=None):
            """This function identifies if top level categories are enabled within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: Boolean value indicating if top level categories are enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.top_level_categories_enabled(self.khoros_object, community_details)

        def show_community_node_in_breadcrumb(self, community_details=None):
            """This function identifies if the community node should be shown in breadcrumbs.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: Boolean value indicating if the community node is displayed in bredcrumbs
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.show_community_node_in_breadcrumb(self.khoros_object,
                                                                                   community_details)

        def show_breadcrumb_at_top_level(self, community_details=None):
            """This function identifies if breadcrumbs should be shown at the top level of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: Boolean value indicating if breadcrumbs are displayed at the top level of the environment
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.show_breadcrumb_at_top_level(self.khoros_object, community_details)

        def top_level_categories_on_community_page(self, community_details=None):
            """This function identifies if top level categories are enabled on community pages.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, NoneType
            :returns: Boolean value indicating if top level categories are enabled on community pages
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.top_level_categories_on_community_page(self.khoros_object,
                                                                                        community_details)
    
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
            return structures_module.nodes.get_node_id(url, node_type)

        @staticmethod
        def get_node_type_from_url(url):
            """This function attempts to retrieve a node type by analyzing a supplied URL.

            :param url: The URL from which to extract the node type
            :type url: str
            :returns: The node type based on the URL provided
            :raises: :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
            """
            return structures_module.nodes.get_node_type_from_url(url)

        def get_total_node_count(self):
            """This function returns the total number of nodes within the Khoros Community environment.

            :returns: The total number of nodes as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.nodes.get_total_node_count(self.khoros_object)

        def get_node_details(self, identifier, first_item=True):
            """This function returns a dictionary of node configuration settings.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str
            :param first_item: Filters the response data to the first item returned (``True`` by default)
            :type first_item: bool
            :returns: The node details within a dictionary
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_node_details(self.khoros_object, identifier, first_item)

        def get_node_field(self, field, identifier=None, node_details=None):
            """This function returns a specific node field from the Khoros Community API.

            .. versionadded:: 2.1.0

            :param field: The field to return from the :py:class:`khoros.structures.base.Mapping` class
            :type field: str
            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The requested field in its native format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_node_field(self.khoros_object, field, identifier, node_details)

        def get_url(self, node_id=None, node_details=None):
            """This function returns the full URL of a given Node ID.

            .. versionadded:: 2.1.0

            :param node_id: The Node ID with which to identify the node
            :type node_id: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The node URl as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_url(self.khoros_object, node_id, node_details)

        def get_type(self, identifier, node_details=None):
            """This function returns the full URL of a given Node ID.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The node URl as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_type(self.khoros_object, identifier, node_details)

        def get_discussion_style(self, identifier, node_details=None):
            """This function returns the full URL of a given Node ID.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The node URl as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_discussion_style(self.khoros_object, identifier, node_details)

        def get_title(self, identifier=None, full_title=True, short_title=False, node_details=None):
            """This function retrieves the full and/or short title of the node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param full_title: Determines if the full title of the node should be returned (``True`` by default)
            :type full_title: bool
            :param short_title: Determines if the short title of the node should be returned (``False`` by default)
            :type short_title: bool
            :param node_details: Dictionary containing node details (optional)
            :type node_details: dict, NoneType
            :returns: The node title(s) as a string or a tuple of strings
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_title(self.khoros_object, identifier, full_title,
                                                     short_title, node_details)

        def get_description(self, identifier, node_details=None):
            """This function returns the description of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The node description as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_description(self.khoros_object, identifier, node_details)

        def get_parent_type(self, identifier, node_details=None):
            """This function returns the parent type of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The parent type as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_parent_type(self.khoros_object, identifier, node_details)

        def get_parent_id(self, identifier, node_details=None, include_prefix=False):
            """This function returns the Parent ID of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :param include_prefix: Determines if the prefix (e.g. ``category:``) should be included (Default: ``False``)
            :type include_prefix: bool
            :returns: The Parent ID as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_parent_id(self.khoros_object, identifier, node_details, include_prefix)

        def get_parent_url(self, identifier, node_details=None):
            """This function returns the parent URL of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The parent URL as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_parent_url(self.khoros_object, identifier, node_details)

        def get_root_type(self, identifier, node_details=None):
            """This function returns the root category type of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The root category type as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_root_type(self.khoros_object, identifier, node_details)

        def get_root_id(self, identifier, node_details=None, include_prefix=False):
            """This function returns the Root Category ID of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :param include_prefix: Determines if the prefix (e.g. ``category:``) should be included (``False`` by default)
            :type include_prefix: bool
            :returns: The Root Category ID as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_root_id(self.khoros_object, identifier, node_details, include_prefix)

        def get_root_url(self, identifier, node_details=None):
            """This function returns the root category URL of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The root category URL as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_root_url(self.khoros_object, identifier, node_details)

        def get_avatar_url(self, identifier, node_details=None, original=True, tiny=False, small=False,
                           medium=False, large=False):
            """This function retrieves one or more avatar URLs for a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :param original: Indicates if the URL for the original-size image should be returned (``True`` by default)
            :type original: bool
            :param tiny: Indicates if the URL for the image in a tiny size should be returned (``False`` by default)
            :type tiny: bool
            :param small: Indicates if the URL for the image in a small size should be returned (``False`` by default)
            :type small: bool
            :param medium: Indicates if the URL for the image in a medium size should be returned (``False`` by default)
            :type medium: bool
            :param large: Indicates if the URL for the image in a large size should be returned (``False`` by default)
            :type large: bool
            :returns: A single URL as a string (default) or a dictionary of multiple URLs by size
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_avatar_url(self.khoros_object, identifier, node_details,
                                                          original, tiny, small, medium, large)

        def get_creation_date(self, identifier, node_details=None, friendly=False):
            """This function returns the creation date of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :param friendly: Determines whether to return the "friendly" date (e.g. ``Friday``) instead (``False`` by default)
            :type friendly: bool
            :returns: The creation date as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_creation_date(self.khoros_object, identifier, node_details, friendly)

        def get_depth(self, identifier, node_details=None):
            """This function returns the depth of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The depth as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_depth(self.khoros_object, identifier, node_details)

        def get_position(self, identifier, node_details=None):
            """This function returns the position of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The position as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_position(self.khoros_object, identifier, node_details)

        def is_hidden(self, identifier, node_details=None):
            """This function identifies whether or not a given node is hidden.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: Boolean indicating whether or not the node is hidden
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.is_hidden(self.khoros_object, identifier, node_details)

        def get_views(self, identifier, node_details=None):
            """This function returns the views for a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, NoneType
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, NoneType
            :returns: The views as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_views(self.khoros_object, identifier, node_details)

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
            objects_module.users.create(self.khoros_object, user_settings, login, email, password, first_name,
                                        last_name, biography, sso_id, web_page_url, cover_image)
            return

        def delete(self, user_id, return_json=False):
            """This function deletes a user from the Khoros Community environment.

            :param user_id: The User ID of the user to be deleted
            :type user_id: str, int
            :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
            :type return_json: bool
            :returns: The API response (optionally in JSON format)
            """
            return objects_module.users.delete(self.khoros_object, user_id, return_json)

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
            return objects_module.users.get_user_id(self.khoros_object, user_settings, login, email, first_name,
                                                    last_name, allow_multiple, display_warnings)

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
            return objects_module.users.get_username(self.khoros_object, user_settings, user_id, email, first_name,
                                                     last_name, allow_multiple, display_warnings)

        def get_login(self, user_settings=None, user_id=None, email=None, first_name=None, last_name=None,
                      allow_multiple=False, display_warnings=True):
            """This is an alternative method name for the :py:meth:`khoros.core.Khoros.User.get_username` method."""
            return objects_module.users.get_login(self.khoros_object, user_settings, user_id, email, first_name,
                                                  last_name, allow_multiple, display_warnings)

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
            return objects_module.users.get_email(self.khoros_object, user_settings, user_id, login, first_name,
                                                  last_name, allow_multiple, display_warnings)

        def query_users_table_by_id(self, select_fields, user_id):
            """This function queries the ``users`` table for one or more given SELECT fields for a specific User ID.

            :param select_fields: One or more SELECT field (e.g. ``login``, ``messages.count(*)``, etc.) to query
            :type select_fields: str, tuple, list, set
            :param user_id: The User ID associated with the user
            :type user_id: int, str
            :returns: The API response for the performed LiQL query
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.query_users_table_by_id(self.khoros_object, select_fields, user_id)

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
            return objects_module.users.get_user_data(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_album_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_followers_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_following_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_images_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_public_images_count(self.khoros_object, user_settings, user_id,
                                                                login, email)

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
            return objects_module.users.get_messages_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_roles_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_solutions_authored_count(self.khoros_object, user_settings, user_id,
                                                                     login, email)

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
            return objects_module.users.get_topics_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_replies_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_videos_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_kudos_given_count(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_kudos_received_count(self.khoros_object, user_settings, user_id,
                                                                 login, email)

        def get_online_user_count(self):
            """This function retrieves the number of users currently online.

            :returns: The user count for online users as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_online_user_count(self.khoros_object)

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
            return objects_module.users.get_registration_data(self.khoros_object, user_settings, user_id, login, email)

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
            return objects_module.users.get_registration_timestamp(self.khoros_object, user_settings, user_id,
                                                                   login, email)

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
            return objects_module.users.get_registration_status(self.khoros_object, user_settings, user_id,
                                                                login, email)

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
            return objects_module.users.get_last_visit_timestamp(self.khoros_object, user_settings, user_id,
                                                                 login, email)

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
