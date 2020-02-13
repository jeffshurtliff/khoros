# -*- coding: utf-8 -*-
"""
:Module:            khoros.core
:Synopsis:          Collection of core functions and tools to work with the Khoros Community APIs
:Usage:             ``import khoros.core`` (Imported by default in primary package)
:Example:           ``khoros.core.initialize(base_url='community.example.com', community='mycommunity')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     31 Jan 2020
"""

import sys
import copy
import logging

from . import auth, errors
from .utils.helper import get_helper_settings

# Initialize logging
logging.getLogger("khoros").addHandler(logging.NullHandler())


class Khoros(object):
    # Define default configuration information
    DEFAULT_SETTINGS = {
        'community_url': 'https://community.khoros.com',
        'tenant_id': 'lithosphere',
    }
    DEFAULT_AUTH = {
        'auth_type': 'oauth2'
    }

    def __init__(self, settings=None, community_url=None, tenant_id=None, auth_type=None, oauth1=None, oauth2=None,
                 sso=None, helper=None):
        # Initializes the dictionaries if not passed to the class
        if settings is None:
            settings = {}

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
        if auth_type is not None:
            accepted_auth_types = ['oauth1', 'oauth2', 'sso']
            auth_map = {
                'oauth1': oauth1,
                'oauth2': oauth2,
                'sso': sso
            }
            if str(auth_type) in accepted_auth_types:
                self._settings['auth_type'] = auth_type
                if auth_map.get(auth_type) is None:
                    error_msg = f"The '{auth_type}' authentication type was specified but no associated data was found."
                    raise errors.exceptions.MissingAuthDataError(error_msg)
            # TODO: Display error if invalid option provided (revert to default)
        elif sso is not None:
            self._settings['auth_type'] = 'sso'
        elif oauth1 is not None:
            self._settings['auth_type'] = 'oauth1'
        else:
            if oauth2 is not None:
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

    def __parse_helper_settings(self):
        # Parse the helper settings and add them to the primary settings
        if 'connection' in self._helper_settings:
            helper_keys = ['community_url', 'tenant_id', 'oauth2']
            for helper_key in helper_keys:
                if helper_key in self._helper_settings['connection']:
                    self._settings[helper_key] = self._helper_settings['connection'][helper_key]

    def __validate_base_url(self):
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

    # def __define_auth_header(self):
    #     self._settings['auth_header'] = {"Authorization": f"Bearer {self._settings['access_token']}"}

    def __del__(self):
        """This function fully destroys the instance."""
        self.close()
