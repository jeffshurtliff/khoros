# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_liql
:Synopsis:       This module is used by pytest to verify that LiQL queries can be performed and parsed successfully.
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  27 Jun 2021
"""

import os
import sys

import pytest

from . import resources

# Define global variables to store LiQL query responses
liql_response, liql_items = {}, None

# Define a global variable to define when the package path has been set
package_path_defined = False


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionchanged:: 4.1.0
       This function now leverages a global variable to ensure it only performs the operation once.
    """
    global package_path_defined
    if not package_path_defined:
        sys.path.insert(0, os.path.abspath('../..'))
        package_path_defined = True
    return


def parse_where_clauses():
    """This function runs through several parsing examples to ensure they all complete successfully.

    .. versionchanged:: 3.4.0
       Updated the name of the :py:func:`khoros.liql.parse_where_clause` function in its respective call.
    """
    # Import the liql module
    from khoros import liql

    # Define each test with a name
    examples = {
        '2-Length Tuple': ('id', 5),
        '3-Length Tuple': ('id', '>', 5),
        'Tuple of Tuples': (('id', 5), ('id', 6)),
        'List of Tuples': [('replies.count(*)', '>', 5), ('replies.count(*)', '<', 10)],
        'Logic Test': (('id', 5), ('id', 6), ('username', '!=', 'John')),
        'Set': {('id', 5), ('replies.count(*)', '=', 0)},
        '1-to-1 Dict': {'id': 5, 'replies.count(*)': 0},
        '1-to-2 Dict': {'id': ('>', 5), 'username': ('<', 10)}
    }

    # Perform each test
    for test_case, example in examples.items():
        # Define which logic to use per test
        if test_case == 'Logic Test':
            logic = ('AND', 'OR')
        else:
            logic = 'AND'

        # Convert any sets to lists for printing below without changing the original identifier
        if type(example) == set:
            print_example = list(example)
        else:
            print_example = example

        # Print results of each test
        print(f"Test Case:\t{test_case}")
        try:
            print(f"Length:\t\t{len(print_example)}")
            print(f"Length[0]:\t{len(print_example[0])}")
        except (KeyError, TypeError):
            pass
        print(f"Example:\t{print_example}")
        where = liql.parse_where_clause(example, logic)
        print(f"Parsed:\t\t{where}\n")
    return True


def perform_test_query(return_items=False):
    """This function performs a LiQL query and saves the response in a global variable.

    :param return_items: Determines if the response should be scoped to only the returned items (``False`` by default)
    :type return_items: bool
    :returns: None
    """
    global liql_response, liql_items
    khoros_object = resources.instantiate_with_local_helper()
    query = "SELECT login FROM users WHERE id = '3'"
    if return_items:
        liql_items = khoros_object.query(query, return_items=return_items)
    else:
        liql_response = khoros_object.query(query, return_items=return_items)
    return


def test_where_clause_parsing():
    """This function tests to confirm that LiQL WHERE clauses are getting parsed properly without failing."""
    set_package_path()
    assert parse_where_clauses() is True        # nosec


def test_liql_query():
    """This function tests to confirm that a standard LiQL query can be performed successfully.

    .. versionadded:: 4.1.0
    """
    if not resources.local_helper_exists():
        pytest.skip("skipping local-only tests")
    set_package_path()
    if not liql_response:
        perform_test_query(return_items=False)
    assert isinstance(liql_response, dict) and liql_response.get('status') == 'success'         # nosec


def test_return_items_option():
    """This function tests the ``return_items`` argument in the :py:meth:`khoros.core.Khoros.query` method.

    .. versionadded:: 4.1.0
    """
    if not resources.local_helper_exists():
        pytest.skip("skipping local-only tests")
    set_package_path()
    if not liql_items:
        perform_test_query(return_items=True)
    assert isinstance(liql_items, list)         # nosec
