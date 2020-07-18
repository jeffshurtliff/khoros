# -*- coding: utf-8 -*-
"""
:Module:            khoros.structures.communities
:Synopsis:          This module contains functions specific to the high-level community configuration
:Usage:             ``from khoros.structures import communities``
:Example:           ``details = get_community_details(khoros_object)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

from . import base
from .. import errors
from ..utils import log_utils
from ..utils.core_utils import display_warning

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_community_details(khoros_object):
    """This function returns a dictionary of community configuration settings.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :returns: The community details within a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    response = base.get_details(khoros_object, community=True)
    _check_for_multiple_tenants(response)
    return response['data']['items'][0]


def _check_for_multiple_tenants(_community_details):
    """This function checks to see if more than one community instance (i.e. tenant) was found and displays a warning.

    .. versionadded:: 2.1.0

    :param _community_details: Dictionary containing community details from LiQL
    :type _community_details: dict
    :returns: None
    """
    if _community_details['data']['size'] > 1:
        display_warning(f"{_community_details['data']['size']} community instances (i.e. tenants) were found but " +
                        "only details from the first tenant will be returned.")
    return


def get_community_field(khoros_object, field, community_details=None):
    """This function returns a specific community field from the Khoros Community API.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param field: The field from the :py:class:`khoros.structures.base.Mapping` class whose value should be returned
    :type field: str
    :param community_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type community_details: dict, None
    :returns: The requested field in its native format
    :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    return base.get_structure_field(khoros_object, field, community=True, details=community_details)


def get_tenant_id(khoros_object, community_details=None):
    """This function retrieves the tenant ID of the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The tenant ID in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'id', community_details)


def get_title(khoros_object, full_title=True, short_title=False, community_details=None):
    """This function retrieves the full and/or short title of the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param full_title: Return the full title of the environment (``True`` by default)
    :type full_title: bool
    :param short_title: Return the short title of the environment (``False`` by default)
    :type short_title: bool
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The title(s) of the environment as a string or a tuple of strings
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    if not full_title and not short_title:
        exc_msg = "Must return at least the full title or the short title."
        raise errors.exceptions.MissingRequiredDataError(exc_msg)
    if not community_details:
        community_details = get_community_details(khoros_object)
    titles = (community_details['title'], community_details['short_title'])
    if not short_title:
        titles = titles[0]
    elif not full_title:
        titles = titles[1]
    return titles


def get_description(khoros_object, community_details=None):
    """This function retrieves the description of the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The description in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'description', community_details)


def get_primary_url(khoros_object, community_details=None):
    """This function retrieves the primary URL of the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The primary URL in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'view_href', community_details)


def get_max_attachments(khoros_object, community_details=None):
    """This function retrieves the maximum number of attachments permitted per message within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The value as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'attachment_max_per_message', community_details)


def get_permitted_attachment_types(khoros_object, community_details=None):
    """This function retrieves the attachment file types permitted within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The permitted file types within a list
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'attachment_file_types', community_details).split(',')


def email_confirmation_required_to_post(khoros_object, community_details=None):
    """This function identifies if an email configuration is required before posting in the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: Boolean value indicating if email configuration is required before posting
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'email_confirmation_required_to_post', community_details)


def get_language(khoros_object, community_details=None):
    """This function retrieves the language (e.g. ``en``) utilized in the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The language code as a string
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'language', community_details)


def get_ooyala_player_branding_id(khoros_object, community_details=None):
    """This function retrieves the branding ID for the Ooyala Player utilized within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The branding ID in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    if not community_details:
        community_details = get_community_details(khoros_object)
    if 'ooyala_player_branding_id' not in community_details:
        branding_id = None
    else:
        branding_id = community_details['ooyala_player_branding_id']
    return branding_id


def get_date_pattern(khoros_object, community_details=None):
    """This function retrieves the date pattern (e.g. ``yyyy-MM-dd``) utilized within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The date pattern in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'date_pattern', community_details)


def friendly_date_enabled(khoros_object, community_details=None):
    """This function if the friendly date functionality is utilized within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: Boolean value indicating if the feature is enabled
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'friendly_date_enabled', community_details)


def get_friendly_date_max_age(khoros_object, community_details=None):
    """This function identifies if the friendly date functionality is utilized within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: Boolean value indicating if the feature is enabled
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'friendly_date_max_age', community_details)


def get_active_skin(khoros_object, community_details=None):
    """This function retrieves the primary active skin that is utilized within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The skin name as a string
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'skin', community_details)


def get_sign_out_url(khoros_object, community_details=None):
    """This function retrieves the Sign Out URL for the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The Sign Out URL as a string
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'web_ui_sign_out_url', community_details)


def get_creation_date(khoros_object, community_details=None):
    """This function retrieves the timestamp for the initial creation of the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: The creation date as a string (e.g. ``2020-02-03T22:41:36.408-08:00``)
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    # TODO: Allow a format to be specified and the ability to parse as a datetime object if needed
    return get_community_field(khoros_object, 'creation_date', community_details)


def top_level_categories_enabled(khoros_object, community_details=None):
    """This function identifies if top level categories are enabled within the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: Boolean value indicating if top level categories are enabled
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'top_level_categories_enabled', community_details)


def show_community_node_in_breadcrumb(khoros_object, community_details=None):
    """This function identifies if the community node should be shown in breadcrumbs.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: Boolean value indicating if the community node is displayed in bredcrumbs
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'tlc_show_community_node_in_breadcrumb', community_details)


def show_breadcrumb_at_top_level(khoros_object, community_details=None):
    """This function identifies if breadcrumbs should be shown at the top level of the environment.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: Boolean value indicating if breadcrumbs are displayed at the top level of the environment
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'tlc_show_breadcrumb_at_top_level', community_details)


def top_level_categories_on_community_page(khoros_object, community_details=None):
    """This function identifies if top level categories are enabled on community pages.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param community_details: Dictionary containing community details (optional)
    :type community_details: dict, None
    :returns: Boolean value indicating if top level categories are enabled on community pages
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return get_community_field(khoros_object, 'tlc_set_on_community_page', community_details)
