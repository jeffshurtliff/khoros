# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.base
:Synopsis:          This module handles general (i.e. object-agnostic) functions relating to API objects.
:Usage:             ``from khoros.objects import base``
:Example:           ``node_id = base.get_node_id('https://community.khoros.com/t5/Khoros-Blog/bg-p/relnote', 'blog')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

import warnings

from ..structures import nodes
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_node_id(url, node_type=None):
    """This **deprecated** function retrieves the Node ID for a given node within a URL.

    .. deprecated:: 2.1.0
       Use :py:func:`khoros.structures.nodes.get_node_id` instead.

    :param url: The URL from which to parse out the Node ID
    :type url: str
    :param node_type: The node type (e.g. ``blog``, ``tkb``, ``message``, etc.) for the object in the URL
    :type node_type: str, NoneType
    :returns: The Node ID retrieved from the URL
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`,
             :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    """
    warnings.warn("The 'khoros.objects.base.get_node_id' function has been deprecated. Use " +
                  "'khoros.structures.nodes.get_node_id' instead.", DeprecationWarning)
    return nodes.get_node_id(url, node_type)


def __get_node_type_identifier(_node_type_lookup):
    """This **deprecated** function attempts to identify the appropriate node type for a function.

    .. deprecated:: 2.1.0
       Use :py:func:`khoros.structures.nodes._get_node_type_identifier` instead.

    :param _node_type_lookup: The value to look up as a node type
    :type _node_type_lookup: str
    :returns: The appropriate node type (if found)
    :raises: :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    warnings.warn("The 'khoros.objects.base.__get_node_type_identifier' function has been deprecated. Use " +
                  "'khoros.structures.nodes._get_node_type_identifier' instead.", DeprecationWarning)
    return nodes._get_node_type_identifier(_node_type_lookup)


def get_node_type_from_url(url):
    """This function attempts to retrieve a node type by analyzing a supplied URL.

    .. deprecated:: 2.1.0
       Use :py:func:`khoros.structures.nodes.get_node_type_from_url` instead.

    :param url: The URL from which to extract the node type
    :type url: str
    :returns: The node type based on the URL provided
    :raises: :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    """
    warnings.warn("The 'khoros.objects.base.get_node_type_from_url' function has been deprecated. Use " +
                  "'khoros.structures.nodes.get_node_type_from_url' instead.", DeprecationWarning)
    return nodes.get_node_type_from_url(url)


class Mapping:
    """This class includes dictionaries that map API fields and values to those used in this SDK.

    .. deprecated:: 2.1.0
       Use :py:class:`khoros.structures.nodes.Mapping` instead.
    """
    warnings.warn("The 'khoros.objects.base.Mapping' class has been deprecated. Use " +
                  "'khoros.structures.nodes.Mapping' instead.", DeprecationWarning)
    node_url_mapping = nodes.Mapping.node_url_mapping
    proper_name_mapping = nodes.Mapping.proper_name_mapping
