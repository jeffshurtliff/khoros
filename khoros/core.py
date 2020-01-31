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
import os.path
import logging

import requests

from . import auth, errors


class Khoros(object):
    # Define default configuration information
    DEFAULT_SETTINGS = {
        'base_url': 'https://community.khoros.com',
        'community': 'lithosphere',
        'helper': ''
    }
    DEFAULT_AUTH = {
        'auth_type': 'oauth2'
    }

    def __init__(self, settings=None, base_url=None, community=None, auth_type=None, oauth1=None, oauth2=None,
                 sso=None):
        # Initializes the dictionaries if not passed to the class
        if settings is None:
            settings = {}

        # Add supplied elements to the settings dictionary
        if base_url:
            settings['base_url'] = base_url
        if community:
            settings['community'] = community

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

        # Capture the version information
        self.sys_version_info = tuple([i for i in sys.version_info])

        # Establish logging
        self.logging = logging

        # Validate the settings
        self.__validate_base_url()
        self.__define_url_settings()

    def __validate_base_url(self):
        if ('http://' not in self._settings['base_url']) and ('https://' not in self._settings['base_url']):
            self._settings['base_url'] = f"https://{self._settings['base_url']}"
        if self._settings['base_url'].endswith('/'):
            self._settings['base_url'] = self._settings['base_url'][:-1]

    def __define_url_settings(self):
        if 'community' in self._settings:
            self._settings['base_url'] = f"{self._settings['base_url']}/{self._settings['community']}"
        self._settings['v2_base'] = f"{self._settings['base_url']}/api/2.0"

    # def __define_auth_header(self):
    #     self._settings['auth_header'] = {"Authorization": f"Bearer {self._settings['access_token']}"}

    def __del__(self):
        """This function fully destroys the instance."""
        self.close()
