# -*- coding: utf-8 -*-
"""
:Module:            khoros.structures.nodes
:Synopsis:          This module contains functions specific to nodes within the Khoros Community platform
:Usage:             ``from khoros.structures import nodes``
:Example:           ``node_id = nodes.get_id(url)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Mar 2021
"""

import re

from . import base
from .. import liql, errors
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_node_id(url=None, node_type=None, node_details=None):
    """This function retrieves the Node ID for a given node within a URL.

    :param url: The URL from which to parse out the Node ID
    :type url: str, None
    :param node_type: The node type (e.g. ``blog``, ``tkb``, ``message``, etc.) for the object in the URL
    :type node_type: str, None
    :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type node_details: dict, None
    :returns: The Node ID retrieved from the URL
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`,
             :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    """
    if not url and not node_details:
        raise errors.exceptions.MissingRequiredDataError("A node URL or dictionary with node details must be given.")
    if node_details:
        node_id = node_details['id'].split(':')[1]
    else:
        if not node_type:
            # Attempt to get the Node Type from the URL
            node_type = get_node_type_from_url(url)
        elif node_type not in Mapping.node_url_mapping:
            node_type = _get_node_type_identifier(node_type)
        node_url_segment = Mapping.node_url_mapping.get(node_type) + '/'
        if node_url_segment not in url:
            raise errors.exceptions.InvalidNodeTypeError(val=node_type)
        node_id = re.sub(r'/.*$', '', re.sub(r'^.*' + node_url_segment, '', url))
        if not node_id or len(node_id) == 0:
            raise errors.exceptions.NodeIDNotFoundError(val=url)
    return node_id


def _get_node_type_identifier(_node_type_lookup):
    """This function attempts to identify the appropriate node type for a function.

    :param _node_type_lookup: The value to look up as a node type
    :type _node_type_lookup: str
    :returns: The appropriate node type (if found)
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    if _node_type_lookup in Mapping.proper_name_mapping:
        _node_type = Mapping.proper_name_mapping.get(_node_type_lookup)
    else:
        raise errors.exceptions.InvalidNodeTypeError(val=_node_type_lookup)
    return _node_type


def get_node_type_from_url(url):
    """This function attempts to retrieve a node type by analyzing a supplied URL.

    :param url: The URL from which to extract the node type
    :type url: str
    :returns: The node type based on the URL provided
    :raises: :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    """
    node_type = None
    for node_type_name, node_url_code in Mapping.node_url_mapping.items():
        if node_url_code in url:
            node_type = node_type_name
            break
    if not node_type:
        raise errors.exceptions.NodeTypeNotFoundError(val=url)
    return node_type


def get_total_node_count(khoros_object):
    """This function returns the total number of nodes within the Khoros Community environment.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :returns: The total number of nodes as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    return liql.get_total_count(khoros_object, 'nodes')


def node_exists(khoros_object, node_id=None, node_url=None):
    """This function checks to see if a node exists.

    .. versionadded:: 2.7.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param node_id: The ID of the node to check
    :type node_id: str, None
    :param node_url: The URL of the node to check
    :type node_url: str, None
    :returns: Boolean value indicating whether or not the node already exists
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    return base.structure_exists(khoros_object, 'node', node_id, node_url)


def get_node_details(khoros_object, identifier, first_item=True):
    """This function returns a dictionary of node configuration settings.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The Node ID or Node URL with which to identify the node
    :type identifier: str
    :param first_item: Filters the response data to the first item returned (``True`` by default)
    :type first_item: bool
    :returns: The node details within a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    return base.get_details(khoros_object, identifier, 'node', first_item)


def get_node_field(khoros_object, field, identifier=None, node_details=None):
    """This function returns a specific node field from the Khoros Community API.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param field: The field from the :py:class:`khoros.structures.base.Mapping` class whose value should be returned
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
    if field == 'view_href' or field == 'url':
        field_value = get_url(khoros_object, identifier, node_details)
    elif field == 'id':
        field_value = get_node_id(identifier, node_details=node_details)
    else:
        field_value = base.get_structure_field(khoros_object, field, identifier,
                                               structure_type='node', details=node_details)
    return field_value


def get_url(khoros_object, node_id=None, node_details=None):
    """This function returns the full URL of a given Node ID.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param node_id: The Node ID with which to identify the node
    :type node_id: str, None
    :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type node_details: dict, None
    :returns: The node URl as a string
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not node_id and not node_details:
        raise errors.exceptions.MissingRequiredDataError("A Node ID or a dictionary with node details must be given.")
    elif not node_id or ('/' in node_id and node_details):
        node_id = get_node_id(node_details=node_details)
    query = f"SELECT view_href FROM nodes WHERE id = '{node_id}'"       # nosec
    response = liql.perform_query(khoros_object, liql_query=query)
    return response['data']['items'][0]['view_href']


def get_type(khoros_object, identifier, node_details=None):
    """This function returns the full URL of a given Node ID.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'node_type', identifier, node_details)


def get_discussion_style(khoros_object, identifier, node_details=None):
    """This function returns the full URL of a given Node ID.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'discussion_style', identifier, node_details)


def get_title(khoros_object, identifier=None, full_title=True, short_title=False, node_details=None):
    """This function retrieves the full and/or short title of the node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    if not full_title and not short_title:
        exc_msg = "Must return at least the full title or the short title."
        raise errors.exceptions.MissingRequiredDataError(exc_msg)
    if not node_details:
        node_details = get_node_details(khoros_object, identifier)
    titles = (node_details['title'], node_details['short_title'])
    if not short_title:
        titles = titles[0]
    elif not full_title:
        titles = titles[1]
    return titles


def get_description(khoros_object, identifier, node_details=None):
    """This function returns the description of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'description', identifier, node_details)


def get_parent_type(khoros_object, identifier, node_details=None):
    """This function returns the parent type of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'parent_type', identifier, node_details)


def get_parent_id(khoros_object, identifier, node_details=None, include_prefix=False):
    """This function returns the Parent ID of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The Node ID or Node URL with which to identify the node
    :type identifier: str, None
    :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type node_details: dict, None
    :param include_prefix: Determines if the prefix (e.g. ``category:``) should be included (``False`` by default)
    :type include_prefix: bool
    :returns: The Parent ID as a string
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    parent_id = get_node_field(khoros_object, 'parent_id', identifier, node_details)
    if not include_prefix:
        parent_id = parent_id.split(':')[1]
    return parent_id


def get_parent_url(khoros_object, identifier, node_details=None):
    """This function returns the parent URL of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    parent_id = get_parent_id(khoros_object, identifier, node_details, include_prefix=False)
    return get_url(khoros_object, parent_id)


def get_root_type(khoros_object, identifier, node_details=None):
    """This function returns the root category type of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'root_type', identifier, node_details)


def get_root_id(khoros_object, identifier, node_details=None, include_prefix=False):
    """This function returns the Root Category ID of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The Node ID or Node URL with which to identify the node
    :type identifier: str, None
    :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type node_details: dict, None
    :param include_prefix: Determines if the prefix (e.g. ``category:``) should be included (``False`` by default)
    :type include_prefix: bool
    :returns: The Root Category ID as a string
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    root_id = get_node_field(khoros_object, 'root_id', identifier, node_details)
    if not include_prefix:
        root_id = root_id.split(':')[1]
    return root_id


def get_root_url(khoros_object, identifier, node_details=None):
    """This function returns the root category URL of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    root_id = get_root_id(khoros_object, identifier, node_details, include_prefix=False)
    return get_url(khoros_object, root_id)


# noinspection PyTypeChecker
def get_avatar_url(khoros_object, identifier, node_details=None, original=True, tiny=False, small=False,
                   medium=False, large=False):
    """This function retrieves one or more avatar URLs for a given node.

            .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The Node ID or Node URL with which to identify the node
    :type identifier: str, None
    :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type node_details: dict, None
    :param original: Indicates if the URL for the image in its original size should be returned (``True`` by default)
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
    if not original and not tiny and not small and not medium and not large:
        raise errors.exceptions.MissingRequiredDataError("At least one file size must be enabled.")
    avatar_details = get_node_field(khoros_object, 'avatar_details', identifier, node_details)
    avatar_urls, file_sizes = {}, {'tiny': tiny, 'small': small, 'medium': medium, 'large': large}
    if original:
        avatar_urls['original'] = avatar_details['tiny_href'].split('/image-size/')[0]
    for size in file_sizes:
        if file_sizes.get(size):
            avatar_urls[size] = avatar_details[Mapping.avatar_size_mapping.get(size)]
    if len(avatar_urls) == 1:
        avatar_urls = list(avatar_urls.values())[0]
    return avatar_urls


def get_creation_date(khoros_object, identifier, node_details=None, friendly=False):
    """This function returns the creation date of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The Node ID or Node URL with which to identify the node
    :type identifier: str, None
    :param node_details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type node_details: dict, None
    :param friendly: Determines whether to return the "friendly" date (e.g. ``Friday``) instead (``False`` by default)
    :type friendly: bool
    :returns: The creation date as a string
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    # TODO: Allow a format to be specified and the ability to parse as a datetime object if needed
    if friendly:
        creation_date = get_node_field(khoros_object, 'creation_date_friendly', identifier, node_details)
    else:
        creation_date = get_node_field(khoros_object, 'creation_date', identifier, node_details)
    return creation_date


def get_depth(khoros_object, identifier, node_details=None):
    """This function returns the depth of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'depth', identifier, node_details)


def get_position(khoros_object, identifier, node_details=None):
    """This function returns the position of a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'position', identifier, node_details)


def is_hidden(khoros_object, identifier, node_details=None):
    """This function identifies whether or not a given node is hidden.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'hidden', identifier, node_details)


def get_views(khoros_object, identifier, node_details=None):
    """This function returns the views for a given node.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
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
    return get_node_field(khoros_object, 'views', identifier, node_details)


class Mapping:
    """This class includes dictionaries that map API fields and values to those used in this SDK."""
    node_url_mapping = {
        'category': 'ct-p',
        'blog': 'bg-p',
        'contest': 'con-p',
        'board': 'bd-p',
        'group': 'gp-p',
        'idea': 'idb-p',
        'message': 'm-p',
        'qa': 'qa-p',
        'tkb': 'tkb-p'
    }
    proper_name_mapping = {
        'Category': 'category',
        'Blog': 'blog',
        'Board': 'board',
        'Contest': 'contest',
        'Forum': 'forum',
        'Group': 'group',
        'Idea Exchange': 'idea',
        'Message': 'message',
        'Q&A': 'qa',
        'TKB': 'tkb'
    }
    avatar_size_mapping = {
        'tiny': 'tiny_href',
        'small': 'small_href',
        'medium': 'medium_href',
        'large': 'large_href'
    }
