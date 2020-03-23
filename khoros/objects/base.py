# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.base
:Synopsis:          This module handles general (i.e. object-agnostic) functions relating to API objects.
:Usage:             ``from khoros.objects import base``
:Example:           ``node_id = base.get_node_id('https://community.khoros.com/t5/Khoros-Blog/bg-p/relnote', 'blog')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     22 Mar 2020
"""

import re

from .. import errors


def get_node_id(url, node_type=None):
    """This function retrieves the Node ID for a given node within a URL.

    :param url: The URL from which to parse out the Node ID
    :type url: str
    :param node_type: The node type (e.g. ``blog``, ``tkb``, ``message``, etc.) for the object in the URL
    :type node_type: str, NoneType
    :returns: The Node ID retrieved from the URL
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`,
             :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    """
    if not node_type:
        # Attempt to get the Node Type from the URL
        node_type = get_node_type_from_url(url)
    elif node_type not in Mapping.node_url_mapping:
        node_type = __get_node_type_identifier(node_type)
    node_url_segment = Mapping.node_url_mapping.get(node_type) + '/'
    if node_url_segment not in url:
        raise errors.exceptions.InvalidNodeTypeError(val=node_type)
    node_id = re.sub(f'/.*$', '', re.sub(r'^.*' + node_url_segment, '', url))
    if not node_id or len(node_id) == 0:
        raise errors.exceptions.NodeIDNotFoundError(val=url)
    return node_id


def __get_node_type_identifier(_node_type_lookup):
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


class Mapping:
    """This class includes dictionaries that map API fields and values to those used in this SDK."""
    node_url_mapping = {
        'category': 'ct-p',
        'blog': 'bg-p',
        'contest': 'con-p',
        'forum': 'bd-p',
        'group': 'gp-p',
        'idea': 'idb-p',
        'message': 'm-p',
        'qa': 'qa-p',
        'tkb': 'tkb-p'
    }
    proper_name_mapping = {
        'Category': 'category',
        'Blog': 'blog',
        'Contest': 'contest',
        'Forum': 'forum',
        'Group': 'group',
        'Idea Exchange': 'idea',
        'Message': 'message',
        'Q&A': 'qa',
        'TKB': 'tkb'
    }
