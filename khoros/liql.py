# -*- coding: utf-8 -*-
"""
:Module:            khoros.liql
:Synopsis:          Collection of functions and classes to leverage the Community API v2 and LiQL for searches
:Usage:             ``from khoros import liql`` (Imported by default in :py:mod:`khoros.core` package)
:Example:           ``query_url = liql.format_query("SELECT * FROM messages WHERE id = '2' LIMIT 1")``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     21 Mar 2020
"""

import requests

from . import api, errors
from .utils.core_utils import convert_set


def format_query(query, pretty_print=False, track_in_lsi=False, always_ok=False, error_code='', format_statements=True):
    """This function formats and URL-encodes a raw LiQL query to be able to use it within a Community v2 API URL.

    :param query: The LiQL query to be formatted and url-encoded
    :type query: str
    :param pretty_print: Defines if the response should be "pretty printed" (``False`` by default)
    :type pretty_print: bool
    :param track_in_lsi: Defines if the query should be tracked within LSI (``False`` by default)
    :type track_in_lsi: bool
    :param always_ok: Defines if the HTTP response should **always** be ``200 OK`` (``False`` by default)
    :type always_ok: bool
    :param error_code: Allows an error code to optionally be supplied for testing purposes (ignored by default)
    :type error_code: str
    :param format_statements: Determines if statements (e.g. ``SELECT``, ``FROM``, et.) should be formatted to be in
                              all caps (``True`` by default)
    :type format_statements: bool
    :returns: The properly formatted query to be inserted in the URL
    """
    chars_to_encode = {
        ' ': '+',
        '=': '%3D'
    }
    query_statements = {
        'select': 'SELECT',
        'from': 'FROM',
        'where': 'WHERE',
        'order by': 'ORDER BY',
        'desc': 'DESC ',
        'limit': 'LIMIT',
        'asc': 'ASC',
        'offset': 'OFFSET'
    }
    parameters = {
        'pretty_print': '&api.pretty_print=true',
        'track_in_lsi': '&api.for_ui_search=true',
        'always_ok': '&api.always_ok',
        'error_code': '&api.error_code='
    }
    replacements = [chars_to_encode]
    if format_statements:
        replacements.append(query_statements)
    for criteria in replacements:
        for orig_string, new_string in criteria.items():
            query = query.replace(orig_string, new_string)
    if pretty_print:
        query = f"{query}{parameters.get('pretty_print')}"
    if track_in_lsi:
        query = f"{query}{parameters.get('track_in_lsi')}"
    if always_ok:
        query = f"{query}{parameters.get('always_ok')}"
    if error_code != '':
        query = f"{query}{parameters.get('error_code')}{error_code}"
    return query


def get_query_url(core_dict, query, pretty_print=False, track_in_lsi=False, always_ok=False,
                  error_code='', format_statements=True):
    """This function defines the full Community API v2 query URL for the LiQL query.

    :param core_dict: The ``core`` dictionary defined in the :py:class:`khoros.core.Khoros` object
    :type core_dict: dict
    :param query: The LiQL query to be encoded and embedded in the URL
    :type query: str
    :param pretty_print: Defines if the response should be "pretty printed" (``False`` by default)
    :type pretty_print: bool
    :param track_in_lsi: Defines if the query should be tracked within LSI (``False`` by default)
    :type track_in_lsi: bool
    :param always_ok: Defines if the HTTP response should **always** be ``200 OK`` (``False`` by default)
    :type always_ok: bool
    :param error_code: Allows an error code to optionally be supplied for testing purposes (ignored by default)
    :type error_code: str
    :param format_statements: Determines if statements (e.g. ``SELECT``, ``FROM``, et.) should be formatted to be in
                              all caps (``True`` by default)
    :type format_statements: bool
    :returns: The full Community API v2 URL in string format
    """
    query = format_query(query, pretty_print, track_in_lsi, always_ok, error_code, format_statements)
    return f"{core_dict['v2_base']}/search?q={query}"


def perform_query(khoros_object, query_url, return_json=True):
    """This function performs a LiQL query using full Community API v2 URL containing the query."

    :param khoros_object: The Khoros object initialized via the :py:mod:`khoros.core` module
    :type khoros_object: class[khoros.Khoros]
    :param query_url: The full Khoros Community API v2 URL for the query
    :type query_url: str
    :param return_json: Determines if the response should be returned in JSON format (``True`` by default)
    :type return_json: bool
    :returns: The API response (in JSON format by default)
    :raises: :py:exc:`khoros.errors.exceptions.MissingAuthDataError`
    """
    if 'header' not in khoros_object.auth:
        error_msg = f"Cannot perform the query as an authorization header is not configured."
        raise errors.exceptions.MissingAuthDataError(error_msg)
    response = api.get_request_with_retries(query_url, return_json, auth_dict=khoros_object.auth)
    if return_json and type(response) != dict:
        response = response.json()
    return response


def parse_query_elements(select_fields, from_source, where_filter="", order_by=None, order_desc=True, limit=0):
    """This function parses query elements to construct a full LiQL query in the appropriate syntax.

    :param select_fields: One or more fields to be selected within the SELECT statement (e.g. ``id``)
    :type select_fields: str, tuple, list, set
    :param from_source: The source of the data to use in the FROM statement (e.g. ``messages``)
    :type from_source: str
    :param where_filter: The filters (if any) to use in the WHERE clause (e.g. ``id = '2'``)
    :type where_filter: str, tuple, list, dict, set
    :param order_by: The field(s) by which to order the response data (optional)
    :type order_by: str, tuple, set, dict, list
    :param order_desc: Defines if the ORDER BY directionality is DESC (default) or ASC
    :type order_desc: bool
    :param limit: Allows an optional limit to be placed on the response items (ignored by default)
    :type limit: int
    :returns: The query response in JSON format
    :raises: :py:exc:`khoros.errors.exceptions.OperatorMismatchError`,
             :py:exc:`khoros.errors.exceptions.InvalidOperatorError`
    """
    # Properly format the provided SELECT fields
    select_fields = __parse_select_fields(select_fields)

    # Establish the base syntax to return
    full_syntax = f"SELECT {select_fields} FROM {from_source}"

    # Append the WHERE clause to the syntax if provided
    if type(where_filter) != str:
        where_filter = __parse_where_clause(where_filter)
    if where_filter != "":
        full_syntax = f"{full_syntax} WHERE {where_filter}"

    # Append the ORDER BY clause to the syntax is provided
    if order_by:
        order_direction = {True: 'DESC', False: 'ASC'}
        if type(order_by) in LiQLSyntax.container_types:
            order_by = convert_set(order_by)
            order_by = ','.join(order_by)
        order_by_clause = f"ORDER BY {order_by} {order_direction.get(order_desc)}"
        full_syntax = f"{full_syntax} {order_by_clause}"

    # Append the LIMIT clause to the syntax if provided
    limit_set = True if limit > 0 else False
    if limit_set:
        limit_syntax = {True: f"LIMIT {limit}", False: ""}
        full_syntax = f"{full_syntax} {limit_syntax.get(limit_set)}"

    # Return the fully parsed query syntax
    return full_syntax


def __parse_select_fields(_select_fields):
    """This function parses the fields to be used in the SELECT statement of the LiQL query.

    :param _select_fields: The field(s) to be used in the SELECT statement
    :type _select_fields: str, tuple, list, set
    :returns: The properly formatted SELECT fields in string format (comma-separated)
    """
    if type(_select_fields) == tuple or type(_select_fields) == list or type(_select_fields) == set:
        _select_fields = convert_set(_select_fields)
        _select_fields = ",".join(_select_fields)
    elif type(_select_fields) == str:
        _select_fields = _select_fields.replace(';', ',').replace(', ', ',')
    return _select_fields


def __wrap_string_vales(_where_value):
    """This function wraps values going in the WHERE clause in single-quotes if they are not integers.

    :param _where_value: The value to be evaluated and potentially wrapped in single-quotes
    :returns: The value in int or string format
    """
    try:
        _where_value = int(_where_value)
    except (TypeError, ValueError):
        _where_value = f"'{_where_value}'"
    return _where_value


def __convert_where_dicts_to_lists(_dict_list):
    """This function converts dictionaries supplied as WHERE clause filters into properly formatted lists.

    :param _dict_list: A list of dictionaries with the WHERE clause information
    :type _dict_list: list
    :returns: A list of lists containing the WHERE clause information
    """
    _master_list = []
    for _where_dict in _dict_list:
        for _dict_key, _dict_val in _where_dict.items():
            _single_list = [_dict_key]
            if type(_dict_val) == tuple or type(_dict_val) == list or type(_dict_val) == set:
                _dict_val = convert_set(_dict_val)
                if len(_dict_val) == 2:
                    for _val in _dict_val:
                        _single_list.append(_val)
                else:
                    raise errors.exceptions.OperatorMismatchError
            else:
                _single_list.append(_dict_val)
            _master_list.append(_single_list)
    return _master_list


def __parse_where_clause(_where, _join_logic='AND'):
    """This function parses the data supplied for the WHERE clause of a LiQL query.

    :param _where: The WHERE clause information
    :type _where: str, tuple, list, set, dict
    :param _join_logic: The logic to use
    :type _join_logic: str, tuple, list
    :returns: A properly formatted WHERE clause (excluding the WHERE statement at the beginning)
    :raises: InvalidOperatorError, OperatorMismatchError
    """
    # Examples:
    #   _where = ('id', 5)      #2-length tuple
    #   _where = ('id', '>', 5)     # 3-length tuple
    #   _where = (('id', 5), ('id', 6))     # tuple of tuples
    #   _where = [('replies.count(*)', '>', 5), ('replies.count(*)', '<', 10)]      # list of tuples
    #   _where = {('id', 5), ('replies.count(*)', '=', 0)}      # set
    #   _where = {'id': 5, 'replies.count(*)': 0}       # one-to-one dict
    #   _where = {'id': ('>', 5), 'id': ('<', 10)}      # one-to-two dict

    # Add them into a list as needed
    if type(_where) != list:
        if type(_where) == dict:
            _where = __convert_where_dicts_to_lists([_where])
        if (type(_where) == tuple or type(_where) == set) and len(_where) > 1:
            _where = convert_set(_where)
            if type(_where[0]) not in LiQLSyntax.container_types:
                _where = [_where]

    # Determine the multi-clause logic to use
    # TODO: Figure out how to allow where clause grouping with logic
    if type(_join_logic) == str:
        if _join_logic not in LiQLSyntax.logic_operators:
            raise errors.exceptions.InvalidOperatorError
        _join_logic = [_join_logic]
    elif len(_join_logic) == 1:
        if _join_logic[0] not in LiQLSyntax.logic_operators:
            raise errors.exceptions.InvalidOperatorError
        else:
            _join_logic = [_join_logic[0]]
    else:
        if len(_join_logic) != len(_where) - 1:
            raise errors.exceptions.OperatorMismatchError
        if type(_join_logic) != list:
            _join_logic = list(_join_logic)

    # Parse the where clause
    _full_clause = ""
    _num_clauses = len(_where)
    while _num_clauses > 0:
        for _clause in _where:
            # Adjust spacing between existing parsed clause and new clause section
            if len(_full_clause) > 0:
                _full_clause = f"{_full_clause} "

            # Parse the individual clause
            if len(_clause) == 2:
                _full_clause = f"{_full_clause}{_clause[0]} = {__wrap_string_vales(_clause[-1])}"
            elif len(_clause) == 3:
                if _clause[1] not in LiQLSyntax.comparison_operators:
                    raise errors.exceptions.InvalidOperatorError
                _full_clause = f"{_full_clause}{_clause[0]} {_clause[1]} {__wrap_string_vales(_clause[-1])}"
            elif type(_clause) == str:
                _full_clause = f"{_full_clause}{_clause}"

            # Add the logic statement to join multiple clauses as necessary
            if _num_clauses > 1:
                _multi_clause_logic = _join_logic[0]
                _join_logic.remove(_join_logic[0])
                _full_clause = f"{_full_clause} {_multi_clause_logic}"

            # Decrement the number of clauses
            _num_clauses -= 1

    # Return the fully parsed WHERE clause
    return _full_clause


class LiQLSyntax:
    """This class defines lists of syntax elements for use in LiQL queries."""
    comparison_operators = ['=', '!=', '>', '<', '>=', '<=']
    logic_operators = ['AND', 'OR', 'IN', 'MATCHES']
    order_operators = ['ASC', 'DESC']
    container_types = [tuple, set, dict, list]
