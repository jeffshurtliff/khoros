# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_node_id_extract
:Synopsis:          This module is used by pytest to verify that Node IDs can be extracted successfully from URLs.
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     11 Mar 2021
:Version:           1.0.2
"""

import os
import sys

import pytest


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list."""
    sys.path.insert(0, os.path.abspath('../..'))
    return


def get_test_data():
    """This function retrieves the test data that will be used in the test functions.

    :returns: The ``test_data`` dictionary with the node types and associated test URLs
    """
    base_test_url = "https://community.khoros.com/t5"
    test_data = {
        'blog': f'{base_test_url}/Khoros-Now-Blog/bg-p/relnote',
        'board': f'{base_test_url}/Growing-Successful-Communities/bd-p/growingcommunities',
        'category': f'{base_test_url}/Forums/ct-p/Forums',
        'contest': f'{base_test_url}/Concert-Photo-Contest/con-p/vacationPhotoContest',
        'group': f'{base_test_url}/Khoros-Rockstars/gp-p/khorosRockstars',
        'idea': f'{base_test_url}/Big-Ideas/idb-p/bigIdeas',
        'message': f'{base_test_url}/Womens-Running-Shoes/Looking-for-an-idea-on-which-of-these-to-choose/m-p/997#M78',
        'qa': f'{base_test_url}/Ask-a-Baker/qa-p/bakingqanda',
        'tkb': f'{base_test_url}/Getting-Started/tkb-p/gettingStarted'
    }
    return test_data


def test_with_valid_node_types():
    """This function tests that Node IDs can be extracted from URLs when valid node types are given.

    :returns: None
    :raises: :py:exc:`AssertionError`, :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`khoros.errors.exceptions.NodeIDNotFoundError`,
             :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    """
    # Import the base module
    set_package_path()
    from khoros.structures import nodes

    # Get the test data
    test_data = get_test_data()

    # Perform the test for each key value pair
    for node_type, url in test_data.items():
        node_id = nodes.get_node_id(url, node_type)
        assert (node_id is not False) and (len(node_id) != 0)       # nosec
    return


def test_with_invalid_node_types():
    """This function tests to ensure that invalid node types will raise the appropriate exception.

    :returns: None
    :raises: :py:exc:`AssertionError`, :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    # Import the base and exceptions modules
    set_package_path()
    from khoros.structures import nodes
    from khoros.errors import exceptions

    # Get the test data
    test_data = get_test_data()

    # Test passing a made-up node type
    with pytest.raises(exceptions.InvalidNodeTypeError):
        nodes.get_node_id(test_data.get('blog'), 'gonna_break')

    # Test passing the wrong node type for a given URL
    with pytest.raises(exceptions.InvalidNodeTypeError):
        nodes.get_node_id(test_data.get('group'), 'tkb')

    # Return when finished
    return


def test_with_only_url():
    """This function tests the :py:func:`khoros.objects.base.get_node_id` function when only a URL is passed.

    :returns: None
    :raises: :py:exc:`AssertionError`
    """
    # Import the base module
    set_package_path()
    from khoros.structures import nodes

    # Get the test data
    test_data = get_test_data().values()

    # Test getting the Node ID for each URL type
    for url in test_data:
        node_id = nodes.get_node_id(url)
        assert (node_id is not False) and (len(node_id) != 0)       # nosec
    return


def test_url_without_node():
    """This function tests to ensure that an appropriate exception is raised when a URL does not contain a valid node.

    :returns: None
    :raises: :py:exc:`AssertionError`, :py:exc:`khoros.errors.exceptions.NodeTypeNotFoundError`
    """
    # Import the base and exceptions modules
    set_package_path()
    from khoros.structures import nodes
    from khoros.errors import exceptions

    # Test passing a URL that does not have a node within it
    with pytest.raises(exceptions.NodeTypeNotFoundError):
        nodes.get_node_id('https://community.khoros.com/this-is-a-test-url')
    return
