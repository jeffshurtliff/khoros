# -*- coding: utf-8 -*-
"""
:Module:            khoros.auth
:Synopsis:          TBD
:Usage:             TBD
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     31 Jan 2020
"""

import requests
from requests_oauthlib import OAuth2Session

from . import core


def init_empty_attributes(khoros_object, oauth, sso):
    """This function initializes empty attributes for the object when not supplied during instantiation.

    :param khoros_object: The Khoros object generated in the khoros.core module
    :type khoros_object: class
    :param oauth: Attribute containing information for connecting via OAuth 2.0
    :type oauth: dict, NoneType
    :param sso: Attribute containing information for connecting via LithiumSSO
    :type sso: dict, NoneType
    :returns: The Khoros object
    """
    if oauth is None:
        khoros_object.oauth = {}
    if sso is None:
        khoros_object.sso = {}
    return
