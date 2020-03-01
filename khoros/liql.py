# -*- coding: utf-8 -*-
"""
:Module:            khoros.liql
:Synopsis:          Collection of functions and classes to leverage the Community API v2 and LiQL for searches
:Usage:             ``import khoros.liql`` (Imported by default in :py:mod:`khoros.core` package)``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Mar 2020
"""

import requests

from . import errors
from .utils.core_utils import convert_set


def format_query(query, pretty_print=False, track_in_lsi=False, always_ok=False, error_code='', format_statements=True):
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
    query = format_query(query, pretty_print, track_in_lsi, always_ok, error_code, format_statements)
    return f"{core_dict['v2_base']}/search?q={query}"


def perform_query(khoros_object, query_url, return_json=True):
    if 'header' not in khoros_object.auth:
        error_msg = f"Cannot perform the query as an authorization header is not configured."
        raise errors.exceptions.MissingAuthDataError(error_msg)
    response = requests.get(query_url, headers=khoros_object.auth['header'])
    if return_json:
        response = response.json()
    return response


def parse_query_elements(select_fields, from_source, where_filter="", order_by=None, order_desc=True, limit=0):
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
        print(f"ORDER BY: {order_by}")
        print(f"TYPE: {type(order_by)}")
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
    if type(_select_fields) == tuple or type(_select_fields) == list or type(_select_fields) == set:
        _select_fields = convert_set(_select_fields)
        _select_fields = ",".join(_select_fields)
    elif type(_select_fields) == str:
        _select_fields = _select_fields.replace(';', ',').replace(', ', ',')
    return _select_fields


def __wrap_string_vales(_where_value):
    try:
        _where_value = int(_where_value)
    except (TypeError, ValueError):
        _where_value = f"'{_where_value}'"
    return _where_value


def __convert_where_dicts_to_lists(_dict_list):
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
    comparison_operators = ['=', '!=', '>', '<', '>=', '<=']
    logic_operators = ['AND', 'OR', 'IN', 'MATCHES']
    order_operators = ['ASC', 'DESC']
    container_types = [tuple, set, dict, list]
