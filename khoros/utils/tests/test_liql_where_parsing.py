# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_liql_where_parsing
:Synopsis:       This module is used by pytest to verify that LiQL WHERE clauses can be parsed successfully.
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  24 Feb 2021
"""

import os
import sys


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list."""
    sys.path.insert(0, os.path.abspath('../..'))
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


def test_where_clause_parsing():
    """This function tests to confirm that LiQL WHERE clauses are getting parsed properly without failing."""
    set_package_path()
    assert parse_where_clauses() is True
