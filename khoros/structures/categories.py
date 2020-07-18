# -*- coding: utf-8 -*-
"""
:Module:            khoros.structures.categories
:Synopsis:          This module contains functions specific to categories within the Khoros Community platform
:Usage:             ``from khoros.structures import categories``
:Example:           ``category_id = categories.get_category_id(url)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

import warnings

from . import base
from ..utils import log_utils
from .. import api, liql, errors

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def create(khoros_object, category_id, category_title, parent_id=None, return_json=True):
    """This function creates a new category.

    .. versionadded:: 2.5.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param category_id: The Category ID of the new category (e.g. ``video-games``)
    :type category_id: str
    :param category_title: The title of the new category (e.g. ``Video Games``)
    :type category_title: str
    :param parent_id: The Category ID of the parent category (optional)
    :type parent_id: str, None
    :param return_json: Determines whether or not the response should be returned in JSON format (``True`` by default)
    :type return_json: bool
    :returns: The response from the API call
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.APIConnectionError`
    """
    parent_url = f"categories/id/{parent_id}/" if parent_id else ""
    endpoint = f"{parent_url}categories/add"
    query_params = {
        'category.id': category_id,
        'category.title': category_title
    }
    return api.make_v1_request(khoros_object, endpoint, query_params, 'POST', return_json)


def get_category_id(url):
    """This function retrieves the Category ID for a given category when provided its URL.

    .. versionchanged:: 2.6.0
       The function was refactored to leverage the :py:func:`khoros.structures.base.get_structure_id` function.

    :param url: The URL from which to parse out the Category ID
    :type url: str
    :returns: The Category ID retrieved from the URL
    :raises: :py:exc:`khoros.errors.exceptions.InvalidURLError`
    """
    return base.get_structure_id(url)


def get_total_count(khoros_object):
    """This function returns the total number of categories within the Khoros Community environment.

    .. versionadded:: 2.6.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :returns: The total number of categories as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return liql.get_total_count(khoros_object, 'categories')


def get_total_category_count(khoros_object):
    """This function returns the total number of categories within the Khoros Community environment.

    .. deprecated:: 2.6.0
       Use the :py:func:`khoros.structures.categories.get_total_count` function instead.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :returns: The total number of categories as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    warnings.warn("The 'khoros.structures.categories.get_total_category_count' function has been deprecated by the"
                  "'khoros.structures.categories.get_total_count' function and will be removed in a future release.",
                  DeprecationWarning)
    return get_total_count(khoros_object)


def category_exists(khoros_object, category_id=None, category_url=None):
    """This function checks to see if a category exists.

    .. versionadded:: 2.7.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param category_id: The ID of the category to check
    :type category_id: str, None
    :param category_url: The URL of the category to check
    :type category_url: str, None
    :returns: Boolean value indicating whether or not the category already exists
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    return base.structure_exists(khoros_object, 'category', category_id, category_url)


def get_category_details(khoros_object, identifier, first_item=True):
    """This function returns a dictionary of category configuration settings.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The Category ID or Category URL with which to identify the category
    :type identifier: str
    :param first_item: Filters the response data to the first item returned (``True`` by default)
    :type first_item: bool
    :returns: The category details within a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    return base.get_details(khoros_object, identifier, 'category', first_item)


def get_category_field(khoros_object, field, identifier=None, category_details=None):
    """This function returns a specific category field from the Khoros Community API.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param field: The field from the :py:class:`khoros.structures.base.Mapping` class whose value should be returned
    :type field: str
    :param identifier: The Category ID or Category URL with which to identify the category
    :type identifier: str, None
    :param category_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type category_details: dict, None
    :returns: The requested field in its native format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    return base.get_structure_field(khoros_object, field, identifier, structure_type='category',
                                    details=category_details)


def get_url(khoros_object, category_id=None, category_details=None):
    """This function retrieves the URL of a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param category_id: The ID of the category to be evaluated (optional if ``category_details`` dictionary is provided)
    :type category_id: str, None
    :param category_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type category_details: dict, None
    :returns: The full URL of the category
    :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    category_url = get_category_field(khoros_object, 'view_href', category_id, category_details)
    if '://' not in category_url:
        base_url = khoros_object.core['community_url']
        category_url = f"{base_url}{get_category_field(khoros_object, 'view_href', category_id, category_details)}"
    return category_url


def get_title(khoros_object, identifier=None, full_title=True, short_title=False, category_details=None):
    """This function retrieves the full and/or short title of the category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The Category ID or Category URL with which to identify the category
    :type identifier: str, None
    :param full_title: Return the full title of the category (``True`` by default)
    :type full_title: bool
    :param short_title: Return the short title of the category (``False`` by default)
    :type short_title: bool
    :param category_details: Dictionary containing category details (optional)
    :type category_details: dict, None
    :returns: The category title(s) as a string or a tuple of strings
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not full_title and not short_title:
        exc_msg = "Must return at least the full title or the short title."
        raise errors.exceptions.MissingRequiredDataError(exc_msg)
    if not category_details:
        category_details = get_category_details(khoros_object, identifier)
    titles = (category_details['title'], category_details['short_title'])
    if not short_title:
        titles = titles[0]
    elif not full_title:
        titles = titles[1]
    return titles


def get_description(khoros_object, identifier=None, category_details=None):
    """This function retrieves the description for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'description', identifier, category_details)


def get_parent_type(khoros_object, identifier=None, category_details=None):
    """This function retrieves the parent type for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'parent_type', identifier, category_details)


def get_parent_id(khoros_object, identifier=None, category_details=None):
    """This function retrieves the parent ID for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'parent_id', identifier, category_details)


def get_parent_url(khoros_object, identifier=None, category_details=None):
    """This function retrieves the parent URL for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'parent_view_href', identifier, category_details)


def get_root_type(khoros_object, identifier=None, category_details=None):
    """This function retrieves the root category type for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'root_type', identifier, category_details)


def get_root_id(khoros_object, identifier=None, category_details=None):
    """This function retrieves the root category ID for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'root_id', identifier, category_details)


def get_root_url(khoros_object, identifier=None, category_details=None):
    """This function retrieves the root category URL for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'root_view_href', identifier, category_details)


def get_language(khoros_object, identifier=None, category_details=None):
    """This function retrieves the defined language for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'language', identifier, category_details)


def is_hidden(khoros_object, identifier=None, category_details=None):
    """This function identifies whether or not a given category is hidden.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'hidden', identifier, category_details)


def get_views(khoros_object, identifier=None, category_details=None):
    """This function retrieves the total view count for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'views', identifier, category_details)


def friendly_date_enabled(khoros_object, identifier=None, category_details=None):
    """This function identifies if friendly dates are enabled for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'friendly_date_enabled', identifier, category_details)


def get_friendly_date_max_age(khoros_object, identifier=None, category_details=None):
    """This function retrieves the maximum age where friendly dates should be used (if enabled) for a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'friendly_date_max_age', identifier, category_details)


def get_active_skin(khoros_object, identifier=None, category_details=None):
    """This function retrieves the skin being used with a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'skin', identifier, category_details)


def get_depth(khoros_object, identifier=None, category_details=None):
    """This function retrieves the depth of a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'depth', identifier, category_details)


def get_position(khoros_object, identifier=None, category_details=None):
    """This function retrieves the position of a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'position', identifier, category_details)


def get_creation_date(khoros_object, identifier=None, category_details=None):
    """This function retrieves the creation date of a given category.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_category_field(khoros_object, 'get_creation_date', identifier, category_details)

