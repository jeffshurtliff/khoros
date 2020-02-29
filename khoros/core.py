# -*- coding: utf-8 -*-
"""
:Module:            khoros.core
:Synopsis:          Collection of core functions and tools to work with the Khoros Community APIs
:Usage:             ``import khoros.core`` (Imported by default in primary package)``
:Example:           ``khoros.core.initialize(base_url='community.example.com', community='mycommunity')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Feb 2020
"""

import sys
import copy
import logging

from . import auth, errors
from .utils.helper import get_helper_settings

# Initialize logging
logging.getLogger("khoros").addHandler(logging.NullHandler())


class Khoros(object):
    """This is the class for the core object leveraged in this library."""
    # Define default configuration information
    DEFAULT_SETTINGS = {
        'community_url': 'https://community.khoros.com',
        'tenant_id': 'lithosphere',
    }
    DEFAULT_AUTH = {
        'auth_type': 'session_auth'
    }

    def __init__(self, settings=None, community_url=None, tenant_id=None, auth_type=None, session_auth=None,
                 oauth2=None, sso=None, helper=None, auto_connect=True):
        """This method initializes the Khoros object.

        :param settings: Predefined settings that the object should use
        :type settings: dict
        :param community_url: The base URL of the Khoros community instance (e.g. ``community.khoros.com``)
        :type community_url: str
        :param tenant_id: The tenant ID for the Khoros community instance (e.g. ``lithosphere``)
        :type tenant_id: str
        :param auth_type: The authentication type to use when connecting to the instance (``session_auth`` by default)
        :type auth_type: str
        :param session_auth: The ``username`` and ``password`` values for session key authentication
        :type session_auth: dict
        :param oauth2: The ``client_id``, ``client_secret`` and ``redirect_url`` values for OAuth 2.0 authentication
        :type oauth2: dict
        :param sso: The values for single sign-on (SSO) authentication
        :type sso: dict
        :param helper: The path (and optional file type) to the YAML or JSON helper configuration file
        :type helper: str, tuple, list, dict
        :param auto_connect: Determines if a connection should be established when initialized (``True`` by default)
        :type auto_connect: bool
        """
        # Initialize the dictionaries if not passed to the class
        if settings is None:
            settings = {}
        
        # Initialize other dictionaries that will be used by the class object
        self.auth = {}
        self.core = {}

        # Add supplied elements to the settings dictionary
        if community_url:
            settings['community_url'] = community_url
        if tenant_id:
            settings['tenant_id'] = tenant_id

        # Creates the private _settings attribute using the default settings as a base
        self._settings = copy.copy(Khoros.DEFAULT_SETTINGS)
        self._settings.update(Khoros.DEFAULT_AUTH)
        self._settings.update(settings)

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
                if auth_map.get(auth_type) is None:
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
                error_msg = f"No data was found for the default '{auth_type}' authentication type."
                raise errors.exceptions.MissingAuthDataError(error_msg)

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

        # Capture the version information
        self.sys_version_info = tuple([i for i in sys.version_info])

        # Establish logging
        self.logging = logging

        # Validate the settings
        self.__validate_base_url()
        self.__define_url_settings()

        # Auto-connect to the environment if specified (default)
        if auto_connect:
            if 'session_auth' in self._settings['auth_type']:
                self.__connect_with_session_key()
            else:
                errors.handlers.eprint("Unable to auto-connect to the instance with the given " +
                                       f"'{self._settings['auth_type']}' authentication type.")

    def __parse_helper_settings(self):
        """This method parses the settings in the helper configuration file when provided."""
        # Parse the helper settings and add them to the primary settings
        if 'connection' in self._helper_settings:
            helper_keys = ['community_url', 'tenant_id', 'oauth2', 'session_auth']
            for helper_key in helper_keys:
                if helper_key in self._helper_settings['connection']:
                    self._settings[helper_key] = self._helper_settings['connection'][helper_key]

    def __validate_base_url(self):
        """This method ensures that the Community URL is defined appropriately."""
        if ('http://' not in self._settings['community_url']) and ('https://' not in self._settings['community_url']):
            self._settings['community_url'] = f"https://{self._settings['community_url']}"
        if self._settings['community_url'].endswith('/'):
            self._settings['community_url'] = self._settings['community_url'][:-1]

    def __define_url_settings(self):
        if 'tenant_id' in self._settings:
            self._settings['base_url'] = f"{self._settings['community_url']}/{self._settings['tenant_id']}"
        else:
            self._settings['base_url'] = self._settings['community_url']
        self._settings['v2_base'] = f"{self._settings['base_url']}/api/2.0"

    def __connect_with_session_key(self):
        if ('username' not in self._settings['session_auth']) or ('password' not in self._settings['session_auth']):
            error_msg = f"The username and/or password for session key authentication cannot be found."
            raise errors.exceptions.MissingAuthDataError(error_msg)
        self._settings['session_auth']['session_key'] = auth.get_session_key(self)
        self._settings['auth_header'] = auth.get_session_header(self._settings['session_auth']['session_key'])
        self.auth['header'] = self._settings['auth_header']

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

    def __del__(self):
        """This method fully destroys the instance."""
        self.close()

    def close(self):
        """This core method destroys the instance."""
        pass
