# -*- coding: utf-8 -*-
"""
:Module:            khoros.core
:Synopsis:          Collection of core functions and tools to work with the Khoros Community APIs
:Usage:             ``import khoros.core`` *(Imported by default in primary package)*
:Example:           ``khoros = Khoros(helper='helper.yml')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     13 Nov 2021
"""

import sys
import copy
import logging
import warnings

from . import auth, errors, liql, api
from . import saml as saml_module
from . import studio as studio_module
from . import objects as objects_module
from . import structures as structures_module
from .utils import environment, log_utils, version
from .utils.helper import get_helper_settings

# Initialize logging
logger = log_utils.initialize_logging(__name__)


# noinspection PyUnresolvedReferences,PyTypeChecker
class Khoros(object):
    """This is the class for the core object leveraged in this library."""
    # Define default configuration information
    DEFAULT_SETTINGS = {
        'community_url': 'https://community.khoros.com',
        'tenant_id': 'lithosphere',
        'use_community_name': False,
        'debug_mode': False,
        'translate_errors': True
    }
    DEFAULT_AUTH = {
        'auth_type': 'session_auth'
    }

    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(self, defined_settings=None, community_url=None, tenant_id=None, community_name=None, auth_type=None,
                 session_auth=None, oauth2=None, sso=None, helper=None, env_variables=None, auto_connect=True,
                 use_community_name=False, prefer_json=True, debug_mode=False, skip_env_variables=False, empty=False,
                 ssl_verify=None):
        """This method instantiates the core Khoros object.

        .. versionchanged:: 4.3.0
           Fixed an issue where the ``ssl_verify`` parameter was being mostly disregarded.

        .. versionchanged:: 4.2.0
           Introduced support for LithiumSSO Token authentication and made some general code improvements.

        .. versionchanged:: 3.4.0
           Introduced the ``ssl_verify`` parameter and established a key-value pair for it in the
           ``core_settings`` dictionary for the object.

        .. versionchanged:: 3.3.2
           Method arguments are no longer ignored if they are implicitly ``False`` and instead only the
           arguments that explicitly have a ``None`` value are ignored. The ``skip_env_variables`` argument
           has also been introduced to explicitly ignore any valid environment variables, as well as the
           ``empty`` argument to optionally instantiate an empty instantiated object. Logging was also added
           in various locations throughout the method.

        .. versionchanged:: 3.3.0
           Changed ``settings`` to ``defined_settings`` and ``_settings`` to ``_core_settings``.

        :param defined_settings: Predefined settings that the object should use
        :type defined_settings: dict, None
        :param community_url: The base URL of the Khoros community instance (e.g. ``community.khoros.com``)
        :type community_url: str, None
        :param tenant_id: The tenant ID for the Khoros community instance (e.g. ``lithosphere``)
        :type tenant_id: str, None
        :param community_name: The community name (e.g. ``community-name``) for the Khoros community instance
        :type community_name: str, None
        :param auth_type: The authentication type to use when connecting to the instance (``session_auth`` by default)
        :type auth_type: str, None
        :param session_auth: The ``username`` and ``password`` values for session key authentication
        :type session_auth: dict, None
        :param oauth2: The ``client_id``, ``client_secret`` and ``redirect_url`` values for OAuth 2.0 authentication
        :type oauth2: dict, None
        :param sso: The values for single sign-on (SSO) authentication
        :type sso: dict, None
        :param helper: The path (and optional file type) to the YAML or JSON helper configuration file
        :type helper: str, tuple, list, dict, None
        :param env_variables: A dictionary (or file path to a YAML or JSON file) that maps environment variable names
        :type env_variables: dict, str, None
        :param auto_connect: Determines if a connection should be established when initialized (``True`` by default)
        :type auto_connect: bool
        :param use_community_name: Defines if the community name should be used in the API URLs (``False`` by default)
        :type use_community_name: bool
        :param prefer_json: Defines preference that API responses be returned in JSON format (``True`` by default)
        :type prefer_json: bool
        :param debug_mode: Determines if Debug Mode should be enabled for development purposes (``False`` by default)
        :type debug_mode: bool
        :param skip_env_variables: Explicitly ignores any valid environment variables (``False`` by default)
        :type skip_env_variables: bool
        :param empty: Instantiates an empty object to act as a placeholder with default values (``False`` by default)
        :type empty: bool
        :param ssl_verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
        :type ssl_verify: bool, None
        :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
                 :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
                 :py:exc:`khoros.errors.exceptions.SessionAuthenticationError`
        """
        # Define the current version
        self.version = version.get_full_version()

        # Initialize the predefined settings dictionary if not passed to the class
        defined_settings = {} if not defined_settings else defined_settings

        # Initialize other dictionaries that will be used by the class object
        self.auth = {}
        self.core = {}
        self.construct = {}
        self._helper_settings = {}

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
            'prefer_json': prefer_json,
            'debug_mode': debug_mode,
            'skip_env_variables': skip_env_variables,
            'empty': empty,
            'ssl_verify': ssl_verify,
        }
        for _arg_key, _arg_val in _individual_arguments.items():
            if _arg_val is not None and defined_settings.get(_arg_key) is None:
                defined_settings[_arg_key] = _arg_val

        # Creates the private core_settings attribute using the default settings as a base
        self.core_settings = copy.copy(Khoros.DEFAULT_SETTINGS)
        self.core_settings.update(Khoros.DEFAULT_AUTH)

        # Capture any relevant environment variables if defined
        if not helper and not skip_env_variables and not empty:
            # Only define the environment variables if a helper file was not supplied as the file takes precedence
            environment.update_env_variable_names(env_variables)
            self._env_settings = environment.get_env_variables()
            self._parse_env_settings()
        else:
            self._env_settings = {}

        # Overwrite any settings with any that were passed in the settings argument
        self.core_settings.update(defined_settings)

        # Capture the helper settings if applicable
        if helper is None:
            self._helper_settings['connection'] = {}
            self._helper_settings['discussion_styles'] = ['blog', 'contest', 'forum', 'idea', 'qanda', 'tkb']
            if ssl_verify is None and self.core_settings.get('ssl_verify') is None:
                self._helper_settings['ssl_verify'] = True
        else:
            self.core_settings['helper'] = helper
            if any((isinstance(helper, tuple), isinstance(helper, list))):
                file_path, file_type = helper
            elif isinstance(helper, str):
                file_path, file_type = (helper, 'yaml')
            elif isinstance(helper, dict):
                file_path, file_type = helper.values()
            else:
                error_msg = "The 'helper' argument can only be supplied as tuple, string, list or dict."
                logger.error(error_msg)
                raise TypeError(error_msg)
            self._helper_settings = get_helper_settings(file_path, file_type, defined_settings)

            # Parse the helper settings
            self._parse_helper_settings()

        # Add the SSL verification setting if applicable
        if 'ssl_verify' in self._helper_settings:
            self.core_settings['ssl_verify'] = self._helper_settings.get('ssl_verify')
        elif ssl_verify is None and self.core_settings.get('ssl_verify') is None:
            self.core_settings['ssl_verify'] = True

        # Update the global variable if SSL Verify is explicitly disabled
        if self.core_settings.get('ssl_verify') is False:
            api.ssl_verify_disabled = True

        # Add the authentication status
        if 'active' not in self.auth:
            self.auth['active'] = False

        # Update the default authentication type if necessary
        self.auth['type'] = self.core_settings.get('auth_type')
        if auth_type is not None:
            accepted_auth_types = ['session_auth', 'oauth2', 'sso']
            auth_map = {
                'session_auth': session_auth,
                'oauth2': oauth2,
                'sso': sso
            }
            if str(auth_type) in accepted_auth_types:
                self.core_settings['auth_type'] = auth_type
                self.auth['type'] = auth_type
                if auth_map.get(auth_type) is None and auth_type not in self._helper_settings.get('connection'):
                    error_msg = f"The '{auth_type}' authentication type was specified but no associated data was found."
                    logger.error(error_msg)
                    raise errors.exceptions.MissingAuthDataError(error_msg)
            else:
                error_msg = f"'{auth_type}' is an invalid authentication type. Reverting to default. ('session_auth')"
                logger.warn(error_msg)
                errors.handlers.eprint(error_msg)
                self.core_settings.update(Khoros.DEFAULT_AUTH)
                self.auth['type'] = self.core_settings.get('auth_type')
        elif sso is not None:
            self.core_settings['auth_type'] = 'sso'
            self.auth['type'] = self.core_settings.get('auth_type')
        elif oauth2 is not None:
            self.core_settings['auth_type'] = 'oauth2'
            self.auth['type'] = self.core_settings.get('auth_type')
        else:
            if empty:
                self._populate_empty_object()
            if session_auth is not None or empty:
                # Session authentication is selected as the auth type when instantiating an empty object
                self.core_settings['auth_type'] = 'session_auth'
            elif self._session_auth_credentials_defined():
                self.core_settings['auth_type'] = 'session_auth'
            elif 'session_auth' not in self._helper_settings.get('connection'):
                error_msg = f"No data was found for the default '{auth_type}' authentication type."
                logger.error(error_msg)
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
        if not empty:
            self._populate_auth_settings()

        # Populate the khoros.construct dictionary with query and syntax constructors
        self._populate_construct_settings()

        # Auto-connect to the environment if specified (default)
        if self.core_settings.get('auto_connect'):
            if self.core_settings.get('auth_type') in ['sso', 'session_auth']:
                self.connect(self.core_settings.get('auth_type'))
            else:
                error_msg = f"Unable to auto-connect to the instance with the given " \
                            f"'{self.core_settings.get('auth_type')}' authentication type."
                logger.error(error_msg)
                errors.handlers.eprint(error_msg)

        # Import inner object classes so their methods can be called from the primary object
        self.v1 = self._import_v1_class()
        self.v2 = self._import_v2_class()
        self.albums = self._import_album_class()
        self.archives = self._import_archives_class()
        self.boards = self._import_board_class()
        self.categories = self._import_category_class()
        self.communities = self._import_community_class()
        self.grouphubs = self._import_grouphub_class()
        self.messages = self._import_message_class()
        self.nodes = self._import_node_class()
        self.roles = self._import_role_class()
        self.saml = self._import_saml_class()
        self.settings = self._import_settings_class()
        self.studio = self._import_studio_class()
        self.subscriptions = self._import_subscription_class()
        self.tags = self._import_tag_class()
        self.users = self._import_user_class()

    def _populate_empty_object(self):
        """This method populates necessary fields to allow an empty object to be instantiated successfully.

        .. versionadded:: 3.3.2
        """
        # Populate the core settings
        self.core_settings['auth_type'] = 'session_auth'
        self.core_settings['session_auth'] = {'username': 'anonymous', 'password': 'anonymous'}
        self.core_settings['session_auth']['session_key'] = ''
        self.core_settings['auth_header'] = {'li-api-session-key': ''}
        self.core_settings['auto_connect'] = False

        # Populate the authentication settings
        self.auth['session_key'] = ''
        self.auth['header'] = {'li-api-session-key': ''}

    def _populate_core_settings(self):
        """This method populates the khoros.core dictionary with the core public settings used by the object.

        .. versionchanged:: 4.2.0
           The way in which the ``_setting`` value is retrieved from ``self.core_settings`` was improved.
        """
        _core_settings = ['community_url', 'base_url', 'v1_base', 'v2_base']
        for _setting in _core_settings:
            if _setting in self.core_settings:
                self.core[_setting] = self.core_settings.get(_setting)

    def _populate_auth_settings(self):
        """This method populates the khoros.auth dictionary to be leveraged in authentication/authorization tasks.

        .. versionchanged:: 4.2.0
           General code improvements were made to avoid unnecessary :py:exc:`KeyError` exceptions.
        """
        _auth_settings = ['auth_type', 'oauth2', 'session_auth', 'sso']
        _setting_keys = {
            'oauth2': ['client_id', 'client_secret', 'redirect_url'],
            'sso': ['sso_token']
        }
        for _setting in _auth_settings:
            if _setting in self.core_settings:
                if _setting in _setting_keys:
                    for _setting_key in _setting_keys.get(_setting):
                        if _setting_key in self.core_settings.get(_setting):
                            self.auth[_setting_key] = self.core_settings.get(_setting).get(_setting_key)

    def _populate_construct_settings(self):
        """This method populates the khoros.construct dictionary to assist in constructing API queries and responses.

        .. versionchanged:: 4.2.0
           General code improvements were made to avoid unnecessary :py:exc:`KeyError` exceptions.
        """
        if 'prefer_json' in self.core_settings:
            return_formats = {True: '&restapi.response_format=json', False: ''}
            self.construct['response_format'] = return_formats.get(self.core_settings.get('prefer_json'))

    def _parse_env_settings(self):
        """This method parses the settings identified from environment variables.

        .. versionadded:: 2.2.0
        """
        for env_var_name, env_var_value in self._env_settings.items():
            if env_var_name in environment.env_settings_mapping:
                settings_fields = environment.env_settings_mapping.get(env_var_name)
                if len(settings_fields) == 1:
                    self.core_settings[settings_fields[0]] = env_var_value
                elif len(settings_fields) == 2:
                    if settings_fields[0] not in self.core_settings:
                        self.core_settings[settings_fields[0]] = {}
                    self.core_settings[settings_fields[0]][settings_fields[1]] = env_var_value

    def _parse_helper_settings(self):
        """This method parses the settings in the helper configuration file when provided.

        .. versionchanged:: 4.2.0
           General code improvements were made to avoid unnecessary :py:exc:`KeyError` exceptions.

        .. versionchanged:: 2.8.0
           Support was added for the ``translate_errors`` setting and any other top-level setting.
        """
        # Parse the helper settings and add them to the primary settings
        if 'connection' in self._helper_settings:
            _helper_keys = ['connection', 'construct', 'translate_errors']
            _auth_keys = ['oauth2', 'session_auth', 'sso']
            for _helper_key in _helper_keys:
                if _helper_key == 'connection':
                    _connection_keys = ['community_url', 'tenant_id', 'default_auth_type', 'oauth2',
                                        'session_auth', 'sso']
                    for _connection_key in _connection_keys:
                        if _connection_key in self._helper_settings.get('connection'):
                            _new_key = 'auth_type' if _connection_key == 'default_auth_type' else _connection_key
                            self.core_settings[_new_key] = self._helper_settings.get('connection').get(_connection_key)
                elif _helper_key == 'construct':
                    _construct_keys = ['prefer_json']
                    for _construct_key in _construct_keys:
                        if _construct_key in self._helper_settings.get('construct'):
                            self.core_settings[_construct_key] = \
                                self._helper_settings.get('construct').get(_construct_key)
                else:
                    if _helper_key in self._helper_settings:
                        self.core_settings[_helper_key] = self._helper_settings.get(_helper_key)
        if 'discussion_styles' in self._helper_settings:
            if isinstance(self._helper_settings.get('discussion_styles'), list):
                self.core_settings['discussion_styles'] = self._helper_settings.get('discussion_styles')

    def _validate_base_url(self):
        """This method ensures that the Community URL is defined appropriately.

        .. versionchanged:: 4.2.0
           General code improvements were made to avoid unnecessary :py:exc:`KeyError` exceptions.
        """
        if ('http://' not in self.core_settings['community_url']) and \
                ('https://' not in self.core_settings.get('community_url')):
            self.core_settings['community_url'] = f"https://{self.core_settings.get('community_url')}"
        if self.core_settings.get('community_url').endswith('/'):
            self.core_settings['community_url'] = self.core_settings.get('community_url')[:-1]

    def _define_url_settings(self):
        """This method defines the URL settings associated with the Khoros environment.

        .. versionchanged:: 4.2.0
           General code improvements were made to avoid unnecessary :py:exc:`KeyError` exceptions.
        """
        if 'community_name' in self.core_settings and self.core_settings.get('use_community_name') is True:
            self.core_settings['base_url'] = f"{self.core_settings.get('community_url')}/" \
                                             f"{self.core_settings.get('community_name')}"
        else:
            self.core_settings['base_url'] = self.core_settings.get('community_url')
        self.core_settings['v1_base'] = f"{self.core_settings.get('community_url')}/restapi/vc"
        self.core_settings['v2_base'] = f"{self.core_settings.get('base_url')}/api/2.0"

    def _session_auth_credentials_defined(self):
        """This method checks to see if session authentication credentials have been defined.

        .. versionchanged:: 4.2.0
           General code improvements were made to avoid unnecessary :py:exc:`KeyError` exceptions.

        .. versionadded:: 2.2.0
        """
        _defined = False
        if 'session_auth' in self.core_settings:
            _defined = True if ('username' in self.core_settings.get('session_auth') and
                                'password' in self.core_settings.get('session_auth')) else _defined
        return _defined

    def _connect_with_session_key(self):
        """This method establishes a connection to the Khoros environment using basic / session key authentication.

        .. versionchanged:: 4.2.0
           General code improvements were made to avoid unnecessary :py:exc:`KeyError` exceptions.

        .. versionchanged:: 3.3.2
           Added logging for the :py:exc:`khoros.errors.exceptions.MissingAuthDataError` exception.

        :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
        """
        if ('username' not in self.core_settings.get('session_auth')) or \
                ('password' not in self.core_settings.get('session_auth')):
            error_msg = f"The username and/or password for session key authentication cannot be found."
            logger.error(error_msg)
            raise errors.exceptions.MissingAuthDataError(error_msg)

        self.core_settings['session_auth']['session_key'] = auth.get_session_key(self)
        self.core_settings['auth_header'] = \
            auth.get_session_header(self.core_settings.get('session_auth').get('session_key'))
        self.auth['session_key'] = self.core_settings.get('session_auth').get('session_key')
        self.auth['header'] = self.core_settings.get('auth_header')
        self.auth['active'] = True

    def _connect_with_lithium_token(self):
        """This method establishes a connection to the Khoros environment using SSO authentication.

        .. versionadded:: 4.2.0

        :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
        """
        if "sso.authentication_token" not in self.core_settings.get('sso'):
            raise errors.exceptions.MissingAuthDataError("SSO authentication requires a LithiumSSO token.")

        li_api_session_key = auth.get_sso_key(self)
        session_key = auth.get_session_header(li_api_session_key)
        self.auth['session_key'] = session_key
        self.auth['header'] = session_key
        self.auth['active'] = True

    def _import_v1_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.V1` inner class to be utilized in the
        core object.

        .. versionadded:: 3.0.0
        """
        return Khoros.V1(self)

    def _import_v2_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.V2` inner class to be utilized in the
        core object.

        .. versionadded:: 4.0.0
        """
        return Khoros.V2(self)

    def _import_album_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Album` inner class to be utilized in the
        core object.

        .. versionadded:: 2.3.0
        """
        return Khoros.Album(self)

    def _import_archives_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Archives` inner class to be utilized in the
        core object.

        .. versionadded:: 4.1.0
        """
        return Khoros.Archives(self)

    def _import_board_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Board` inner class to be utilized in the
        core object.

        .. versionadded:: 2.5.0
        """
        return Khoros.Board(self)

    def _import_category_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Category` inner class to be utilized in the
        core object.

        .. versionadded:: 2.1.0
        """
        return Khoros.Category(self)

    def _import_community_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Community` inner class to be utilized in the
        core object.

        .. versionadded:: 2.1.0
        """
        return Khoros.Community(self)

    def _import_grouphub_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.GroupHub` inner class to be utilized in the
        core object.

        .. versionadded:: 2.6.0
        """
        return Khoros.GroupHub(self)

    def _import_message_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Message` inner class to be utilized in the core object.

        .. versionadded:: 2.3.0
        """
        return Khoros.Message(self)

    def _import_node_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Node` inner class to be utilized in the core object.

        .. versionadded:: 2.1.0
        """
        return Khoros.Node(self)

    def _import_role_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Role` inner class to be utilized in the core object.

        .. versionadded:: 2.4.0
        """
        return Khoros.Role(self)

    def _import_saml_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.SAML` inner class to be utilized in the core object.

        .. versionadded:: 4.3.0
        """
        return Khoros.SAML(self)

    def _import_settings_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Settings` inner class to be utilized in the core object.

        .. versionadded:: 3.2.0
        """
        return Khoros.Settings(self)

    def _import_studio_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Studio` inner class to be utilized in the core object.

        .. versionadded:: 2.5.1
        """
        return Khoros.Studio(self)

    def _import_subscription_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Subscription` inner class to be utilized
           in the core object.

        .. versionadded:: 3.5.0
        """
        return Khoros.Subscription(self)

    def _import_tag_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.Tag` inner class to be utilized in the core object.

        .. versionadded:: 4.1.0
        """
        return Khoros.Tag(self)

    def _import_user_class(self):
        """This method allows the :py:class:`khoros.core.Khoros.User` inner class to be utilized in the core object.

        .. versionadded:: 2.0.0
        """
        return Khoros.User(self)

    # The public functions below provide ways to interact with the Khoros object
    def connect(self, connection_type=None):
        """This method establishes a connection to the environment using a specified authentication type.

        .. versionchanged:: 4.2.0
           Introduced support for LithiumSSO Token authentication and made general code improvements to avoid
           unnecessary :py:exc:`KeyError` exceptions. Also fixed an issue with the exception error message.

        .. versionchanged:: 3.3.2
           Added logging for the :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError` exception.

        :param connection_type: The type of authentication method (e.g. ``session_auth``)
        :type connection_type: str, None
        :returns: None
        :raises: :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`
        """
        if connection_type is None:
            connection_type = self.core_settings.get('auth_type')
        if connection_type == 'session_auth':
            self._connect_with_session_key()
        elif connection_type == 'sso':
            self._connect_with_lithium_token()
        else:
            error_msg = f"The '{connection_type}' authentication type is currently unsupported."
            logger.error(error_msg)
            raise errors.exceptions.CurrentlyUnsupportedError(f"'{connection_type}' authentication type")

    def get_session_key(self, username=None, password=None):
        """This method retrieves the session key for an authentication session.

        .. versionadded:: 3.5.0

        :param username: The username (i.e. login) of a secondary user to authenticate *(optional)*
        :type username:  str, None
        :param password: The password of a secondary user to authenticate *(optional)*

                         .. caution:: It is recommended that the :py:func:`khoros.core.Khoros.users.impersonate_user``
                                      method be used instead of authenticating as a secondary user with this method.

        :type password: str, None
        :returns: The session key in string format
        :raises: :py:exc:`khoros.errors.exceptions.SessionAuthenticationError`
        """
        return auth.get_session_key(self, username, password)

    def get(self, query_url, relative_url=True, return_json=True, headers=None, proxy_user_object=None):
        """This method performs a simple GET request that leverages the Khoros authorization headers.

        .. versionchanged:: 4.2.0
           Resolved an issue that caused errors with absolute URLs, and made general code improvements were made
           to avoid unnecessary :py:exc:`KeyError` exceptions.

        .. versionchanged:: 4.0.0
           Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
           of other users.

        :param query_url: The relative (default) or fully-qualified URL for the API call
        :type query_url: str
        :param relative_url: Determines if the URL should be appended to the community domain (``True`` by default)
        :type relative_url: bool
        :param return_json: Determines if the API response should be converted into JSON format (``True`` by default)
        :type return_json: bool
        :param headers: Allows the API call headers to be manually defined rather than using only the core object
        :type headers: dict, None
        :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                                  API request on behalf of a secondary user.
        :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
        :returns: The API response from the GET request
        :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
                 :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                 :py:exc:`khoros.errors.exceptions.GETRequestError`
        """
        query_url = f"/{query_url}" if not query_url.startswith('/') and relative_url else query_url
        query_url = f"{self.core_settings.get('community_url')}{query_url}" if relative_url else query_url
        return api.get_request_with_retries(query_url, return_json=return_json, headers=headers, khoros_object=self,
                                            proxy_user_object=proxy_user_object)

    def post(self, query_url, payload=None, relative_url=True, return_json=True, content_type=None, headers=None,
             multipart=False, proxy_user_object=None):
        """This method performs a simple POST request that leverages the Khoros authorization headers.

        .. versionchanged:: 4.2.0
           Resolved an issue that caused errors with absolute URLs, and made general code improvements were made
           to avoid unnecessary :py:exc:`KeyError` exceptions.

        .. versionchanged:: 4.0.0
           Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
           of other users.

        .. versionchanged:: 3.5.0
           The ``query_url`` no longer gets prefixed with a slash (``/``) if ``relative_url`` is set to ``False``.

        .. versionchanged:: 3.1.1
           The ``content_type`` parameter now gets defined as an empty string prior to calling the sub-function.

        .. versionadded:: 3.1.0

        :param query_url: The relative (default) or fully-qualified URL for the API call
        :type query_url: str
        :param payload: The JSON or plaintext payload (if any) to be supplied with the API request

                        .. todo:: Add support for other payload formats such as binary, etc.

        :type payload: dict, str, None
        :param relative_url: Determines if the URL should be appended to the community domain (``True`` by default)
        :type relative_url: bool
        :param return_json: Determines if the API response should be converted into JSON format (``True`` by default)
        :type return_json: bool
        :param content_type: Allows the ``content-type`` value to be explicitly defined if necessary

                             .. note:: If this parameter is not defined then the content type will be identified based
                                       on the payload format and/or type of request.

        :type content_type: str, None
        :param headers: Allows the API call headers to be manually defined rather than using only the core object
        :type headers: dict, None
        :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
        :type multipart: bool
        :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                                  API request on behalf of a secondary user.
        :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
        :returns: The API response from the POST request
        :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                 :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                 :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
        """
        query_url = f"/{query_url}" if not query_url.startswith('/') and relative_url else query_url
        query_url = f"{self.core_settings.get('community_url')}{query_url}" if relative_url else query_url[1:]
        json_payload = payload if isinstance(payload, dict) else None
        plaintext_payload = payload if isinstance(payload, str) else None
        content_type = '' if not content_type else content_type
        return api.post_request_with_retries(query_url, json_payload=json_payload, plaintext_payload=plaintext_payload,
                                             return_json=return_json, headers=headers, multipart=multipart,
                                             content_type=content_type.lower(), khoros_object=self,
                                             proxy_user_object=proxy_user_object)

    def put(self, query_url, payload=None, relative_url=True, return_json=True, content_type=None, headers=None,
            multipart=False, proxy_user_object=None):
        """This method performs a simple PUT request that leverages the Khoros authorization headers.

        .. versionchanged:: 4.2.0
           Resolved an issue that caused errors with absolute URLs, and made general code improvements were made
           to avoid unnecessary :py:exc:`KeyError` exceptions.

        .. versionchanged:: 4.0.0
           Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
           of other users.

        .. versionchanged:: 3.1.1
           The ``content_type`` parameter now gets defined as an empty string prior to calling the sub-function.

        .. versionadded:: 3.1.0

        :param query_url: The relative (default) or fully-qualified URL for the API call
        :type query_url: str
        :param payload: The JSON or plaintext payload (if any) to be supplied with the API request

                        .. todo:: Add support for other payload formats such as binary, etc.

        :type payload: dict, str, None
        :param relative_url: Determines if the URL should be appended to the community domain (``True`` by default)
        :type relative_url: bool
        :param return_json: Determines if the API response should be converted into JSON format (``True`` by default)
        :type return_json: bool
        :param content_type: Allows the ``content-type`` value to be explicitly defined if necessary

                             .. note:: If this parameter is not defined then the content type will be identified based
                                       on the payload format and/or type of request.

        :type content_type: str, None
        :param headers: Allows the API call headers to be manually defined rather than using only the core object
        :type headers: dict, None
        :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
        :type multipart: bool
        :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                                  API request on behalf of a secondary user.
        :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
        :returns: The API response from the PUT request
        :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                 :py:exc:`khoros.errors.exceptions.PUTRequestError`,
                 :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
        """
        query_url = f"/{query_url}" if not query_url.startswith('/') and relative_url else query_url
        query_url = f"{self.core_settings.get('community_url')}{query_url}" if relative_url else query_url
        json_payload = payload if isinstance(payload, dict) else None
        plaintext_payload = payload if isinstance(payload, str) else None
        content_type = '' if not content_type else content_type
        return api.put_request_with_retries(query_url, json_payload=json_payload, plaintext_payload=plaintext_payload,
                                            return_json=return_json, headers=headers, multipart=multipart,
                                            content_type=content_type.lower(), khoros_object=self,
                                            proxy_user_object=proxy_user_object)

    def query(self, query, return_json=True, pretty_print=False, track_in_lsi=False, always_ok=False,
              error_code='', format_statements=True, return_items=False):
        """This method performs a Community API v2 query using LiQL with the full LiQL syntax.

        .. versionchanged:: 4.1.0
           The JSON response can now be reduced to just the returned items by passing ``return_items=True``.

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
        :param format_statements: Determines if statements (e.g. ``SELECT``, ``FROM``, et.) should be formatted to be
                                  in all caps (``True`` by default)
        :type format_statements: bool
        :param return_items: Reduces the JSON response to be only the list of items returned from the LiQL response
                             (``False`` by default)

                             .. note:: If an error response is returned then an empty list will be returned.

        :type return_items: bool
        :returns: The query response from the API in JSON format (unless defined otherwise)
        :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
                 :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                 :py:exc:`khoros.errors.exceptions.GETRequestError`
        """
        query_url = liql.get_query_url(self.core, query, pretty_print, track_in_lsi, always_ok,
                                       error_code, format_statements)
        return liql.perform_query(self, query_url, return_json=return_json, return_items=return_items)

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
        """This method retrieves the total asset count from a given collection (e.g. ``categories``).

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

    def get_platform_version(self, full_release=False, simple=False, commit_id=False, timestamp=False):
        """This method retrieves the Khoros Community platform version information for a given environment.

        .. versionadded:: 3.4.0

        :param full_release: Defines if the full platform release version should be returned

                             .. note:: If none of the options are enabled then the ``full_release`` option will be
                                       enabled by default.

        :type full_release: bool
        :param simple: Defines if the simple X.Y version (e.g. 20.6) should be returned (``False`` by default)
        :type simple: bool
        :param commit_id: Defines if the Commit ID (i.e. hash) for the release should be returned (``False`` by default)
        :type commit_id: bool
        :param timestamp: Defines if the timestamp of the release (e.g. 2007092156) should be returned
                          (``False`` by default)
        :type timestamp: bool
        :returns: One or more string with version information
        :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
        """
        base_url = self.core_settings.get('base_url')
        return api.get_platform_version(base_url, full_release, simple, commit_id, timestamp, self)

    def perform_v1_search(self, endpoint, filter_field, filter_value, return_json=False, fail_on_no_results=False):
        """This method performs a search for a particular field value using a Community API v1 call.

        .. versionchanged:: 3.3.2
           Added logging for the :py:exc:`DeprecationWarning`.

        .. deprecated:: 3.0.0
           Use the :py:meth:`khoros.core.Khoros.V1.search` method instead.

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
        warnings.warn("This method has been deprecated. Use the v1.search method instead",
                      DeprecationWarning)
        logger.warn("The 'perform_v1_search' method has been deprecated. Use the 'v1.search' method instead.")
        return api.perform_v1_search(self, endpoint, filter_field, filter_value, return_json, fail_on_no_results)

    @staticmethod
    def parse_v2_response(json_response, return_dict=False, status=False, error_msg=False, http_code=False,
                          data_id=False, data_url=False, data_api_uri=False, v2_base=''):
        """This method parses an API response for a Community API v2 operation and returns parsed data.

        .. versionchanged:: 3.2.0
           The lower-level function call now utilizes keyword arguments to fix an argument mismatch issue.

        .. versionadded:: 2.5.0

        :param json_response: The API response in JSON format
        :type json_response: dict
        :param return_dict: Defines if the parsed data should be returned within a dictionary
        :type return_dict: bool
        :param status: Defines if the **status** value should be returned
        :type status: bool
        :param error_msg: Defines if the error message (and **developer response** message) should be returned
        :type error_msg: bool
        :param http_code: Defines if the **HTTP status code** should be returned
        :type http_code: bool
        :param data_id: Defines if the **ID** should be returned
        :type data_id: bool
        :param data_url: Defines if the **URL** should be returned
        :type data_url: bool
        :param data_api_uri: Defines if the **API URI** should be returned
        :type data_api_uri: bool
        :param v2_base: The base URL for the API v2
        :type v2_base: str
        :returns: A string, tuple or dictionary with the parsed data
        :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
        """
        return api.parse_v2_response(json_response, return_dict, status, error_msg, dev_msg=error_msg,
                                     http_code=http_code, data_id=data_id, data_url=data_url,
                                     data_api_uri=data_api_uri, v2_base=v2_base)

    class V1(object):
        """This class includes methods for performing base Community API v1 requests."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.V1` inner class object.

            .. versionadded:: 3.0.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def get(self, endpoint, query_params=None, return_json=True, proxy_user_object=None):
            """This method makes a Community API v1 GET request.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.0.0

            :param endpoint: The API endpoint to be queried
            :type endpoint: str
            :param query_params: The field and associated values to be leveraged in the query string
            :type query_params: dict
            :param return_json: Determines if the response should be returned in JSON format rather than the default
            :type return_json: bool
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response
            :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
                     :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
                     :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`
            """
            query_params = {} if not query_params else query_params
            return api.make_v1_request(self.khoros_object, endpoint, query_params, 'GET', return_json,
                                       proxy_user_object=proxy_user_object)

        def post(self, endpoint, query_params=None, return_json=True, params_in_uri=False, json_payload=False,
                 proxy_user_object=None):
            """This method makes a Community API v1 POST request.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionchanged:: 3.2.0
               Introduced the ability to pass the query parameters as payload to avoid URI length limits.

            .. versionadded:: 3.0.0

            :param endpoint: The API endpoint to be queried
            :type endpoint: str
            :param query_params: The field and associated values to be leveraged in the query string
            :type query_params: dict
            :param return_json: Determines if the response should be returned in JSON format rather than the default
            :type return_json: bool
            :param params_in_uri: Determines if query parameters should be passed in the URI rather than in the
                                  request body (``False`` by default)
            :type params_in_uri: bool
            :param json_payload: Determines if query parameters should be passed as JSON payload rather than in the URI
                                 (``False`` by default)

                                 .. caution:: This is not yet fully supported and therefore should not be used
                                              at this time.

            :type json_payload: bool
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response
            :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
                     :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            query_params = {} if not query_params else query_params
            return api.make_v1_request(self.khoros_object, endpoint, query_params, 'POST', return_json=return_json,
                                       params_in_uri=params_in_uri, json_payload=json_payload,
                                       proxy_user_object=proxy_user_object)

        def put(self, endpoint, query_params=None, return_json=True, params_in_uri=False, json_payload=False,
                proxy_user_object=None):
            """This method makes a Community API v1 PUT request.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionchanged:: 3.2.0
               Introduced the ability to pass the query parameters as payload to avoid URI length limits.

            .. versionadded:: 3.0.0

            .. caution:: While ``PUT`` requests are technically supported in this library, at this time
                         they are not yet supported by the Khoros Community API v1 endpoints.

            :param endpoint: The API endpoint to be queried
            :type endpoint: str
            :param query_params: The field and associated values to be leveraged in the query string
            :type query_params: dict
            :param return_json: Determines if the response should be returned in JSON format rather than the default
            :type return_json: bool
            :param params_in_uri: Determines if query parameters should be passed in the URI rather than in the
                                  request body (``False`` by default)
            :type params_in_uri: bool
            :param json_payload: Determines if query parameters should be passed as JSON payload rather than in the URI
                                 (``False`` by default)

                                 .. caution:: This is not yet fully supported and therefore should not be used
                                              at this time.

            :type json_payload: bool
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response
            :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
                     :py:exc:`khoros.errors.exceptions.PUTRequestError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
                     :py:exc:`khoros.errors.exceptions.InvalidRequestTypeError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            query_params = {} if not query_params else query_params
            return api.make_v1_request(self.khoros_object, endpoint, query_params, 'PUT', return_json=return_json,
                                       params_in_uri=params_in_uri, json_payload=json_payload,
                                       proxy_user_object=proxy_user_object)

        def search(self, endpoint, filter_field, filter_value, return_json=False, fail_on_no_results=False,
                   proxy_user_object=None):
            """This method performs a search for a particular field value using a Community API v1 call.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.0.0

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
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response (optionally in JSON format)
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return api.perform_v1_search(self, endpoint, filter_field, filter_value, return_json, fail_on_no_results,
                                         proxy_user_object=proxy_user_object)

    class V2(object):
        """This class includes methods for performing base Community API v2 requests."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.V2` inner class object.

            .. versionadded:: 4.0.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def get(self, endpoint, return_json=True, headers=None, proxy_user_object=None):
            """This method performs a Community API v2 GET request that leverages the Khoros authorization headers.

            .. versionadded:: 4.0.0

            :param endpoint: The API v2 endpoint aginst which to query
            :type endpoint: str
            :param return_json: Determines if the API response should be converted into JSON format (``True`` by default)
            :type return_json: bool
            :param headers: Allows the API call headers to be manually defined rather than using only the core object
            :type headers: dict, None
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                                      API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response from the GET request
            :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            endpoint = f"/{endpoint}" if not endpoint.startswith('/') else endpoint
            query_url = f"{self.khoros_object.core.get('v2_base')}{endpoint}"
            return api.get_request_with_retries(query_url, return_json=return_json, headers=headers,
                                                khoros_object=self.khoros_object, proxy_user_object=proxy_user_object)

        def post(self, endpoint, payload=None, return_json=True, content_type=None, headers=None, multipart=False,
                 proxy_user_object=None):
            """This method performs a Community API v2 POST request that leverages the Khoros authorization headers.

            .. versionadded:: 4.0.0

            :param endpoint: The relative (default) or fully-qualified URL for the API call
            :type endpoint: str
            :param payload: The JSON or plaintext payload (if any) to be supplied with the API request

                            .. todo:: Add support for other payload formats such as binary, etc.

            :type payload: dict, str, None
            :param return_json: Determines if the API response should be converted into JSON format (``True`` by default)
            :type return_json: bool
            :param content_type: Allows the ``content-type`` value to be explicitly defined if necessary

                                 .. note:: If this parameter is not defined then the content type will be identified based
                                           on the payload format and/or type of request.

            :type content_type: str, None
            :param headers: Allows the API call headers to be manually defined rather than using only the core object
            :type headers: dict, None
            :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
            :type multipart: bool
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                                      API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response from the POST request
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            endpoint = f"/{endpoint}" if not endpoint.startswith('/') else endpoint
            query_url = f"{self.khoros_object.core('v2_base')}{endpoint}"
            json_payload = payload if isinstance(payload, dict) else None
            plaintext_payload = payload if isinstance(payload, str) else None
            content_type = '' if not content_type else content_type
            return api.post_request_with_retries(query_url, json_payload=json_payload,
                                                 plaintext_payload=plaintext_payload,
                                                 return_json=return_json, headers=headers, multipart=multipart,
                                                 content_type=content_type.lower(), khoros_object=self.khoros_object,
                                                 proxy_user_object=proxy_user_object)

        def put(self, endpoint, payload=None, return_json=True, content_type=None, headers=None, multipart=False,
                proxy_user_object=None):
            """This method performs a Community API v2 PUT request that leverages the Khoros authorization headers.

            .. versionadded:: 4.0.0

            :param endpoint: The relative (default) or fully-qualified URL for the API call
            :type endpoint: str
            :param payload: The JSON or plaintext payload (if any) to be supplied with the API request

                            .. todo:: Add support for other payload formats such as binary, etc.

            :type payload: dict, str, None
            :param return_json: Determines if the API response should be converted into JSON format (``True`` by default)
            :type return_json: bool
            :param content_type: Allows the ``content-type`` value to be explicitly defined if necessary

                                 .. note:: If this parameter is not defined then the content type will be identified based
                                           on the payload format and/or type of request.

            :type content_type: str, None
            :param headers: Allows the API call headers to be manually defined rather than using only the core object
            :type headers: dict, None
            :param multipart: Defines whether or not the query is a ``multipart/form-data`` query (``False`` by default)
            :type multipart: bool
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                                      API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response from the PUT request
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.PUTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            endpoint = f"/{endpoint}" if not endpoint.startswith('/') else endpoint
            query_url = f"{self.khoros_object.core.get('v2_base')}{endpoint}"
            json_payload = payload if isinstance(payload, dict) else None
            plaintext_payload = payload if isinstance(payload, str) else None
            content_type = '' if not content_type else content_type
            return api.put_request_with_retries(query_url, json_payload=json_payload,
                                                plaintext_payload=plaintext_payload,
                                                return_json=return_json, headers=headers, multipart=multipart,
                                                content_type=content_type.lower(), khoros_object=self.khoros_object,
                                                proxy_user_object=proxy_user_object)

    class Album(object):
        """This class includes methods for interacting with the `albums <https://rsa.im/2WAewBP>`_ collection."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Album` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def create(self, title=None, description=None, owner_id=None, hidden=False, default=False, full_response=False):
            """This method creates a new image album for a user.

            .. versionadded:: 2.3.0

            :param title: The title of the album to be created
            :type title: str, None
            :param description: The description of the album
            :type description: str, None
            :param owner_id: The User ID of the album owner

                             .. note:: If not defined, the owner will be the user performing the API call.

            :type owner_id: str, int, None
            :param hidden: Defines if the album should be public (default) or hidden
            :type hidden: bool
            :param default: Defines if this will be the default album for the user (``False`` by default)
            :type default: bool
            :param full_response: Defines if the full response should be returned instead of the outcome
                                  (``False`` by default)
            :type full_response: bool
            :returns: Boolean value indicating a successful outcome (default) or the full API response
            """
            return objects_module.albums.create(self.khoros_object, title, description, owner_id, hidden,
                                                default, full_response)

        def get_albums_for_user(self, user_id=None, login=None, public=None, private=None, verify_success=False,
                                allow_exceptions=True):
            """This method returns data for the albums owned by a given user.

            .. versionadded:: 2.3.0

            :param user_id: The User ID for the album owner
            :type user_id: str, int
            :param login: The username of the album owner
            :type login: str
            :param public: Indicates that **public** albums should be returned (all albums returned by default)
            :type public: bool
            :param private: Indicates that **private** albums should be returned (all albums returned by default)
            :type private: bool
            :param verify_success: Optionally check to confirm that the API query was successful (``False`` by default)
            :type verify_success: bool
            :param allow_exceptions: Defines whether or not exceptions can be raised for responses returning errors

                                     .. caution:: This does not apply to exceptions for missing required data.

            :type allow_exceptions: bool
            :returns: A list of dictionaries representing each album
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return objects_module.albums.get_albums_for_user(self.khoros_object, user_id, login, public, private,
                                                             verify_success, allow_exceptions)

    class Archives(object):
        """This class includes methods for archiving content.

        .. versionadded:: 4.1.0
        """
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Archives` inner class object.

            .. versionadded:: 4.1.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def archive(self, message_id=None, message_url=None, suggested_url=None, archive_entries=None,
                    aggregate_results=False, include_raw=False):
            """This method archives one or more messages while providing an optional suggested URL as a placeholder.

            .. versionadded:: 4.1.0

            :param message_id: The message ID for the content to be archived
            :type message_id: str, int, None
            :param message_url: The URL of the message to be archived (as an alternative to the ``message_id``
                                argument)
            :type message_url: str, None
            :param suggested_url: The full URL to suggest to the user when navigating to the archived message
            :type suggested_url: str, None
            :param archive_entries: A dictionary mapping one or more message IDs with accompanying suggested URLs

                                    .. note:: Alternatively, a list, tuple or set of message IDs can be supplied
                                              which will be converted into a dictionary with blank suggested URLs.

            :type archive_entries: dict, list, tuple, set, None
            :param aggregate_results: Aggregates the operation results into an easy-to-parse dictionary
                                      (``False`` by default)
            :type aggregate_results: bool
            :param include_raw: Includes the raw API response in the aggregated data dictionary under the ``raw`` key
                                (``False`` by default)

                                .. note:: This parameter is only relevant when the ``aggregate_results``
                                          parameter is ``True``.

            :type include_raw: bool
            :returns: Boolean value indicating a successful outcome (default), the full API response or one or more
                      specific fields defined by function arguments
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`
            """
            return objects_module.archives.archive(self.khoros_object, message_id, message_url, suggested_url,
                                                   archive_entries, aggregate_results, include_raw)

        def unarchive(self, message_id=None, message_url=None, new_board_id=None, archive_entries=None,
                      aggregate_results=False, include_raw=False):
            """This method unarchives one or more messages and moves them to a given board.

            .. versionadded:: 4.1.0

            :param message_id: The message ID for the content to be archived
            :type message_id: str, int, None
            :param message_url: The URL of the message to be archived (as an alternative to the ``message_id`` argument)
            :type message_url: str, None
            :param new_board_id: The board ID of what will be the new parent board of a message getting unarchived
            :type new_board_id: str, None
            :param archive_entries: A dictionary mapping one or more message IDs with accompanying board IDs

                                    .. note:: Alternatively, a list, tuple or set of message IDs can be supplied which
                                              will be converted into a dictionary with blank board IDs.

            :type archive_entries: dict, list, tuple, set, None
            :param aggregate_results: Aggregates the operation results into an easy-to-parse dictionary
                                      (``False`` by default)
            :type aggregate_results: bool
            :param include_raw: Includes the raw API response in the aggregated data dictionary under the ``raw`` key
                                (``False`` by default)

                                .. note:: This parameter is only relevant when the ``aggregate_results``
                                          parameter is ``True``.

            :type include_raw: bool
            :returns: Boolean value indicating a successful outcome (default), the full API response or one or more
                      specific fields defined by function arguments
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`
            """
            return objects_module.archives.unarchive(self.khoros_object, message_id, message_url, new_board_id,
                                                     archive_entries, aggregate_results, include_raw)

        @staticmethod
        def aggregate_results(results, include_raw=False):
            """This method aggregates the results of an archive/unarchive operation into an easy-to-parse dictionary.

            .. versionadded:: 4.1.0

            :param results: The results from an archive or unarchive operation
            :type results: list, dict
            :param include_raw: Includes the raw API response in the aggregated data dictionary under the ``raw`` key
                                (``False`` by default)
            :type include_raw: bool
            :returns: A dictionary with fields for ``status``, ``archived``, ``unarchived``, ``failed`` and ``unknown``
                      or the raw response when the API call completely fails, with the optional raw data when requested
            """
            return objects_module.archives.aggregate_results_data(results, include_raw)

    class Board(object):
        """This class includes methods for interacting with boards.

        .. versionadded:: 2.5.0
        """
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Board` inner class object.

            .. versionadded:: 2.5.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def create(self, board_id, board_title, discussion_style, description=None, parent_category_id=None,
                   hidden=None, allowed_labels=None, use_freeform_labels=None, use_predefined_labels=None,
                   predefined_labels=None, media_type=None, blog_authors=None, blog_author_ids=None,
                   blog_author_logins=None, blog_comments_enabled=None, blog_moderators=None, blog_moderator_ids=None,
                   blog_moderator_logins=None, one_entry_per_contest=None, one_kudo_per_contest=None,
                   posting_date_end=None, posting_date_start=None, voting_date_end=None, voting_date_start=None,
                   winner_announced_date=None, full_response=None, return_id=None, return_url=None, return_api_url=None,
                   return_http_code=None, return_status=None, return_error_messages=None, split_errors=False):
            """This method creates a new board within a Khoros Community environment.

            .. versionchanged:: 2.5.2
               Changed the functionality around the ``return_error_messages`` argument and added the ``split_errors``
               argument.

            .. versionadded:: 2.5.0

            :param board_id: The unique identifier (i.e. ``id`` field) for the new board **(Required)**
            :type board_id: str
            :param board_title: The title of the new board **(Required)**
            :type board_title: str
            :param discussion_style: Defines the board as a ``blog``, ``contest``, ``forum``, ``idea``, ``qanda``
                                     or ``tkb`` **(Required)**
            :type discussion_style: str
            :param description: A brief description of the board
            :type description: str, None
            :param parent_category_id: The ID of the parent category (if applicable)
            :type parent_category_id: str, None
            :param hidden: Defines whether or not the new board should be hidden from lists and menus
                           (disabled by default)
            :type hidden: bool, None
            :param allowed_labels: The type of labels allowed on the board (``freeform-only``, ``predefined-only`` or
                                   ``freeform and pre-defined``)
            :type allowed_labels: str, None
            :param use_freeform_labels: Determines if freeform labels should be utilized
            :type use_freeform_labels: bool, None
            :param use_predefined_labels: Determines if pre-defined labels should be utilized
            :type use_predefined_labels: bool, None
            :param predefined_labels: The pre-defined labels to utilized on the board as a list of dictionaries

                                      .. todo:: The ability to provide labels as a simple list and optionally
                                                standardize their format (e.g. Pascal Case, etc.) will be available
                                                in a future release.

            :type predefined_labels: list, None
            :param media_type: The media type associated with a contest. (``image``, ``video`` or ``story``
                               meaning text)
            :type media_type: str, None
            :param blog_authors: The approved blog authors in a blog board as a list of user data dictionaries
            :type blog_authors: list, None
            :param blog_author_ids: A list of User IDs representing the approved blog authors in a blog board
            :type blog_author_ids: list, None
            :param blog_author_logins: A list of User Logins (i.e. usernames) representing approved blog authors
                                       in a blog board
            :type blog_author_logins: list, None
            :param blog_comments_enabled: Determines if comments should be enabled on blog posts within a blog board
            :type blog_comments_enabled: bool, None
            :param blog_moderators: The designated blog moderators in a blog board as a list of user data dictionaries
            :type blog_moderators: list, None
            :param blog_moderator_ids: A list of User IDs representing the blog moderators in a blog board
            :type blog_moderator_ids: list, None
            :param blog_moderator_logins: A list of User Logins (i.e. usernames) representing blog moderators in a
                                          blog board
            :type blog_moderator_logins: list, None
            :param one_entry_per_contest: Defines whether a user can submit only one entry to a single contest
            :type one_entry_per_contest: bool, None
            :param one_kudo_per_contest: Defines whether a user can vote only once per contest
            :type one_kudo_per_contest: bool, None
            :param posting_date_end: The date/time when the contest is closed to submissions
            :type posting_date_end: type[datetime.datetime], None
            :param posting_date_start: The date/time when the voting period for a contest begins
            :type posting_date_start: type[datetime.datetime], None
            :param voting_date_end: The date/time when the voting period for a contest ends
            :type voting_date_end: type[datetime.datetime], None
            :param voting_date_start: The date/time when the voting period for a contest begins
            :type voting_date_start: type[datetime.datetime], None
            :param winner_announced_date: The date/time the contest winner will be announced
            :type winner_announced_date: type[datetime.datetime], None
            :param full_response: Determines whether the full, raw API response should be returned by the function
            :type full_response: bool, None
            :param return_id: Determines if the **ID** of the new board should be returned by the function
            :type return_id: bool, None
            :param return_url: Determines if the **URL** of the new board should be returned by the function
            :type return_url: bool, None
            :param return_api_url: Determines if the **API URL** of the new board should be returned by the function
            :type return_api_url: bool, None
            :param return_http_code: Determines if the **HTTP Code** of the API response should be returned by
                                     the function
            :type return_http_code: bool, None
            :param return_status: Determines if the **Status** of the API response should be returned by the function
            :type return_status: bool, None
            :param return_error_messages: Determines if the **Developer Response Message** (if any) associated with
                   the API response should be returned by the function
            :type return_error_messages: bool, None
            :param split_errors: Defines whether or not error messages should be merged when applicable
            :type split_errors: bool
            :returns: Boolean value indicating a successful outcome (default), the full API response or one or more
                      specific fields defined by function arguments
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
                     :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`
            """
            return structures_module.boards.create(self.khoros_object, board_id, board_title, discussion_style,
                                                   description, parent_category_id, hidden, allowed_labels,
                                                   use_freeform_labels, use_predefined_labels, predefined_labels,
                                                   media_type, blog_authors, blog_author_ids, blog_author_logins,
                                                   blog_comments_enabled, blog_moderators, blog_moderator_ids,
                                                   blog_moderator_logins, one_entry_per_contest, one_kudo_per_contest,
                                                   posting_date_end, posting_date_start, voting_date_end,
                                                   voting_date_start, winner_announced_date, full_response, return_id,
                                                   return_url, return_api_url, return_http_code, return_status,
                                                   return_error_messages, split_errors)

        def structure_payload(self, board_id, board_title, discussion_style, description=None, parent_category_id=None,
                              hidden=None, allowed_labels=None, use_freeform_labels=None, use_predefined_labels=None,
                              predefined_labels=None, media_type=None, blog_authors=None, blog_author_ids=None,
                              blog_author_logins=None, blog_comments_enabled=None, blog_moderators=None,
                              blog_moderator_ids=None, blog_moderator_logins=None, one_entry_per_contest=None,
                              one_kudo_per_contest=None, posting_date_end=None, posting_date_start=None,
                              voting_date_end=None, voting_date_start=None, winner_announced_date=None):
            """This method structures the payload to use in a Community API v2 request involving a board.

            .. versionadded:: 2.6.0

            :param board_id: The unique identifier (i.e. ``id`` field) for the new board **(Required)**
            :type board_id: str
            :param board_title: The title of the new board **(Required)**
            :type board_title: str
            :param discussion_style: Defines the board as a ``blog``, ``contest``, ``forum``, ``idea``, ``qanda`` or
                                     ``tkb`` **(Required)**
            :type discussion_style: str
            :param description: A brief description of the board
            :type description: str, None
            :param parent_category_id: The ID of the parent category (if applicable)
            :type parent_category_id: str, None
            :param hidden: Defines whether or not the new board should be hidden from lists and menus
                           (disabled by default)
            :type hidden: bool, None
            :param allowed_labels: The type of labels allowed on the board (``freeform-only``, ``predefined-only`` or
                                   ``freeform and pre-defined``)
            :type allowed_labels: str, None
            :param use_freeform_labels: Determines if freeform labels should be utilized
            :type use_freeform_labels: bool, None
            :param use_predefined_labels: Determines if pre-defined labels should be utilized
            :type use_predefined_labels: bool, None
            :param predefined_labels: The pre-defined labels to utilized on the board as a list of dictionaries

                                      .. todo:: The ability to provide labels as a simple list and optionally
                                                standardize their format (e.g. Pascal Case, etc.) will be available
                                                in a future release.

            :type predefined_labels: list, None
            :param media_type: The media type associated with a contest. (``image``, ``video`` or ``story`` i.e. text)
            :type media_type: str, None
            :param blog_authors: The approved blog authors in a blog board as a list of user data dictionaries
            :type blog_authors: list, None
            :param blog_author_ids: A list of User IDs representing the approved blog authors in a blog board
            :type blog_author_ids: list, None
            :param blog_author_logins: A list of User Logins (i.e. usernames) representing approved blog authors
                                       in a blog board
            :type blog_author_logins: list, None
            :param blog_comments_enabled: Determines if comments should be enabled on blog posts within a blog board
            :type blog_comments_enabled: bool, None
            :param blog_moderators: The designated blog moderators in a blog board as a list of user data dictionaries
            :type blog_moderators: list, None
            :param blog_moderator_ids: A list of User IDs representing the blog moderators in a blog board
            :type blog_moderator_ids: list, None
            :param blog_moderator_logins: A list of User Logins (i.e. usernames) representing blog moderators
                                          in a blog board
            :type blog_moderator_logins: list, None
            :param one_entry_per_contest: Defines whether a user can submit only one entry to a single contest
            :type one_entry_per_contest: bool, None
            :param one_kudo_per_contest: Defines whether a user can vote only once per contest
            :type one_kudo_per_contest: bool, None
            :param posting_date_end: The date/time when the contest is closed to submissions
            :type posting_date_end: type[datetime.datetime], None
            :param posting_date_start: The date/time when the voting period for a contest begins
            :type posting_date_start: type[datetime.datetime], None
            :param voting_date_end: The date/time when the voting period for a contest ends
            :type voting_date_end: type[datetime.datetime], None
            :param voting_date_start: The date/time when the voting period for a contest begins
            :type voting_date_start: type[datetime.datetime], None
            :param winner_announced_date: The date/time the contest winner will be announced
            :type winner_announced_date: type[datetime.datetime], None
            :returns: The full and properly formatted payload for the API request
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
            """
            return structures_module.boards.structure_payload(self.khoros_object, board_id, board_title,
                                                              discussion_style, description, parent_category_id, hidden,
                                                              allowed_labels, use_freeform_labels,
                                                              use_predefined_labels, predefined_labels, media_type,
                                                              blog_authors, blog_author_ids, blog_author_logins,
                                                              blog_comments_enabled, blog_moderators,
                                                              blog_moderator_ids, blog_moderator_logins,
                                                              one_entry_per_contest, one_kudo_per_contest,
                                                              posting_date_end, posting_date_start, voting_date_end,
                                                              voting_date_start, winner_announced_date)

        @staticmethod
        def get_board_id(url):
            """This method retrieves the Board ID for a given board when provided its URL.

            .. versionadded:: 2.6.0

            :param url: The URL from which to parse out the Board ID
            :type url: str
            :returns: The Board ID retrieved from the URL
            :raises: :py:exc:`khoros.errors.exceptions.InvalidURLError`
            """
            return structures_module.boards.get_board_id(url)

        def board_exists(self, board_id=None, board_url=None):
            """This method checks to see if a board (i.e. blog, contest, forum, idea exchange, Q&A or TKB) exists.

            .. versionadded:: 2.7.0

            :param board_id: The ID of the board to check
            :type board_id: str, None
            :param board_url: The URL of the board to check
            :type board_url: str, None
            :returns: Boolean value indicating whether or not the board already exists
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.boards.board_exists(self.khoros_object, board_id, board_url)

    class Category(object):
        """This class includes methods for interacting with categories."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Category` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def create(self, category_id, category_title, parent_id=None, return_json=True):
            """This method creates a new category.

            .. versionadded:: 2.5.0

            :param category_id: The Category ID of the new category (e.g. ``video-games``)
            :type category_id: str
            :param category_title: The title of the new category (e.g. ``Video Games``)
            :type category_title: str
            :param parent_id: The Category ID of the parent category (optional)
            :type parent_id: str, None
            :param return_json: Determines whether or not the response should be returned in JSON format
                                (``True`` by default)
            :type return_json: bool
            :returns: The response from the API call
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`
            """
            return structures_module.categories.create(self.khoros_object, category_id, category_title, parent_id,
                                                       return_json)

        @staticmethod
        def get_category_id(url):
            """This method retrieves the Category ID for a given category when provided its URL.

            :param url: The URL from which to parse out the Category ID
            :type url: str
            :returns: The Category ID retrieved from the URL
            :raises: :py:exc:`khoros.errors.exceptions.InvalidURLError`
            """
            return structures_module.categories.get_category_id(url)

        def get_total_count(self):
            """This method returns the total number of categories within the Khoros Community environment.

            .. versionadded:: 2.6.0

            :returns: The total number of categories as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.categories.get_total_count(self.khoros_object)

        def get_total_category_count(self):
            """This method returns the total number of categories within the Khoros Community environment.

            .. versionchanged:: 3.3.2
               Added logging for the :py:exc:`DeprecationWarning`.

            .. deprecated:: 2.6.0
               Use the :py:meth:`khoros.core.Khoros.Category.get_total_count` method instead.

            :returns: The total number of categories as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            deprecation_msg = "The 'categories.get_total_category_count' method has been replaced with the " \
                              "'categories.get_total_count' method and will be removed in a future release."
            logger.warn(deprecation_msg)
            warnings.warn(deprecation_msg, DeprecationWarning)
            return self.get_total_count()

        def category_exists(self, category_id=None, category_url=None):
            """This method checks to see if a category exists.

            .. versionadded:: 2.7.0

            :param category_id: The ID of the category to check
            :type category_id: str, None
            :param category_url: The URL of the category to check
            :type category_url: str, None
            :returns: Boolean value indicating whether or not the category already exists
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.category_exists(self.khoros_object, category_id, category_url)

        def get_category_details(self, identifier, first_item=True):
            """This method returns a dictionary of community configuration settings.

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
            """This method returns a specific community field from the Khoros Community API.

            .. versionadded:: 2.1.0

            :param field: The field whose value to return from the :py:class:`khoros.structures.base.Mapping` class
            :type field: str
            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type category_details: dict, None
            :returns: The requested field in its native format
            :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_category_field(self.khoros_object, field, identifier,
                                                                   category_details)

        def get_url(self, category_id=None, category_details=None):
            """This method retrieves the URL of a given category.

            .. versionadded:: 2.1.0

            :param category_id: The ID of the category to be evaluated (optional if ``category_details`` provided)
            :type category_id: str, None
            :param category_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type category_details: dict, None
            :returns: The full URL of the category
            :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_url(self.khoros_object, category_id, category_details)

        def get_title(self, identifier=None, full_title=True, short_title=False, category_details=None):
            """This method retrieves the full and/or short title of the category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param full_title: Return the full title of the environment (``True`` by default)
            :type full_title: bool
            :param short_title: Return the short title of the environment (``False`` by default)
            :type short_title: bool
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The title(s) of the environment as a string or a tuple of strings
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_title(self.khoros_object, identifier, full_title, short_title,
                                                          category_details)

        def get_description(self, identifier=None, category_details=None):
            """This method retrieves the description for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The description in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_description(self.khoros_object, identifier, category_details)

        def get_parent_type(self, identifier=None, category_details=None):
            """This method retrieves the parent type for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The parent type in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_parent_type(self.khoros_object, identifier, category_details)

        def get_parent_id(self, identifier=None, category_details=None):
            """This method retrieves the parent ID for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The parent ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_parent_id(self.khoros_object, identifier, category_details)

        def get_parent_url(self, identifier=None, category_details=None):
            """This method retrieves the parent URL for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The parent URL in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_parent_url(self.khoros_object, identifier, category_details)

        def get_root_type(self, identifier=None, category_details=None):
            """This method retrieves the root category type for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The root category type in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_root_type(self.khoros_object, identifier, category_details)

        def get_root_id(self, identifier=None, category_details=None):
            """This method retrieves the root category ID for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The root category ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_root_id(self.khoros_object, identifier, category_details)

        def get_root_url(self, identifier=None, category_details=None):
            """This method retrieves the root category URL for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The root category URL in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_root_url(self.khoros_object, identifier, category_details)

        def get_language(self, identifier=None, category_details=None):
            """This method retrieves the defined language for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The language (e.g. ``en``) in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_language(self.khoros_object, identifier, category_details)

        def is_hidden(self, identifier=None, category_details=None):
            """This method identifies whether or not a given category is hidden.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: Boolean value indicating if the category is hidden
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.is_hidden(self.khoros_object, identifier, category_details)

        def get_views(self, identifier=None, category_details=None):
            """This method retrieves the total view count for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The total number of views
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_views(self.khoros_object, identifier, category_details)

        def friendly_date_enabled(self, identifier=None, category_details=None):
            """This method identifies if friendly dates are enabled for a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: Boolean indicating if friendly dates are enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.friendly_date_enabled(self.khoros_object, identifier, category_details)

        def get_friendly_date_max_age(self, identifier=None, category_details=None):
            """This method retrieves the maximum age where friendly dates should be used (if enabled) for a category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: Integer representing the number of days the friendly date feature should be leveraged if enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_friendly_date_max_age(self, identifier, category_details)

        def get_active_skin(self, identifier=None, category_details=None):
            """This method retrieves the skin being used with a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The name of the active skin in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_active_skin(self.khoros_object, identifier, category_details)

        def get_depth(self, identifier=None, category_details=None):
            """This method retrieves the depth of a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The depth of the category as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_depth(self.khoros_object, identifier, category_details)

        def get_position(self, identifier=None, category_details=None):
            """This method retrieves the position of a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The position of the category as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.categories.get_position(self.khoros_object, identifier, category_details)

        def get_creation_date(self, identifier=None, category_details=None):
            """This method retrieves the creation date of a given category.

            .. versionadded:: 2.1.0

            :param identifier: The Category ID or Category URL with which to identify the category
            :type identifier: str, None
            :param category_details: Dictionary containing community details (optional)
            :type category_details: dict, None
            :returns: The creation of the category in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            # TODO: Allow a format to be specified and the ability to parse as a datetime object if needed
            return structures_module.categories.get_creation_date(self.khoros_object, identifier, category_details)

    class Community(object):
        """This class includes methods for interacting with the overall Khoros Community."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Community` inner class object.

            .. versionadded:: 2.1.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def get_community_details(self):
            """This method returns a dictionary of community configuration settings.

            .. versionadded:: 2.1.0

            :returns: The community details within a dictionary
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_community_details(self.khoros_object)

        def get_community_field(self, field, community_details=None):
            """This method retrieves a particular field from the community collection in the API.

            .. versionadded:: 2.1.0

            :param field: The field whose value to return from the :py:class:`khoros.structures.base.Mapping` class
            :type field: str
            :param community_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type community_details: dict, None
            :returns: The requested field in its native format
            :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.communities.get_community_field(self.khoros_object, field, community_details)

        def get_tenant_id(self, community_details=None):
            """This method retrieves the tenant ID of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The tenant ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_tenant_id(self.khoros_object, community_details)

        def get_title(self, full_title=True, short_title=False, community_details=None):
            """This method retrieves the full and/or short title of the environment.

            .. versionadded:: 2.1.0

            :param full_title: Return the full title of the environment (``True`` by default)
            :type full_title: bool
            :param short_title: Return the short title of the environment (``False`` by default)
            :type short_title: bool
            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The title(s) of the environment as a string or a tuple of strings
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_title(self.khoros_object, full_title, short_title,
                                                           community_details)

        def get_description(self, community_details=None):
            """This method retrieves the description of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The description in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_description(self.khoros_object, community_details)

        def get_primary_url(self, community_details=None):
            """This method retrieves the primary URL of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The primary URL in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_primary_url(self.khoros_object, community_details)

        def get_max_attachments(self, community_details=None):
            """This method retrieves the maximum number of attachments permitted per message within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The value as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_max_attachments(self.khoros_object, community_details)

        def get_permitted_attachment_types(self, community_details=None):
            """This method retrieves the attachment file types permitted within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The permitted file types within a list
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_permitted_attachment_types(self.khoros_object, community_details)

        def email_confirmation_required_to_post(self, community_details=None):
            """This method identifies if an email configuration is required before posting in the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: Boolean value indicating if email configuration is required before posting
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.email_confirmation_required_to_post(self.khoros_object,
                                                                                     community_details)

        def get_language(self, community_details=None):
            """This method retrieves the language (e.g. ``en``) utilized in the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The language code as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_language(self.khoros_object, community_details)

        def get_ooyala_player_branding_id(self, community_details=None):
            """This method retrieves the branding ID for the Ooyala Player utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The branding ID in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_ooyala_player_branding_id(self.khoros_object, community_details)

        def get_date_pattern(self, community_details=None):
            """This method retrieves the date pattern (e.g. ``yyyy-MM-dd``) utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The date pattern in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_date_pattern(self.khoros_object, community_details)

        def friendly_date_enabled(self, community_details=None):
            """This method if the friendly date functionality is utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: Boolean value indicating if the feature is enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.friendly_date_enabled(self.khoros_object, community_details)

        def get_friendly_date_max_age(self, community_details=None):
            """This method identifies if the friendly date functionality is utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: Boolean value indicating if the feature is enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_friendly_date_max_age(self.khoros_object, community_details)

        def get_active_skin(self, community_details=None):
            """This method retrieves the primary active skin that is utilized within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The skin name as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_active_skin(self.khoros_object, community_details)

        def get_sign_out_url(self, community_details=None):
            """This method retrieves the Sign Out URL for the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The Sign Out URL as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.get_sign_out_url(self.khoros_object, community_details)

        def get_creation_date(self, community_details=None):
            """This method retrieves the timestamp for the initial creation of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: The creation date as a string (e.g. ``2020-02-03T22:41:36.408-08:00``)
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            # TODO: Allow a format to be specified and the ability to parse as a datetime object if needed
            return structures_module.communities.get_creation_date(self.khoros_object, community_details)

        def top_level_categories_enabled(self, community_details=None):
            """This method identifies if top level categories are enabled within the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: Boolean value indicating if top level categories are enabled
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.top_level_categories_enabled(self.khoros_object, community_details)

        def show_community_node_in_breadcrumb(self, community_details=None):
            """This method identifies if the community node should be shown in breadcrumbs.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: Boolean value indicating if the community node is displayed in bredcrumbs
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.show_community_node_in_breadcrumb(self.khoros_object,
                                                                                   community_details)

        def show_breadcrumb_at_top_level(self, community_details=None):
            """This method identifies if breadcrumbs should be shown at the top level of the environment.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: Boolean value indicating if breadcrumbs are displayed at the top level of the environment
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.show_breadcrumb_at_top_level(self.khoros_object, community_details)

        def top_level_categories_on_community_page(self, community_details=None):
            """This method identifies if top level categories are enabled on community pages.

            .. versionadded:: 2.1.0

            :param community_details: Dictionary containing community details (optional)
            :type community_details: dict, None
            :returns: Boolean value indicating if top level categories are enabled on community pages
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.communities.top_level_categories_on_community_page(self.khoros_object,
                                                                                        community_details)

    class GroupHub(object):
        """This class includes methods for interacting with group hubs."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.GroupHub` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def create(self, group_id, group_title, description=None, membership_type=None, open_group=None,
                   closed_group=None, hidden_group=None, discussion_styles=None, enable_blog=None, enable_contest=None,
                   enable_forum=None, enable_idea=None, enable_qanda=None, enable_tkb=None, all_styles_default=True,
                   parent_category_id=None, avatar_image_path=None, full_response=None, return_id=None, return_url=None,
                   return_api_url=None, return_http_code=None, return_status=None, return_error_messages=None,
                   split_errors=False):
            """This method creates a new group hub within a Khoros Community environment.

            .. versionadded:: 2.6.0

            :param group_id: The unique identifier (i.e. ``id`` field) for the new group hub **(Required)**
            :type group_id: str, int
            :param group_title: The title of the group hub **(Required)**
            :type group_title: str
            :param description: A brief description of the group hub
            :type description: str, None
            :param membership_type: The ``membership_type`` value (``open``, ``closed`` or ``closed_hidden``)
            :type membership_type: dict, None
            :param open_group: Defines the group hub as an open group
            :type open_group: bool, None
            :param closed_group: Defines the group hub as a closed group
            :type closed_group: bool, None
            :param hidden_group: Defines the group hub as a closed and hidden group
            :type hidden_group: bool, None
            :param discussion_styles: A list of discussion styles that will be permitted in the group hub
            :type discussion_styles: list, None
            :param enable_blog: Defines that the **blog** discussion style should be enabled for the group hub
            :type enable_blog: bool, None
            :param enable_contest: Defines that the **contest** discussion style should be enabled for the group hub
            :type enable_contest: bool, None
            :param enable_forum: Defines that the **forum** discussion style should be enabled for the group hub
            :type enable_forum: bool, None
            :param enable_idea: Defines that the **idea** discussion style should be enabled for the group hub
            :type enable_idea: bool, None
            :param enable_qanda: Defines that the **Q&A** (``qanda``) discussion style should be enabled for
                                 the group hub
            :type enable_qanda: bool, None
            :param enable_tkb: Defines that the **TKB** (``tkb``) discussion style should be enabled for
                               the group hub
            :type enable_tkb: bool, None
            :param all_styles_default: Enables all discussion styles if not otherwise specified
            :type all_styles_default: bool
            :param parent_category_id: The parent category identifier (if applicable)
            :type parent_category_id: str, int, None
            :param avatar_image_path: The file path to the avatar image to be uploaded (if applicable)
            :type avatar_image_path: str, None
            :param full_response: Determines whether the full, raw API response should be returned by the function

                                  .. caution:: This argument overwrites the ``return_id``, ``return_url``,
                                               ``return_api_url``, ``return_http_code``, ``return_status`` and
                                               ``return_error_messages`` arguments.

            :type full_response: bool, None
            :param return_id: Determines if the **ID** of the new group hub should be returned by the function
            :type return_id: bool, None
            :param return_url: Determines if the **URL** of the new group hub should be returned by the function
            :type return_url: bool, None
            :param return_api_url: Determines if the **API URL** of the new group hub should be returned by the function
            :type return_api_url: bool, None
            :param return_http_code: Determines if the **HTTP Code** of the API response should be returned by
                                     the function
            :type return_http_code: bool, None
            :param return_status: Determines if the **Status** of the API response should be returned by the function
            :type return_status: bool, None
            :param return_error_messages: Determines if any error messages associated with the API response should
                                          be returned by the function
            :type return_error_messages: bool, None
            :param split_errors: Defines whether or not error messages should be merged when applicable
            :type split_errors: bool
            :returns: Boolean value indicating a successful outcome (default), the full API response or one or more
                      specific fields defined by function arguments
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`
            """
            return structures_module.grouphubs.create(self.khoros_object, group_id, group_title, description,
                                                      membership_type, open_group, closed_group, hidden_group,
                                                      discussion_styles, enable_blog, enable_contest, enable_forum,
                                                      enable_idea, enable_qanda, enable_tkb, all_styles_default,
                                                      parent_category_id, avatar_image_path, full_response,
                                                      return_id, return_url, return_api_url, return_http_code,
                                                      return_status, return_error_messages, split_errors)

        def structure_payload(self, group_id, group_title, description=None, membership_type=None, open_group=None,
                              closed_group=None, hidden_group=None, discussion_styles=None, enable_blog=None,
                              enable_contest=None, enable_forum=None, enable_idea=None, enable_qanda=None,
                              enable_tkb=None, all_styles_default=True, parent_category_id=None):
            """This method structures the payload to use in a Group Hub API request.

            .. versionadded:: 2.6.0

            :param group_id: The unique identifier (i.e. ``id`` field) for the new group hub **(Required)**
            :type group_id: str, int
            :param group_title: The title of the group hub **(Required)**
            :type group_title: str
            :param description: A brief description of the group hub
            :type description: str, None
            :param membership_type: The ``membership_type`` value (``open``, ``closed`` or ``closed_hidden``)
            :type membership_type: dict, None
            :param open_group: Defines the group hub as an open group
            :type open_group: bool, None
            :param closed_group: Defines the group hub as a closed group
            :type closed_group: bool, None
            :param hidden_group: Defines the group hub as a closed and hidden group
            :type hidden_group: bool, None
            :param discussion_styles: A list of discussion styles that will be permitted in the group hub
            :type discussion_styles: list, None
            :param enable_blog: Defines if the **blog** discussion style should be enabled for the group hub
            :type enable_blog: bool, None
            :param enable_contest: Defines if the **contest** discussion style should be enabled for the group hub
            :type enable_contest: bool, None
            :param enable_forum: Defines if the **forum** discussion style should be enabled for the group hub
            :type enable_forum: bool, None
            :param enable_idea: Defines if the **idea** discussion style should be enabled for the group hub
            :type enable_idea: bool, None
            :param enable_qanda: Defines if the **Q&A** (``qanda``) discussion style should be enabled for the group hub
            :type enable_qanda: bool, None
            :param enable_tkb: Defines if the **TKB** (``tkb``) discussion style should be enabled for the group hub
            :type enable_tkb: bool, None
            :param all_styles_default: Defines if all discussion styles should be enabled if not otherwise specified
            :type all_styles_default: bool
            :param parent_category_id: The parent category identifier (if applicable)
            :type parent_category_id: str, int, None
            :returns: The properly formatted payload for the API request
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError`
            """
            return structures_module.grouphubs.structure_payload(self.khoros_object, group_id, group_title, description,
                                                                 membership_type, open_group, closed_group,
                                                                 hidden_group, discussion_styles, enable_blog,
                                                                 enable_contest, enable_forum, enable_idea,
                                                                 enable_qanda, enable_tkb, all_styles_default,
                                                                 parent_category_id)

        def get_total_count(self):
            """This method returns the total number of group hubs within the Khoros Community environment.

            :returns: The total number of group hubs as an integer
            """
            return structures_module.grouphubs.get_total_count(self.khoros_object)

        def grouphub_exists(self, grouphub_id=None, grouphub_url=None):
            """This method checks to see if a group hub exists.

            .. versionadded:: 2.7.0

            :param grouphub_id: The ID of the group hub to check
            :type grouphub_id: str, None
            :param grouphub_url: The URL of the group hub to check
            :type grouphub_url: str, None
            :returns: Boolean value indicating whether or not the group hub already exists
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.grouphubs.grouphub_exists(self.khoros_object, grouphub_id, grouphub_url)

        def update_title(self, new_title, group_hub_id=None, group_hub_url=None, full_response=None, return_id=None,
                         return_url=None, return_api_url=None, return_http_code=None, return_status=None,
                         return_error_messages=None, split_errors=False):
            """This method updates the title of an existing group hub.

            .. versionadded:: 2.6.0

            :param new_title: The new title for the group hub
            :type new_title: str
            :param group_hub_id: The group hub ID that identifies the group hub to update
                                 (necessary if URL not provided)
            :type group_hub_id: str, None
            :param group_hub_url: The group hub URL that identifies the group hub to update
                                  (necessary if ID not provided)
            :type group_hub_url: str, None
            :param full_response: Determines whether the full, raw API response should be returned by the function

                                  .. caution:: This argument overwrites the ``return_id``, ``return_url``,
                                               ``return_api_url``, ``return_http_code``, ``return_status`` and
                                               ``return_error_messages`` arguments.

            :type full_response: bool, None
            :param return_id: Determines if the **ID** of the new group hub should be returned by the function
            :type return_id: bool, None
            :param return_url: Determines if the **URL** of the new group hub should be returned by the function
            :type return_url: bool, None
            :param return_api_url: Determines if the **API URL** of the new group hub should be returned
                                   by the function
            :type return_api_url: bool, None
            :param return_http_code: Determines if the **HTTP Code** of the API response should be returned
                                     by the function
            :type return_http_code: bool, None
            :param return_status: Determines if the **Status** of the API response should be returned by the function
            :type return_status: bool, None
            :param return_error_messages: Determines if any error messages associated with the API response should be
                                          returned by the function
            :type return_error_messages: bool, None
            :param split_errors: Defines whether or not error messages should be merged when applicable
            :type split_errors: bool
            :returns: Boolean value indicating a successful outcome (default), the full API response or one or more
                      specific fields defined by function arguments
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.PUTRequestError`
            """
            return structures_module.grouphubs.update_title(self.khoros_object, new_title, group_hub_id,
                                                            group_hub_url, full_response, return_id, return_url,
                                                            return_api_url, return_http_code, return_status,
                                                            return_error_messages, split_errors)

    class Message(object):
        """This class includes methods for interacting with messages."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Message` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def create(self, subject=None, body=None, node=None, node_id=None, node_url=None, canonical_url=None,
                   context_id=None, context_url=None, cover_image=None, images=None, is_answer=None, is_draft=None,
                   labels=None, product_category=None, products=None, read_only=None, seo_title=None,
                   seo_description=None, tags=None, ignore_non_string_tags=False, teaser=None, topic=None, videos=None,
                   attachment_file_paths=None, full_payload=None, full_response=None, return_id=None, return_url=None,
                   return_api_url=None, return_http_code=None, return_status=None, return_error_messages=None,
                   split_errors=False, proxy_user_object=None):
            """This method creates a new message within a given node.

            .. versionchanged:: 4.4.0
               Introduced the ``proxy_user_object`` parameter to allow messages to be created on behalf of other users.

            .. versionchanged:: 4.3.0
               It is now possible to pass the pre-constructed full JSON payload into the function via the
               ``full_payload`` parameter as an alternative to defining each field individually.

            .. versionchanged:: 2.8.0
               The ``ignore_non_string_tags``, ``return_status``, ``return_error_messages`` and ``split_errors``
               arguments were introduced.

            .. versionadded:: 2.3.0

            :param subject: The title or subject of the message
            :type subject: str, None
            :param body: The body of the message in HTML format
            :type body: str, None
            :param node: A dictionary containing the ``id`` key and its associated value indicating the destination
            :type node: dict, None
            :param node_id: The ID of the node in which the message will be published
            :type node_id: str, None
            :param node_url: The URL of the node in which the message will be published

                             .. note:: This argument is necessary in the absence of the ``node`` and ``node_id``
                                       arguments.

            :type node_url: str, None
            :param canonical_url: The search engine-friendly URL to the message
            :type canonical_url: str, None
            :param context_id: Metadata on a message to identify the message with an external identifier of your choice
            :type context_id: str, None
            :param context_url: Metadata on a message representing a URL to associate with the message
                                (external identifier)
            :type context_url: str, None
            :param cover_image: The cover image set for the message
            :type cover_image: dict, None
            :param images: The query to retrieve images uploaded to the message
            :type images: dict, None
            :param is_answer: Designates the message as an answer on a Q&A board
            :type is_answer: bool, None
            :param is_draft: Indicates whether or not the message is still a draft (i.e. unpublished)
            :type is_draft: bool, None
            :param labels: The query to retrieve labels applied to the message
            :type labels: dict, None
            :param product_category: The product category (i.e. container for ``products``) associated with the message
            :type product_category: dict, None
            :param products: The product in a product catalog associated with the message
            :type products: dict, None
            :param read_only: Indicates whether or not the message should be read-only or have replies/comments blocked
            :type read_only: bool, None
            :param seo_title: The title of the message used for SEO purposes
            :type seo_title: str, None
            :param seo_description: A description of the message used for SEO purposes
            :type seo_description: str, None
            :param tags: The query to retrieve tags applied to the message
            :type tags: dict, None
            :param ignore_non_string_tags: Determines if non-strings (excluding iterables) should be ignored rather than
                                           converted to strings (``False`` by default)
            :type ignore_non_string_tags: bool
            :param teaser: The message teaser (used with blog articles)
            :type teaser: str, None
            :param topic: The root message of the conversation in which the message appears
            :type topic: dict, None
            :param videos: The query to retrieve videos uploaded to the message
            :type videos: dict, None
            :param attachment_file_paths: The full path(s) to one or more attachment (e.g. ``path/to/file1.pdf``)
            :type attachment_file_paths: str, tuple, list, set, None
            :param full_payload: Pre-constructed full JSON payload as a dictionary (*preferred*) or a JSON string with
                                 the following syntax:

                                    .. code-block:: json

                                       {
                                         "data": {
                                           "type": "message",

                                         }
                                       }

                                 .. note:: The ``type`` field shown above is essential for the payload to be valid.

            :type full_payload: dict, str, None
            :param full_response: Defines if the full response should be returned instead of the outcome
                                  (``False`` by default)

                                  .. caution:: This argument overwrites the ``return_id``, ``return_url``,
                                               ``return_api_url`` and ``return_http_code`` arguments.

            :type full_response: bool, None
            :param return_id: Indicates that the **Message ID** should be returned (``False`` by default)
            :type return_id: bool, None
            :param return_url: Indicates that the **Message URL** should be returned (``False`` by default)
            :type return_url: bool, None
            :param return_api_url: Indicates that the **API URL** of the message should be returned
                                   (``False`` by default)
            :type return_api_url: bool, None
            :param return_http_code: Indicates that the **HTTP status code** of the response should be returned
                                     (``False`` by default)
            :type return_http_code: bool, None
            :param return_status: Determines if the **Status** of the API response should be returned by the function
            :type return_status: bool, None
            :param return_error_messages: Determines if the **Developer Response Message** (if any) associated with the
                                          API response should be returned by the function
            :type return_error_messages: bool, None
            :param split_errors: Defines whether or not error messages should be merged when applicable
            :type split_errors: bool
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to create
                                      the message on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: Boolean value indicating a successful outcome (default) or the full API response
            :raises: :py:exc:`TypeError`, :py:exc:`ValueError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.DataMismatchError`
            """
            return objects_module.messages.create(self.khoros_object, subject, body, node, node_id, node_url,
                                                  canonical_url, context_id, context_url, cover_image, images,
                                                  is_answer, is_draft, labels, product_category, products, read_only,
                                                  seo_title, seo_description, tags, ignore_non_string_tags, teaser,
                                                  topic, videos, attachment_file_paths, full_payload, full_response,
                                                  return_id, return_url, return_api_url, return_http_code,
                                                  return_status, return_error_messages, split_errors, proxy_user_object)

        def update(self, msg_id=None, msg_url=None, subject=None, body=None, node=None, node_id=None, node_url=None,
                   canonical_url=None, context_id=None, context_url=None, cover_image=None, is_draft=None, labels=None,
                   moderation_status=None, parent=None, product_category=None, products=None, read_only=None,
                   topic=None, status=None, seo_title=None, seo_description=None, tags=None, overwrite_tags=False,
                   ignore_non_string_tags=False, teaser=None, attachments_to_add=None, attachments_to_remove=None,
                   full_response=None, return_id=None, return_url=None, return_api_url=None, return_http_code=None,
                   return_status=None, return_error_messages=None, split_errors=False, proxy_user_object=None):
            """This method updates one or more elements of an existing message.

            .. versionchanged:: 4.4.0
               Introduced the ``proxy_user_object`` parameter to allow messages to be updated on behalf of other users.

            .. versionadded:: 2.8.0

            :param msg_id: The ID of the existing message
            :type msg_id: str, int, None
            :param msg_url: The URL of the existing message
            :type msg_url: str, None
            :param subject: The title or subject of the message
            :type subject: str, None
            :param body: The body of the message in HTML format
            :type body: str, None
            :param node: A dictionary containing the ``id`` key and its associated value indicating the destination
            :type node: dict, None
            :param node_id: The ID of the node in which the message will be published
            :type node_id: str, None
            :param node_url: The URL of the node in which the message will be published

                             .. note:: This argument is necessary in the absence of the ``node`` and ``node_id``
                                       arguments.

            :type node_url: str, None
            :param canonical_url: The search engine-friendly URL to the message
            :type canonical_url: str, None
            :param context_id: Metadata on a message to identify the message with an external identifier of
                               your choosing
            :type context_id: str, None
            :param context_url: Metadata on a message representing a URL to associate with the message
                                (external identifier)
            :type context_url: str, None
            :param cover_image: The cover image set for the message
            :type cover_image: dict, None
            :param is_draft: Indicates whether or not the message is still a draft (i.e. unpublished)
            :type is_draft: bool, None
            :param labels: The query to retrieve labels applied to the message
            :type labels: dict, None
            :param moderation_status: The moderation status of the message

                                      .. note:: Acceptable values are ``unmoderated``, ``approved``, ``rejected``,
                                                ``marked_undecided``, ``marked_approved`` and ``marked_rejected``.

            :type moderation_status: str, None
            :param parent: The parent of the message
            :type parent: str, None
            :param product_category: The product category (i.e. container for ``products``) associated with the message
            :type product_category: dict, None
            :param products: The product in a product catalog associated with the message
            :type products: dict, None
            :param read_only: Indicates whether or not the message should be read-only or have replies/comments blocked
            :type read_only: bool, None
            :param topic: The root message of the conversation in which the message appears
            :type topic: dict, None
            :param status: The message status for messages where conversation.style is ``idea`` or ``contest``

                           .. caution:: This property is not returned if the message has the default ``Unspecified``
                                        status assigned. It will only be returned for ideas with a status of Completed
                                        or with a custom status created in Community Admin.

            :type status: dict, None
            :param seo_title: The title of the message used for SEO purposes
            :type seo_title: str, None
            :param seo_description: A description of the message used for SEO purposes
            :type seo_description: str, None
            :param tags: The query to retrieve tags applied to the message
            :type tags: dict, None
            :param overwrite_tags: Determines if tags should overwrite any existing tags (where applicable) or if the
                                   tags should be appended to the existing tags (default)
            :type overwrite_tags: bool
            :param ignore_non_string_tags: Determines if non-strings (excluding iterables) should be ignored rather than
                                           converted to strings (``False`` by default)
            :type ignore_non_string_tags: bool
            :param teaser: The message teaser (used with blog articles)
            :type teaser: str, None
            :param attachments_to_add: The full path(s) to one or more attachments (e.g. ``path/to/file1.pdf``) to be
                                           added to the message
            :type attachments_to_add: str, tuple, list, set, None
            :param attachments_to_remove: One or more attachments to remove from the message

                                          .. note:: Each attachment should specify the attachment id of the attachment
                                                    to remove, which begins with ``m#_``. (e.g. ``m283_file1.pdf``)

            :type attachments_to_remove: str, tuple, list, set, None
            :param full_response: Defines if the full response should be returned instead of the outcome
                                  (``False`` by default)

                                  .. caution:: This argument overwrites the ``return_id``, ``return_url``,
                                               ``return_api_url`` and ``return_http_code`` arguments.

            :type full_response: bool, None
            :param return_id: Indicates that the **Message ID** should be returned (``False`` by default)
            :type return_id: bool, None
            :param return_url: Indicates that the **Message URL** should be returned (``False`` by default)
            :type return_url: bool, None
            :param return_api_url: Indicates that the **API URL** of the message should be returned
                                   (``False`` by default)
            :type return_api_url: bool, None
            :param return_http_code: Indicates that the **HTTP status code** of the response should be returned
                                     (``False`` by default)
            :type return_http_code: bool, None
            :param return_status: Determines if the **Status** of the API response should be returned by the function
            :type return_status: bool, None
            :param return_error_messages: Determines if the **Developer Response Message** (if any) associated with the
                   API response should be returned by the function
            :type return_error_messages: bool, None
            :param split_errors: Defines whether or not error messages should be merged when applicable
            :type split_errors: bool
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to create
                                      the message on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: Boolean value indicating a successful outcome (default) or the full API response
            :raises: :py:exc:`TypeError`, :py:exc:`ValueError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.DataMismatchError`
            """
            return objects_module.messages.update(self.khoros_object, msg_id, msg_url, subject, body, node, node_id,
                                                  node_url, canonical_url, context_id, context_url, cover_image,
                                                  is_draft, labels, moderation_status, parent, product_category,
                                                  products, read_only, topic, status, seo_title, seo_description, tags,
                                                  overwrite_tags, ignore_non_string_tags, teaser, attachments_to_add,
                                                  attachments_to_remove, full_response, return_id, return_url,
                                                  return_api_url, return_http_code, return_status,
                                                  return_error_messages, split_errors, proxy_user_object)

        @staticmethod
        def parse_v2_response(json_response, return_dict=False, status=False, response_msg=False, http_code=False,
                              message_id=False, message_url=False, message_api_uri=False, v2_base=''):
            """This method parses an API response for a message operation (e.g. creating a message) and returns data.

            .. versionchanged:: 3.3.2
               Added logging for the :py:exc:`DeprecationWarning`.

            .. versionchanged:: 3.2.0
               The lower-level function call now utilizes keyword arguments to fix an argument mismatch issue.

            .. deprecated:: 2.5.0
               Use the :py:func:`khoros.core.Khoros.parse_v2_response` function instead.

            .. versionadded:: 2.3.0

            :param json_response: The API response in JSON format
            :type json_response: dict
            :param return_dict: Defines if the parsed data should be returned within a dictionary
            :type return_dict: bool
            :param status: Defines if the **status** value should be returned
            :type status: bool
            :param response_msg: Defines if the **developer response** message should be returned
            :type response_msg: bool
            :param http_code: Defines if the **HTTP status code** should be returned
            :type http_code: bool
            :param message_id: Defines if the **message ID** should be returned
            :type message_id: bool
            :param message_url: Defines if the **message URL** should be returned
            :type message_url: bool
            :param message_api_uri: Defines if the ** message API URI** should be returned
            :type message_api_uri: bool
            :param v2_base: The base URL for the API v2
            :type v2_base: str
            :returns: A string, tuple or dictionary with the parsed data
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            deprecation_msg = "The 'messages.parse_v2_response' method is deprecated and the 'parse_v2_response' " \
                              "method should be used instead."
            warnings.warn(deprecation_msg, DeprecationWarning)
            logger.warn(deprecation_msg)
            dev_msg = response_msg
            return api.parse_v2_response(json_response, return_dict, status, response_msg, dev_msg, http_code=http_code,
                                         data_id=message_id, data_url=message_url, data_api_uri=message_api_uri,
                                         v2_base=v2_base)

        @staticmethod
        def validate_message_payload(payload):
            """This method validates the payload for a message to ensure that it can be successfully utilized.

            .. versionadded:: 4.3.0

            :param payload: The message payload to be validated as a dictionary (*preferred*) or a JSON string.
            :type payload: dict, str
            :returns: The payload as a dictionary
            :raises: :py:exc:`khoros.errors.exceptions.InvalidMessagePayloadError`
            """
            return objects_module.messages.validate_message_payload(payload)

        def get_metadata(self, msg_id, metadata_key):
            """This method retrieves the value for a specific metadata key associated with a given message.

            .. versionadded:: 4.5.0

            :param msg_id: The ID of the message for which the metadata will be retrieved
            :type msg_id: str, int
            :param metadata_key: The metadata key for which the value will be retrieved
            :type metadata_key: str
            :returns: The metadata value
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError',
                     :py:exc:`khoros.errors.exceptions.InvalidMetadataError`,
                     :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.messages.get_metadata(self.khoros_object, msg_id, metadata_key)

        def format_content_mention(self, content_info=None, content_id=None, title=None, url=None):
            """This method formats the ``<li-message>`` HTML tag for a content @mention.

            .. versionadded:: 2.4.0

            :param content_info: A dictionary containing the ``'id'`` and/or ``'login'`` key(s) with the user data

                                 .. note:: This argument is necessary if the Title and URL are not explicitly passed
                                           using the ``title`` and ``url`` function arguments.

            :type content_info: dict, None
            :param content_id: The Message ID (aka Content ID) associated with the content mention

                               .. note:: This is an optional argument as the ID can be retrieved from the URL.

            :type content_id: str, int, None
            :param title: The display title for the content mention (e.g. ``"Click Here"``)
            :type title: str, None
            :param url: The fully-qualified URL of the message being mentioned
            :type url: str, None
            :returns: The properly formatted ``<li-message>`` HTML tag in string format
            :raises: :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.MessageTypeNotFoundError`,
                     :py:exc:`khoros.errors.exceptions.InvalidURLError`
            """
            return objects_module.messages.format_content_mention(self.khoros_object, content_info, content_id,
                                                                  title, url)

        def format_user_mention(self, user_info=None, user_id=None, login=None):
            """This method formats the ``<li-user>`` HTML tag for a user @mention.

            .. versionadded:: 2.4.0

            :param user_info: A dictionary containing the ``'id'`` and/or ``'login'`` key(s) with the user information

                              .. note:: This argument is necessary if the User ID and/or Login are not explicitly passed
                                        using the ``user_id`` and/or ``login`` function arguments.

            :type user_info: dict, None
            :param user_id: The unique user identifier (i.e. User ID) for the user
            :type user_id: str, int, None
            :param login: The login (i.e. username) for the user
            :type login: str, None
            :returns: The properly formatted ``<li-user>`` HTML tag in string format
            :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return objects_module.messages.format_user_mention(self.khoros_object, user_info, user_id, login)

    class Node(object):
        """This class includes methods for interacting with nodes."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Node` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        @staticmethod
        def get_node_id(url, node_type=None):
            """This method retrieves the Node ID for a given node within a URL.

            :param url: The URL from which to parse out the Node ID
            :type url: str
            :param node_type: The node type (e.g. ``blog``, ``tkb``, ``message``, etc.) for the object in the URL
            :type node_type: str, None
            :returns: The Node ID retrieved from the URL
            :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
                     :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`,
                     :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
            """
            return structures_module.nodes.get_node_id(url, node_type)

        @staticmethod
        def get_node_type_from_url(url):
            """This method attempts to retrieve a node type by analyzing a supplied URL.

            :param url: The URL from which to extract the node type
            :type url: str
            :returns: The node type based on the URL provided
            :raises: :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
            """
            return structures_module.nodes.get_node_type_from_url(url)

        def get_total_node_count(self):
            """This method returns the total number of nodes within the Khoros Community environment.

            :returns: The total number of nodes as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return structures_module.nodes.get_total_node_count(self.khoros_object)

        def node_exists(self, node_id=None, node_url=None):
            """This method checks to see if a node exists.

            .. versionadded:: 2.7.0

            :param node_id: The ID of the node to check
            :type node_id: str, None
            :param node_url: The URL of the node to check
            :type node_url: str, None
            :returns: Boolean value indicating whether or not the node already exists
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.node_exists(self.khoros_object, node_id, node_url)

        def get_node_details(self, identifier, first_item=True):
            """This method returns a dictionary of node configuration settings.

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
            """This method returns a specific node field from the Khoros Community API.

            .. versionadded:: 2.1.0

            :param field: The field to return from the :py:class:`khoros.structures.base.Mapping` class
            :type field: str
            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The requested field in its native format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_node_field(self.khoros_object, field, identifier, node_details)

        def get_url(self, node_id=None, node_details=None):
            """This method returns the full URL of a given Node ID.

            .. versionadded:: 2.1.0

            :param node_id: The Node ID with which to identify the node
            :type node_id: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The node URl as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_url(self.khoros_object, node_id, node_details)

        def get_type(self, identifier, node_details=None):
            """This method returns the full URL of a given Node ID.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The node URl as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_type(self.khoros_object, identifier, node_details)

        def get_discussion_style(self, identifier, node_details=None):
            """This method returns the full URL of a given Node ID.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The node URl as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_discussion_style(self.khoros_object, identifier, node_details)

        def get_title(self, identifier=None, full_title=True, short_title=False, node_details=None):
            """This method retrieves the full and/or short title of the node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param full_title: Determines if the full title of the node should be returned (``True`` by default)
            :type full_title: bool
            :param short_title: Determines if the short title of the node should be returned (``False`` by default)
            :type short_title: bool
            :param node_details: Dictionary containing node details (optional)
            :type node_details: dict, None
            :returns: The node title(s) as a string or a tuple of strings
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_title(self.khoros_object, identifier, full_title,
                                                     short_title, node_details)

        def get_description(self, identifier, node_details=None):
            """This method returns the description of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The node description as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_description(self.khoros_object, identifier, node_details)

        def get_parent_type(self, identifier, node_details=None):
            """This method returns the parent type of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The parent type as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_parent_type(self.khoros_object, identifier, node_details)

        def get_parent_id(self, identifier, node_details=None, include_prefix=False):
            """This method returns the Parent ID of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
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
            """This method returns the parent URL of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The parent URL as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_parent_url(self.khoros_object, identifier, node_details)

        def get_root_type(self, identifier, node_details=None):
            """This method returns the root category type of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The root category type as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_root_type(self.khoros_object, identifier, node_details)

        def get_root_id(self, identifier, node_details=None, include_prefix=False):
            """This method returns the Root Category ID of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :param include_prefix: Defines if the prefix (e.g. ``category:``) should be included (``False`` by default)
            :type include_prefix: bool
            :returns: The Root Category ID as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_root_id(self.khoros_object, identifier, node_details, include_prefix)

        def get_root_url(self, identifier, node_details=None):
            """This method returns the root category URL of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The root category URL as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_root_url(self.khoros_object, identifier, node_details)

        def get_avatar_url(self, identifier, node_details=None, original=True, tiny=False, small=False,
                           medium=False, large=False):
            """This method retrieves one or more avatar URLs for a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
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
            """This method returns the creation date of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :param friendly: Defines if the "friendly" date (e.g. ``Friday``) should be returned (``False`` by default)
            :type friendly: bool
            :returns: The creation date as a string
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_creation_date(self.khoros_object, identifier, node_details, friendly)

        def get_depth(self, identifier, node_details=None):
            """This method returns the depth of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The depth as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_depth(self.khoros_object, identifier, node_details)

        def get_position(self, identifier, node_details=None):
            """This method returns the position of a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The position as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_position(self.khoros_object, identifier, node_details)

        def is_hidden(self, identifier, node_details=None):
            """This method identifies whether or not a given node is hidden.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: Boolean indicating whether or not the node is hidden
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.is_hidden(self.khoros_object, identifier, node_details)

        def get_views(self, identifier, node_details=None):
            """This method returns the views for a given node.

            .. versionadded:: 2.1.0

            :param identifier: The Node ID or Node URL with which to identify the node
            :type identifier: str, None
            :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
            :type node_details: dict, None
            :returns: The views as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
                     :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return structures_module.nodes.get_views(self.khoros_object, identifier, node_details)

    class Role(object):
        """This class includes methods relating to roles and permissions."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Role` inner class object.

            .. versionadded:: 2.4.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        @staticmethod
        def get_role_id(role_name, scope='community', node_id=None):
            """This method constructs and returns the Role ID associated with a given role name and scope.

            .. versionadded:: 4.0.0

            :param role_name: The name of the role (e.g. ``Administrator``, ``Moderator``, ``Owner``, etc.)
            :type role_name: str
            :param scope: The scope of the role (``community`` by default)
            :type scope: str
            :param node_id: The associated Node ID for any role that does not have a global/community scope.
            :type node_id: str, None
            :returns: The properly constructed Role ID where applicable
            :raises: :py:exc:`khoros.errors.exceptions.InvalidRoleError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return objects_module.roles.get_role_id(role_name, scope, node_id)

        def assign_roles_to_user(self, user, lookup_type='id', roles_to_add=None, node=None, node_type='board',
                                 v1=False, return_json=True):
            """This method assigns a user to one or more roles.

            .. versionadded:: 4.0.0

            :param user: The identifier (i.e. ID, login or email) of the user to be assigned to the role
            :type user: str
            :param lookup_type: The lookup type for the user identifier (``id``, ``login`` or ``email``)
            :type lookup_type: str
            :param roles_to_add: One or more roles (Role IDs or Role Names) to which the user will be assigned
            :type roles_to_add: str, list, tuple, set
            :param node: The Node ID of the node to which the role is scoped when applicable
            :type node: str, None
            :param node_type: The type of node to which the role is scoped
                              (e.g. ``board`` (default), ``category``, etc.)
            :type node_type: str
            :param v1: Determines if the Community API v1 should be used to perform the operation
                       (``False`` by default)
            :type v1: bool
            :param return_json: Determines if the response should be returned as JSON rather than XML
                                (``True`` by default)
            :type return_json: bool
            :returns: The response from the API request
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.CurrentlyUnsupportedError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
                     :py:exc:`khoros.errors.exceptions.UnsupportedNodeTypeError`,
                     :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PUTRequestError`
            """
            return objects_module.roles.assign_roles_to_user(self.khoros_object, user, lookup_type, roles_to_add,
                                                             node, node_type, v1, return_json)

        def get_total_role_count(self, return_dict=False, total=True, top_level=False, board=False,
                                 category=False, group_hub=False):
            """This method retrieves the total role count for one or more role type(s).

            .. versionadded:: 2.4.0

            :param return_dict: Determines if the data should be returned as a dictionary (``False`` by default)
            :type return_dict: bool
            :param total: Indicates that the total overall role count should be returned (``True`` by default)
            :type total: bool
            :param top_level: Indicates that the total top-level role count should be returned (``False`` by default)
            :type top_level: bool
            :param board: Indicates that the total board-level role count should be returned (``False`` by default)
            :type board: bool
            :param category: Indicates that the total category-level role count should be returned
                             (``False`` by default)
            :type category: bool
            :param group_hub: Indicates that the total group hub-level role count should be returned
                              (``False`` by default)
            :type group_hub: bool
            :returns: The role count(s) as an integer, tuple or dictionary, depending on the arguments supplied
            :raises: :py:exc:`khoros.objects.roles.InvalidRoleTypeError`
            """
            return objects_module.roles.get_total_role_count(self.khoros_object, return_dict, total, top_level, board,
                                                             category, group_hub)

        def get_roles_for_user(self, user_id, fields=None):
            """This method returns all roles associated with a given User ID.

            .. versionchanged:: 4.1.0
               The docstring has been updated to reference the correct exception raised by this method.

            .. versionchanged:: 3.5.0
               Fields to return in the LiQL query can now be explicitly defined.

            .. versionadded:: 2.4.0

            :param user_id: The User ID for which to retrieve the roles data
            :type user_id: str
            :param fields: The field(s) to retrieve from the LiQL query as a string or list

                   .. note:: All fields (i.e. ``SELECT *``) are returned unless fields are explicitly defined.

            :type fields: str, list, tuple, set, None
            :returns: A dictionary with data for each role associated with the given User ID
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.roles.get_roles_for_user(self.khoros_object, user_id, fields)

        def get_users_with_role(self, fields='login', role_id=None, role_name=None, scope=None, node_id=None,
                                limit_per_query=1000, simple=False):
            """This method retrieves a list of all users that have a specific role.

            .. versionadded:: 3.5.0

            :param fields: One or more fields from the ``Users`` object to return (``login`` field by default)
            :type fields: str, tuple, list, set
            :param role_id: The identifier for the role in ``node_type:node_id:role_name`` format
            :type role_id: str, None
            :param role_name: The simple role name (e.g. ``Administrator``)

                              .. caution:: This option should only be used when the role name is unique within the
                                           community at all node levels.

            :type role_name: str, None
            :param scope: The scope of the role (e.g. ``board``, ``category``, ``community``, ``grouphub``)

                          .. note:: If a value is not supplied and only a role name is defined then the role scope is
                                    assumed to be at the ``community`` level. (i.e. global)

            :type scope: str, None
            :param node_id: The Node ID associated with the role (where applicable)

                            .. note:: If a value is not supplied and only a role name is defined then the role scope is
                                      assumed to be at the ``community`` level. (i.e. global)

            :type node_id: str, None
            :param limit_per_query: Defines a ``LIMIT`` constraint other than the default ``1000`` limit per LiQL query

                                    .. note:: Unless modified by Khoros Support or Professional Services, ``1000`` is
                                              the maximum number of entries that can be returned in a single LiQL query.

            :type limit_per_query: int, str
            :param simple: Returns a simple list of the strings or tuples of the value(s) for each user
                           (``False`` by default)
            :type simple: bool
            :returns: A list of users as strings, tuples or dictionaries depending if ``simple`` mode is enabled
            :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`,
                     :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return objects_module.roles.get_users_with_role(self.khoros_object, fields, role_id, role_name, scope,
                                                            node_id, limit_per_query, simple=simple)

    class SAML(object):
        """This class includes methods relating to SAML 2.0 authentication and user provisioning.

        .. versionadded:: 4.3.0
        """
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.SAML` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        @staticmethod
        def import_assertion(file_path, base64_encode=True, url_encode=True):
            """This method imports an XML SAML assertion as a string and optionally base64- and/or URL-encodes it.

            .. versionadded:: 4.3.0

            :param file_path: The file path to the XML file to import
            :type file_path: str
            :param base64_encode: Determines if the assertion should be base64-encoded (``True`` by default)
            :type base64_encode: bool
            :param url_encode: Determines if the assertion should be URL-encoded (``True`` by default)
            :type url_encode: bool
            :returns: The SAML assertion string
            :raises: :py:exc:`FileNotFoundError`
            """
            return saml_module.import_assertion(file_path, base64_encode, url_encode)

        def send_assertion(self, assertion=None, file_path=None, base64_encode=True, url_encode=True):
            """This method sends a SAML assertion as a POST request in order to provision a new user.

            .. versionadded:: 4.3.0

            :param assertion: The SAML assertion in string format and optionally base64- and/or URL-encoded
            :type assertion: str, None
            :param file_path: The file path to the XML file to import that contains the SAML assertion
            :type file_path: str, None
            :param base64_encode: Determines if the assertion should be base64-encoded (``True`` by default)
            :type base64_encode: bool
            :param url_encode: Determines if the assertion should be URL-encoded (``True`` by default)
            :type url_encode: bool
            :returns: The API response from the POST request
            :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return saml_module.send_assertion(self.khoros_object, assertion, file_path, base64_encode, url_encode)

    class Settings(object):
        """This class includes methods relating to the retrieval and defining of various settings.

        .. versionadded:: 3.2.0
        """
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Settings` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def get_node_setting(self, setting_name, node_id, node_type='board', v1=None, convert_json=False):
            """This method retrieves the value of a specific node setting.

            .. versionchanged:: 3.3.2
               The ``convert_json`` parameter has been introduced which optionally converts a JSON string
               into a dictionary.

            .. versionadded:: 3.2.0

            :param setting_name: The name of the setting field for which to retrieve the value
            :type setting_name: str
            :param node_id: The ID of the node associated with the setting to retrieve
            :type node_id: str
            :param node_type: Defines the node as a ``board`` (default), ``category`` or ``grouphub``
            :type node_type: str
            :param v1: Optionally defines a specific Community API version to use when retrieving the value
            :type v1: bool, None
            :param convert_json: Optionally converts a JSON string into a Python dictionary (``False``  by default)
            :type convert_json: bool
            :returns: The value of the setting for the node
            :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.GETRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
                     :py:exc:`khoros.errors.exceptions.LiQLParseError`
            """
            return objects_module.settings.get_node_setting(self.khoros_object, setting_name, node_id, node_type, v1,
                                                            convert_json)

        def define_node_setting(self, setting_name, setting_val, node_id, node_type='board', return_json=True):
            """This method defines a particular setting value for a given node.

            .. versionchanged:: 4.0.0
               The default value for the ``return_json`` parameter is now ``True``.

            .. versionchanged:: 3.3.2
               The ``return_json`` parameter has been introduced which returns a simple JSON object (as a ``dict``)
               indicating whether or not the operation was successful. (Currently ``False`` by default)

            .. versionadded:: 3.2.0

            :param setting_name: The name of the setting field for which to retrieve the value
            :type setting_name: str
            :param setting_val: The value of the setting to be defined
            :type setting_val: str
            :param node_id: The ID of the node associated with the setting to retrieve
            :type node_id: str
            :param node_type: Defines the node as a ``board`` (default), ``category`` or ``grouphub``
            :type node_type: str
            :param return_json: Returns a simple JSON dictionary indicating the operation result (``False`` by default)

                                .. caution:: An unsuccessful REST call will result in the raising of the
                                             :py:exc:`khoros.errors.exceptions.PostRequestError` exception if the
                                             ``return_json`` parameter is set to ``False``.

            :type return_json: bool
            :returns: None
            :raises: :py:exc:`ValueError`, :py:exc:`TypeError`,
                     :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            return objects_module.settings.define_node_setting(self.khoros_object, setting_name, setting_val,
                                                               node_id, node_type, return_json)

    class Studio(object):
        """This class includes methods relating to the Lithium SDK and Studio Plugin."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Studio` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        @staticmethod
        def sdk_installed():
            """This method checks to see if the Lithium SDK is installed.

            .. versionadded:: 2.5.1

            :returns: Boolean value indicating whether or not the Lithium SDK is installed
            """
            return studio_module.base.sdk_installed()

        @staticmethod
        def get_sdk_version():
            """This method identifies the currently installed version of the Lithium SDK.

            .. versionadded:: 2.5.1

            :returns: The SDK version in string format or ``None`` if not installed
            """
            return studio_module.base.get_sdk_version()

        @staticmethod
        def node_installed():
            """This method checks whether or not Node.js is installed.

            .. versionadded:: 2.5.1

            :returns: Boolean value indicating whether or not Node.js is installed
            """
            return studio_module.base.node_installed()

        @staticmethod
        def get_node_version():
            """This method identifies and returns the installed Node.js version.

            .. versionadded:: 2.5.1

            :returns: The version as a string or ``None`` if not installed
            """
            return studio_module.base.get_node_version()

        @staticmethod
        def npm_installed():
            """This method checks whether or not npm is installed.

            .. versionadded:: 2.5.1

            :returns: Boolean value indicating whether or not npm is installed
            """
            return studio_module.base.npm_installed()

        @staticmethod
        def get_npm_version():
            """This method identifies and returns the installed npm version.

            .. versionadded:: 2.5.1

            :returns: The version as a string or ``None`` if not installed
            """
            return studio_module.base.get_npm_version()

    class Subscription(object):
        """This class includes methods relating to subscriptions."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Subscription` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def add_subscription(self, target_id, target_type='board', payload=None, included_boards=None,
                             excluded_boards=None, proxy_user_object=None):
            """This method adds a subscription to a given target for the current user.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.5.0

            :param target_id: The unique identifier for the target (e.g. Node ID, Message ID, etc.)
            :type target_id: str, int
            :param target_type: The target type such as ``board`` (default), ``message``, ``category``, etc.
            :param payload: Pre-constructed payload to use in the API call
            :type payload: dict, None
            :param included_boards: One or more boards (represented by Node ID) to be included in the
                                    partial subscription
            :type included_boards: list, tuple, set, str, None
            :param excluded_boards: One or more boards (represented by Node ID) to be excluded from the
                                    partial subscription
            :type excluded_boards: list, tuple, set, str, None
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response in JSON format
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            return objects_module.subscriptions.add_subscription(self.khoros_object, target_id, target_type, payload,
                                                                 included_boards, excluded_boards,
                                                                 proxy_user_object=proxy_user_object)

        def get_subscription_uri(self):
            """This method returns the subscriptions URI for the v2 API to perform API calls.

            .. versionadded:: 3.5.0

            :returns: The full (absolute) URI for the ``subscriptions`` v2 API endpoint
            """
            return objects_module.subscriptions.get_subscription_uri(self.khoros_object)

        def subscribe_to_board(self, node_id, proxy_user_object=None):
            """This method subscribes the current user to an individual message.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.5.0

            :param node_id: The unique identifier for a board (i.e. Board ID)
            :type node_id: str
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response in JSON format
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            return objects_module.subscriptions.subscribe_to_board(self.khoros_object, node_id, proxy_user_object)

        def subscribe_to_category(self, node_id, included_boards=None, excluded_boards=None, proxy_user_object=None):
            """This method subscribes the current user to a full or partial category.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.5.0

            :param node_id: The unique identifier (i.e. Node ID) for the category
            :type node_id: str
            :param included_boards: One or more boards (represented by Node ID) to be included in
                                    the partial subscription
            :type included_boards: list, tuple, set, str, None
            :param excluded_boards: One or more boards (represented by Node ID) to be excluded from
                                    the partial subscription
            :type excluded_boards: list, tuple, set, str, None
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response in JSON format
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            return objects_module.subscriptions.subscribe_to_category(self.khoros_object, node_id, included_boards,
                                                                      excluded_boards, proxy_user_object)

        def subscribe_to_label(self, label, board_id, proxy_user_object=None):
            """This method subscribes the current user to label found on a board.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.5.0

            :param label: The label to which to subscribe
            :type label: str, int
            :param board_id: The unique identifier (i.e. Node ID) for the board where the label is found
            :type board_id: str
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response in JSON format
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            return objects_module.subscriptions.subscribe_to_label(self.khoros_object, label, board_id,
                                                                   proxy_user_object)

        def subscribe_to_message(self, msg_id, proxy_user_object=None):
            """This method subscribes the current user to an individual message.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.5.0

            :param msg_id: The unique identifier for an individual message
            :type msg_id: str, int
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response in JSON format
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            return objects_module.subscriptions.subscribe_to_message(self.khoros_object, msg_id, proxy_user_object)

        def subscribe_to_product(self, product_id, proxy_user_object=None):
            """This method subscribes the current user to a product.

            .. versionchanged:: 4.0.0
               Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf
               of other users.

            .. versionadded:: 3.5.0

            :param product_id: The unique identifier for a product
            :type product_id: str, int
            :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform
                                      the API request on behalf of a secondary user.
            :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
            :returns: The API response in JSON format
            :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
                     :py:exc:`khoros.errors.exceptions.POSTRequestError`,
                     :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
            """
            return objects_module.subscriptions.subscribe_to_product(self.khoros_object, product_id, proxy_user_object)

    class Tag(object):
        """This class includes methods relating to the tagging of content.

        .. versionadded:: 4.1.0
        """
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.Tag` inner class object.

            .. versionadded:: 4.1.0

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def get_tags_for_message(self, msg_id):
            """This method retrieves the tags for a given message.

            .. versionadded:: 4.1.0

            :param msg_id: The Message ID for the message from which to retrieve tags
            :type msg_id: str, int
            :returns: A list of tags associated with the message
            """
            return objects_module.tags.get_tags_for_message(self.khoros_object, msg_id)

        def add_single_tag_to_message(self, tag, msg_id, allow_exceptions=False):
            """This method adds a single tag to an existing message.

            .. versionadded:: 4.1.0

            :param tag: The tag value to be added
            :type tag: str
            :param msg_id: The unique identifier for the message
            :type msg_id: str, int
            :param allow_exceptions: Determines if exceptions are permitted to be raised (``False`` by default)
            :type allow_exceptions: bool
            :returns: None
            :raises: :py:exc:`khoros.errors.exceptions.POSTRequestError`
            """
            return objects_module.tags.add_single_tag_to_message(self.khoros_object, tag, msg_id, allow_exceptions)

        def add_tags_to_message(self, tags, msg_id, allow_exceptions=False):
            """This method adds one or more tags to an existing message.

            .. versionadded:: 4.1.0

            ..caution:: This function is not the most effective way to add multiple tags to a message. It is recommended
                        that the :py:meth:`khoros.core.Khoros.messages.update` method be used instead with its ``tags``
                        argument, which is more efficient and performance-conscious.

            :param tags: One or more tags to be added to the message
            :type tags: str, tuple, list, set
            :param msg_id: The unique identifier for the message
            :type msg_id: str, int
            :param allow_exceptions: Determines if exceptions are permitted to be raised (``False`` by default)
            :type allow_exceptions: bool
            :returns: None
            :raises: :py:exc:`khoros.errors.exceptions.POSTRequestError`
            """
            objects_module.tags.add_tags_to_message(self.khoros_object, tags, msg_id, allow_exceptions)
            return

        @staticmethod
        def structure_single_tag_payload(tag_text):
            """This method structures the payload for a single tag.

            .. versionadded:: 4.1.0

            :param tag_text: The tag to be included in the payload
            :type tag_text: str
            :returns: The payload as a dictionary
            :raises: :py:exc:`khoros.errors.exceptions.InvalidPayloadValueError`
            """
            return objects_module.tags.structure_single_tag_payload(tag_text)

        def structure_tags_for_message(self, *tags, msg_id=None, overwrite=False, ignore_non_strings=False,
                                       wrap_json=False):
            """This method structures tags to use within the payload for creating or updating a message.

            .. versionchanged:: 4.3.0
               Introduced the ``wrap_json`` parameter to wrap the tags in a dictionary within the ``items`` key.

            .. versionadded:: 4.1.0

            :param tags: One or more tags or list of tags to be structured
            :type tags: str, list, tuple, set
            :param msg_id: Message ID of an existing message so that its existing tags can be retrieved (optional)
            :type msg_id: str, int, None
            :param overwrite: Determines if tags should overwrite any existing tags (where applicable) or if the tags
                              should be appended to the existing tags (default)
            :type overwrite: bool
            :param ignore_non_strings: Determines if non-strings (excluding iterables) should be ignored rather than
                                       converted to strings (``False`` by default)
            :type ignore_non_strings: bool
            :param wrap_json: Determines if the list of tags should be wrapped in the ``{"items": []}`` JSON structure
                              -- In other words, a dictionary rather than a list (``False`` by default)
            :type wrap_json: bool
            :returns: A list of properly formatted tags to act as the value for the ``tags`` field in the message payload
            """
            return objects_module.tags.structure_tags_for_message(*tags, khoros_object=self.khoros_object,
                                                                  msg_id=msg_id, overwrite=overwrite,
                                                                  ignore_non_strings=ignore_non_strings,
                                                                  wrap_json=wrap_json)

    class User(object):
        """This class includes methods for interacting with users."""
        def __init__(self, khoros_object):
            """This method initializes the :py:class:`khoros.core.Khoros.User` inner class object.

            :param khoros_object: The core :py:class:`khoros.Khoros` object
            :type khoros_object: class[khoros.Khoros]
            """
            self.khoros_object = khoros_object

        def impersonate_user(self, user_login):
            """This method instantiates and returns the :py:class`khoros.objects.users.ImpersonatedUser` object which
               can then be passed to other methods and functions to perform operations as a secondary user.

               .. note:: The authenticated user must have the **Administrator** role and/or have the
                         **Switch User** permission enabled.

            .. versionadded:: 4.0.0

            :param user_login: The username (i.e. login) of the user to be impersonated
            :type user_login: str
            :returns: The instantiated :py:class`khoros.objects.users.ImpersonatedUser` object
            """
            return objects_module.users.impersonate_user(self.khoros_object, user_login)

        def create(self, user_settings=None, login=None, email=None, password=None, first_name=None, last_name=None,
                   biography=None, sso_id=None, web_page_url=None, cover_image=None, ignore_exceptions=False):
            """This method creates a new user in the Khoros Community environment.

            .. versionchanged:: 4.0.0
               This function now returns the API response and the ``ignore_exceptions`` parameter has been introduced.

            .. versionchanged:: 3.5.0
               The unnecessary ``return`` statement at the end of the method has been removed.

            :param user_settings: Allows all user settings to be passed to the function within a single dictionary
            :type user_settings: dict, None
            :param login: The username (i.e. ``login``) for the user (**required**)
            :type login: str, None
            :param email: The email address for the user (**required**)
            :type email: str, None
            :param password: The password for the user
            :type password: str, None
            :param first_name: The user's first name (i.e. given name)
            :type first_name: str, None
            :param last_name: The user's last name (i.e. surname)
            :type last_name: str, None
            :param biography: The user's biography for their profile
            :type biography: str, None
            :param sso_id: The Single Sign-On (SSO) ID for the user
            :type sso_id: str, None
            :param web_page_url: The URL to the user's website
            :type web_page_url: str, None
            :param cover_image: The cover image to be used on the user's profile
            :type cover_image: str, None
            :param ignore_exceptions: Defines whether to raise the :py:exc:`khoros.errors.exceptions.UserCreationError`
                                      exception if the creation attempt fails (``False`` by default)
            :type ignore_exceptions: bool
            :returns: The response to the user creation API request
            :raises: :py:exc:`khoros.errors.exceptions.UserCreationError`
            """
            return objects_module.users.create(self.khoros_object, user_settings, login, email, password, first_name,
                                               last_name, biography, sso_id, web_page_url, cover_image,
                                               ignore_exceptions)

        def delete(self, user_id, return_json=False):
            """This method deletes a user from the Khoros Community environment.

            :param user_id: The User ID of the user to be deleted
            :type user_id: str, int
            :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
            :type return_json: bool
            :returns: The API response (optionally in JSON format)
            :raises: :py:exc:`khoros.errors.exceptions.FeatureNotConfiguredError`
            """
            return objects_module.users.delete(self.khoros_object, user_id, return_json)

        def get_user_id(self, user_settings=None, login=None, email=None, first_name=None, last_name=None,
                        allow_multiple=False, display_warnings=True):
            """This method looks up and retrieves the User ID for a user by leveraging supplied user information.

            .. note:: The priority of supplied fields are as follows: login, email, first and last name,
                      last name, first name

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :param first_name: The first name (i.e. given name) of the user
            :type first_name: str, None
            :param last_name: The last name (i.e. surname) of the user
            :type last_name: str, None
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
            """This method looks up and retrieves the username for a user by leveraging supplied user information.

            .. note:: The priority of supplied fields are as follows: User ID, email, first and last name, last name,
                      first name

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID of the user
            :type user_id: str, None
            :param email: The email address of the user
            :type email: str, None
            :param first_name: The first name (i.e. given name) of the user
            :type first_name: str, None
            :param last_name: The last name (i.e. surname) of the user
            :type last_name: str, None
            :param allow_multiple: Allows a list of usernames to be returned if multiple results are found
            :type allow_multiple: bool
            :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
            :type display_warnings: bool
            :returns: The username (i.e. login) of the user or a list of usernames if ``allow_multiple`` is ``True``
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
            """This method retrieves the email address for a user by leveraging supplied user information.

            .. note:: The priority of supplied fields are as follows: User ID, username, first and last name, last name,
                      first name

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID of the user
            :type user_id: str, None
            :param login: The username of the user
            :type login: str, None
            :param first_name: The first name (i.e. given name) of the user
            :type first_name: str, None
            :param last_name: The last name (i.e. surname) of the user
            :type last_name: str, None
            :param allow_multiple: Allows a list of email addresses to be returned if multiple results are found
            :type allow_multiple: bool
            :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
            :type display_warnings: bool
            :returns: The email address of the user as a string or a list of emails if ``allow_multiple`` is ``True``
            """
            return objects_module.users.get_email(self.khoros_object, user_settings, user_id, login, first_name,
                                                  last_name, allow_multiple, display_warnings)

        def get_ids_from_login_list(self, login_list, return_type='list'):
            """This method identifies the User IDs associated with a list of user logins. (i.e. usernames)

            :param login_list: List of user login (i.e. username) values in string format
            :type login_list: list, tuple
            :param return_type: Determines if the data should be returned as a ``list`` (default) or a ``dict``
            :type return_type: str
            :returns: A list or dictionary with the User IDs
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_ids_from_login_list(self.khoros_object, login_list, return_type)

        def query_users_table_by_id(self, select_fields, user_id):
            """This method queries the ``users`` table for one or more given SELECT fields for a specific User ID.

            :param select_fields: One or more SELECT field (e.g. ``login``, ``messages.count(*)``, etc.) to query
            :type select_fields: str, tuple, list, set
            :param user_id: The User ID associated with the user
            :type user_id: int, str
            :returns: The API response for the performed LiQL query
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.query_users_table_by_id(self.khoros_object, select_fields, user_id)

        def get_user_data(self, user_settings=None, user_id=None, login=None, email=None):
            """This method retrieves all user data for a given user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: A dictionary containing the user data for the user
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_user_data(self.khoros_object, user_settings, user_id, login, email)

        def get_album_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the number of albums for a user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of albums found for the user as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_album_count(self.khoros_object, user_settings, user_id, login, email)

        def get_followers_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of community members who have added the user as a friend in the community.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of community members who have added the user as a friend in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_followers_count(self.khoros_object, user_settings, user_id, login, email)

        def get_following_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of community members the user has added as a friend in the community.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of community members the user has added as a friend in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_following_count(self.khoros_object, user_settings, user_id, login, email)

        def get_images_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of images uploaded by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of images uploaded by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_images_count(self.khoros_object, user_settings, user_id, login, email)

        def get_public_images_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of public images uploaded by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of public images uploaded by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_public_images_count(self.khoros_object, user_settings, user_id,
                                                                login, email)

        def get_messages_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of messages (topics and replies) posted by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of messages (topics and replies) posted by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_messages_count(self.khoros_object, user_settings, user_id, login, email)

        def get_roles_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of roles applied to the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of roles applied to the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_roles_count(self.khoros_object, user_settings, user_id, login, email)

        def get_solutions_authored_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of messages created by the user that are marked as accepted solutions.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of messages created by the user that are marked as accepted solutions in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_solutions_authored_count(self.khoros_object, user_settings, user_id,
                                                                     login, email)

        def get_topics_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of topic messages (excluding replies) posted by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of topic messages (excluding replies) posted by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_topics_count(self.khoros_object, user_settings, user_id, login, email)

        def get_replies_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of replies posted by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of replies posted by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_replies_count(self.khoros_object, user_settings, user_id, login, email)

        def get_videos_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of videos uploaded by the user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of videos uploaded by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_videos_count(self.khoros_object, user_settings, user_id, login, email)

        def get_kudos_given_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of kudos a user has given.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of kudos given by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_kudos_given_count(self.khoros_object, user_settings, user_id, login, email)

        def get_kudos_received_count(self, user_settings=None, user_id=None, login=None, email=None):
            """This method gets the count of kudos a user has received.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The number of kudos received by the user in integer format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_kudos_received_count(self.khoros_object, user_settings, user_id,
                                                                 login, email)

        def get_online_user_count(self):
            """This method retrieves the number of users currently online.

            :returns: The user count for online users as an integer
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_online_user_count(self.khoros_object)

        def get_registration_data(self, user_settings=None, user_id=None, login=None, email=None):
            """This method retrieves the registration data for a given user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: A dictionary containing the registration data for the user
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_registration_data(self.khoros_object, user_settings, user_id, login, email)

        def get_registration_timestamp(self, user_settings=None, user_id=None, login=None, email=None):
            """This method retrieves the timestamp for when a given user registered for an account.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The registration timestamp in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_registration_timestamp(self.khoros_object, user_settings, user_id,
                                                                   login, email)

        def get_registration_status(self, user_settings=None, user_id=None, login=None, email=None):
            """This method retrieves the registration status for a given user.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The registration status in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_registration_status(self.khoros_object, user_settings, user_id,
                                                                login, email)

        def get_last_visit_timestamp(self, user_settings=None, user_id=None, login=None, email=None):
            """This method retrieves the timestamp for the last time the user logged into the community.

            :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
            :type user_settings: dict, None
            :param user_id: The User ID associated with the user
            :type user_id: int, str, None
            :param login: The username of the user
            :type login: str, None
            :param email: The email address of the user
            :type email: str, None
            :returns: The last visit timestamp in string format
            :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
            """
            return objects_module.users.get_last_visit_timestamp(self.khoros_object, user_settings, user_id,
                                                                 login, email)

        def update_sso_id(self, new_sso_id, user_id=None, user_login=None):
            """This method updates the SSO ID for a user.

            .. versionadded:: 4.5.0

            :param new_sso_id: The new SSO ID for the user
            :type new_sso_id: str
            :param user_id: The numeric User ID that identifies the user
            :type user_id: str, int, None
            :param user_login: The username that identifies the user
            :type user_login: str, None
            :returns: The API response
            :raises: py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
            """
            return objects_module.users.update_sso_id(self.khoros_object, new_sso_id, user_id, user_login)

    def signout(self):
        """This method invalidates the active session key or SSO authentication session.

        .. versionchanged:: 3.5.0
           The unnecessary ``return`` statement at the end of the method has been removed.

        .. versionchanged:: 3.3.2
           Logging was introduced to report the successful session invalidation.
        """
        session_terminated = auth.invalidate_session(self)
        if session_terminated:
            self.auth['active'] = False
        logger.info('The session has been successfully invalidated and the API is no longer connected.')

    def __del__(self):
        """This method fully destroys the instance."""
        self.close()

    def close(self):
        """This core method destroys the instance.

        .. versionchanged:: 3.5.0
           The unnecessary ``pass`` statement at the end of the method has been removed.
        """
