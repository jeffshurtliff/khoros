# -*- coding: utf-8 -*-
"""
:Module:            khoros.liql
:Synopsis:          Collection of functions and classes to leverage the Community API v2 and LiQL for searches
:Usage:             ``from khoros import liql`` (Imported by default in :py:mod:`khoros.core` package)
:Example:           ``query_url = liql.format_query("SELECT * FROM messages WHERE id = '2' LIMIT 1")``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Oct 2021
"""

from . import api, errors
from .utils import log_utils
from .utils.core_utils import convert_set

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)

COLLECTIONS = ['albums', 'attachments', 'boards', 'bookmarks', 'categories', 'communities', 'custom_tags',
               'floated_messages', 'grouphubs', 'images', 'inbox_notes', 'kudos', 'labels', 'me_toos',
               'membership_requests', 'messages', 'metrics', 'nodes', 'notes_threads', 'notification_feeds',
               'outbox_notes', 'product_categories', 'products', 'ranks', 'ratings', 'review_comments',
               'review_dimensions', 'review_ratings', 'reviews', 'roles', 'subscriptions', 'tags', 'threaded_notes',
               'tkb_helpfulness_ratings', 'users', 'videos']


def format_query(query, pretty_print=False, track_in_lsi=False, always_ok=False, error_code='', format_statements=True):
    """This function formats and URL-encodes a raw LiQL query to be able to use it within a Community v2 API URL.

    .. versionchanged:: 2.1.0
       Queries ending in a semicolon (``;``) will have that character stripped to avoid syntax errors.

    .. versionchanged:: 2.0.0
       Added URL-encoding support for several additional characters.

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
        '=': '%3D',
        '"': '%22',
        '\'': '%27',
        '(': '%28',
        '}': '%29',
        '@': '%40'
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
            if query.endswith(';'):
                query = query[:-1]
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


def perform_query(khoros_object, query_url=None, liql_query=None, return_json=True, verify_success=False,
                  allow_exceptions=True, verify=None, return_items=False):
    """This function performs a LiQL query using full Community API v2 URL containing the query."

    .. versionchanged:: 4.1.0
       The JSON response can now be reduced to just the returned items by passing ``return_items=True``.

    .. versionchanged:: 3.4.0
       Support has been introduced for the ``verify`` parameter to determine if SSL certificate verification is needed.

    .. versionchanged:: 2.3.0
       Added the ``allow_exceptions`` argument (``True`` by default) to allow exceptions to be disabled
       and updated the error/exception message to be more specific.

    .. versionchanged:: 2.0.0
       Added the ability for a raw LiQL query to be passed to this function rather than only a formatted query URL,
       and included the optional ``verify_success`` Boolean argument to verify a successful response.

    :param khoros_object: The Khoros object initialized via the :py:mod:`khoros.core` module
    :type khoros_object: class[khoros.Khoros]
    :param query_url: The full Khoros Community API v2 URL for the query
    :type query_url: str, None
    :param liql_query: The LiQL query to be performed, not yet embedded in the query URL
    :type liql_query: str, None
    :param return_json: Determines if the response should be returned in JSON format (``True`` by default)
    :type return_json: bool
    :param verify_success: Optionally check to confirm that the API query was successful (``False`` by default)
    :type verify_success: bool
    :param allow_exceptions: Defines whether or not exceptions can be raised for responses returning errors

                             .. caution:: This does not apply to exceptions for missing required data.

    :type allow_exceptions: bool
    :param verify: Determines whether or not to verify the server's TLS certificate (``True`` by default)
    :type verify: bool, None
    :param return_items: Reduces the JSON response to be only the list of items returned from the LiQL response
                         (``False`` by default)

                         .. note:: If an error response is returned then an empty list will be returned.

    :type return_items: bool
    :returns: The API response (in JSON format by default)
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    # Determine if TLS certificates should be verified during API calls
    verify = api.should_verify_tls(khoros_object) if verify is None else verify

    # Validate the LiQL query
    if not query_url and not liql_query:
        raise errors.exceptions.MissingRequiredDataError("An API query URL or a raw LiQL query must be provided.")
    if liql_query:
        query_url = get_query_url(khoros_object.core, liql_query)
    if 'header' not in khoros_object.auth:
        error_msg = "Cannot perform the query as an authorization header is not configured."
        raise errors.exceptions.MissingAuthDataError(error_msg)

    # Perform the API call and validate the data
    response = api.get_request_with_retries(query_url, return_json, auth_dict=khoros_object.auth, verify=verify)
    if verify_success:
        if not api.query_successful(response):
            error_msg = errors.handlers.get_error_from_json(response, include_error_bool=False)[2]
            if allow_exceptions:
                raise errors.exceptions.GETRequestError(error_msg)
            errors.handlers.eprint(error_msg)
    if return_json:
        # Convert the response to JSON as needed
        if not isinstance(response, dict):
            response = response.json()

        # Reduce teh scope to just the returned items when requested
        if return_items:
            if response.get('data') and response.get('data').get('items'):
                response = response.get('data').get('items')
            else:
                # Return an empty list as no items were found
                response = []
                # TODO: Log an entry stating that the LiQL query failed
    return response


def get_total_count(khoros_object, collection, where_filter="", verify_success=True):
    """This function retrieves the total asset count from a given collection (e.g. ``categories``).

    :param khoros_object: The Khoros object initialized via the :py:mod:`khoros.core` module
    :type khoros_object: class[khoros.Khoros]
    :param collection: The collection object to use in the FROM clause of the LiQL query (e.g. ``users``)
    :type collection: str
    :param where_filter: An optional filter to use as the WHERE clause in the LiQL query
    :type where_filter: str
    :param verify_success: Determines if the API query should be verified as successful (``True`` by default)
    :type verify_success: bool
    :returns: The total count as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    query_syntax = parse_query_elements('count(*)', collection, where_filter)
    response = perform_query(khoros_object, liql_query=query_syntax, verify_success=verify_success)
    return response['data']['count']


def get_returned_items(liql_response, only_first=False):
    """This function prunes a full LiQL API response down to only the returned item(s).

    .. versionchanged:: 3.3.2
       The error handling has been improved to avoid :py:exc:`IndexError` exceptions from being raised when no items
       were found in the LiQL response.

    .. versionadded:: 3.2.0

    :param liql_response: The full JSON response from the LiQL query as a dictionary
    :type liql_response: dict
    :param only_first: Returns only the first item found rather than a list of items (``False`` by default)
    :type only_first: bool
    :returns: A list of items (or a single item) found within the LiQL response
    :raises: :py:exc:`khoros.errors.exceptions.LiQLParseError`
    """
    if 'status' not in liql_response:
        raise errors.exceptions.LiQLParseError()
    elif liql_response.get('status') != 'success':
        raise errors.exceptions.LiQLParseError(message=liql_response.get('message'))
    liql_items = liql_response['data']['items']
    if only_first:
        fail_msg = "No items were found in the LiQL response and therefore a NoneType value will be returned."
        try:
            if len(liql_items) > 0:
                liql_items = liql_items[0]
            else:
                logger.error(fail_msg)
                liql_items = None
        except IndexError:
            logger.error(fail_msg)
            liql_items = None
    return liql_items


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
    select_fields = parse_select_fields(select_fields)

    # Establish the base syntax to return
    full_syntax = f"SELECT {select_fields} FROM {from_source}"

    # Append the WHERE clause to the syntax if provided
    if type(where_filter) != str:
        where_filter = parse_where_clause(where_filter)
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


def parse_select_fields(_select_fields):
    """This function parses the fields to be used in the SELECT statement of the LiQL query.

    .. versionchanged:: 3.5.0
       Refactored the function to leverage the :py:func:`isinstance` built-in function.

    .. versionchanged:: 3.4.0
       Renamed the function to adhere to PEP8 guidelines.

    :param _select_fields: The field(s) to be used in the SELECT statement
    :type _select_fields: str, tuple, list, set
    :returns: The properly formatted SELECT fields in string format (comma-separated)
    :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`
    """
    if not any((isinstance(_select_fields, list), isinstance(_select_fields, str), isinstance(_select_fields, tuple),
                isinstance(_select_fields, set))):
        raise errors.exceptions.InvalidFieldError("Fields must be in string or iterable format when explicitly defined")
    if any((isinstance(_select_fields, tuple), isinstance(_select_fields, list), isinstance(_select_fields, set))):
        _select_fields = convert_set(_select_fields)
        _select_fields = ",".join(_select_fields)
    elif isinstance(_select_fields, str):
        _select_fields = _select_fields.replace(';', ',').replace(', ', ',')
    return _select_fields


def structure_cursor_clause(cursor=None, liql_response=None):
    """This function structures the CURSOR clause for a LiQL query.

    .. versionchanged:: 4.0.0
       The cursor string has been wrapped in single quotes to prevent the
       :py:exc:`khoros.errors.exceptions.LiQLParseError` exception from being raised.

    .. versionadded:: 3.5.0

    :param cursor: A cursor value from the ``next_cursor`` key in a LiQL response
    :type cursor: str, None
    :param liql_response: A full LiQL query response in dictionary format
    :type liql_response: dict, None
    :returns: The properly formatted CURSOR clause for use in a new LiQL query
    :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not cursor and not liql_response:
        raise errors.exceptions.MissingRequiredDataError('Must provide cursor value or LiQL response')
    if cursor:
        if not isinstance(cursor, str):
            raise errors.exceptions.InvalidFieldError('Cursor value must be a string')
        if not cursor.lower().startswith('cursor'):
            cursor = f"CURSOR '{cursor}'"
    else:
        cursor = ''
        if liql_response.get('data') and liql_response['data'].get('next_cursor'):
            cursor = f"CURSOR {liql_response['data'].get('next_cursor')}"
    return cursor


def _wrap_string_values(_where_value):
    """This function wraps values going in the WHERE clause in single-quotes if they are not integers.

    .. versionchanged:: 3.4.0
       Renamed the function to adhere to PEP8 guidelines.

    :param _where_value: The value to be evaluated and potentially wrapped in single-quotes
    :returns: The value in int or string format
    """
    try:
        _where_value = int(_where_value)
    except (TypeError, ValueError):
        _where_value = f"'{_where_value}'"
    return _where_value


def _convert_where_dicts_to_lists(_dict_list):
    """This function converts dictionaries supplied as WHERE clause filters into properly formatted lists.

    .. versionchanged:: 3.4.0
       Renamed the function to adhere to PEP8 guidelines.

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


def parse_where_clause(where, join_logic='AND'):
    """This function parses the data supplied for the WHERE clause of a LiQL query.

    .. versionchanged:: 4.3.0
       Refactored the function to be more efficient and Pythonic, and added missing parenthesis on the
       exception classes.

    .. versionchanged:: 3.4.0
       Renamed the function to adhere to PEP8 guidelines and converted from a private to a public function.

    :param where: The WHERE clause information
    :type where: str, tuple, list, set, dict
    :param join_logic: The logic to use
    :type join_logic: str, tuple, list
    :returns: A properly formatted WHERE clause (excluding the WHERE statement at the beginning)
    :raises: :py:exc:`khoros.errors.exceptions.InvalidOperatorError`,
             :py:exc:`khoros.errors.exceptions.OperatorMismatchError`
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
    if not isinstance(where, list):
        if isinstance(where, dict):
            where = _convert_where_dicts_to_lists([where])
        if isinstance(where, tuple) or isinstance(where, set) and where:
            where = convert_set(where)
            if type(where[0]) not in LiQLSyntax.container_types:
                where = [where]

    # Determine the multi-clause logic to use
    # TODO: Figure out how to allow where clause grouping with logic
    if isinstance(join_logic, str):
        if join_logic not in LiQLSyntax.logic_operators:
            raise errors.exceptions.InvalidOperatorError()
        join_logic = [join_logic]
    elif len(join_logic) == 1:
        if join_logic[0] not in LiQLSyntax.logic_operators:
            raise errors.exceptions.InvalidOperatorError()
        else:
            join_logic = [join_logic[0]]
    else:
        if len(join_logic) != len(where) - 1:
            raise errors.exceptions.OperatorMismatchError()
        if not isinstance(join_logic, list):
            join_logic = list(join_logic)

    # Parse the where clause
    full_clause = ""
    num_clauses = len(where)
    while num_clauses > 0:
        for clause in where:
            # Adjust spacing between existing parsed clause and new clause section
            if len(full_clause) > 0:
                full_clause = f"{full_clause} "

            # Parse the individual clause
            if len(clause) == 2:
                full_clause = f"{full_clause}{clause[0]} = {_wrap_string_values(clause[-1])}"
            elif len(clause) == 3:
                if clause[1] not in LiQLSyntax.comparison_operators:
                    raise errors.exceptions.InvalidOperatorError()
                full_clause = f"{full_clause}{clause[0]} {clause[1]} {_wrap_string_values(clause[-1])}"
            elif type(clause) == str:
                full_clause = f"{full_clause}{clause}"

            # Add the logic statement to join multiple clauses as necessary
            if num_clauses > 1:
                multi_clause_logic = join_logic[0]
                join_logic.remove(join_logic[0])
                full_clause = f"{full_clause} {multi_clause_logic}"

            # Decrement the number of clauses
            num_clauses -= 1

    # Return the fully parsed WHERE clause
    return full_clause


class LiQLSyntax:
    """This class defines lists of syntax elements for use in LiQL queries."""
    comparison_operators = ['=', '!=', '>', '<', '>=', '<=']
    logic_operators = ['AND', 'OR', 'IN', 'MATCHES']
    order_operators = ['ASC', 'DESC']
    container_types = [tuple, set, dict, list]
