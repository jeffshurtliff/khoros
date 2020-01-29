# -*- coding: utf-8 -*-
"""
:Module:            khoros.core
:Synopsis:          Collection of core functions and tools to work with the Khoros Community APIs
:Usage:             ``import khorosjx.core`` (Imported by default in primary package)
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     29 Jan 2020
"""


def initialize(**kwargs):
    """This function initializes the package by defining a global dictionary of environmental variables.
    
    :param kwargs: Keyword arguments to popuate in the global dictionary
    :type kwargs: dict 
    :returns: None
    """
    # Define the global dictionary if it doesn't already exist
    try:
        settings
    except NameError:
        global settings
        settings = {}

    # Populate the dictionary with any supplied key value pairs that are supported
    permitted_fields = ['base_url', 'community', 'access_token', 'helper']
    for init_key, init_val in kwargs.items():
        if init_key in permitted_fields:
            settings[init_key] = init_val
    
    # Evaluate the values to ensure that they are valid
    evaluate_settings()
    return


def __validate_base_url():
    if ('http://' not in settings['base_url']) and ('https://' not in settings['base_url']):
        settings['base_url'] = f"https://{settings['base_url']}"
    if settings['base_url'][-1:] == '/':
        settings['base_url'] = settings['base_url'][:-1]
    return


def __define_url_settings():
    if 'community' in settings.keys():
        settings['v2_base'] = f"{settings['base_url']}/{settings['community']}/api/2.0"
    return


def __define_auth_header():
    settings['auth_header'] = {"Authorization": f"Bearer {settings['access_token']}"}
    return


def evaluate_settings():
    if 'base_url' in settings.keys():
        __validate_base_url()
        __define_url_settings()
    if 'access_token' in settings.keys():
        __define_auth_header()
    return
