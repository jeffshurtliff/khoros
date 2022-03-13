# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.bulk_data
:Synopsis:          This module includes functions that relate to the Bulk Data API.
:Usage:             ``from khoros import bulk_data``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     12 Mar 2022
"""

from . import api, errors
from .utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_base_url(khoros_object=None, community_id=None, europe=False):
    """This function constructs and/or retrieves the base URL for the Bulk Data API.

    .. versionadded:: 5.0.0

    .. note:: The URL from the helper settings will be leveraged when available unless the ``community_id`` is
              explicitly defined as a function parameter.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None
    :param community_id: The Community ID to leverage in the URL
    :type community_id: str, None
    :param europe: Determines if the European URL should be utilized (``False`` by default)
    :type europe: bool
    :returns: The base URL for the Bulk Data API
    """
    base_url = None
    base_urls = {
        True: 'https://eu.api.lithium.com/lsi-data/v2/data/export/community/',
        False: 'https://api.lithium.com/lsi-data/v2/data/export/community/'
    }

    # Retrieve the base URL from the helper settings when defined
    if not community_id and khoros_object:
        try:
            base_url = khoros_object._helper_settings['connection']['bulk_data']['base_url']
        except (KeyError, AttributeError):
            # Attempt to define the community ID if found
            try:
                community_id = khoros_object._helper_settings['connection']['bulk_data']['community_id']
            except (KeyError, AttributeError):
                pass

    # Construct the base URL when not defined in the helper settings
    if not base_url:
        base_url = base_urls.get(europe)
        if community_id:
            base_url = f'{base_url}{community_id}'
    return base_url

