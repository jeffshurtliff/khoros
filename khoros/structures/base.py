# -*- coding: utf-8 -*-
"""
:Module:            khoros.structures.communities
:Synopsis:          This module contains functions relating to structures (i.e. categories, nodes and tenants)
:Usage:             ``from khoros.structures import base``
:Example:           ``details = base.get_details(khoros_object, 'category', 'category-id')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Mar 2021
"""

from .. import liql, errors
from ..utils import log_utils
from ..utils.core_utils import display_warning

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_details(khoros_object, identifier='', structure_type=None, first_item=None, community=False):
    """This function retrieves all details for a structure type via LiQL.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param identifier: The identifier (Category/Node ID or URL) by which to filter the results in the ``WHERE`` clause.
    :type identifier: str
    :param structure_type: Designates the structure as a ``category``, ``node`` or ``community``

                           .. note:: Optional if the ``identifier`` is a URL or the ``community`` Boolean is ``True``

    :param first_item: Filters the response data to the first item returned (``True`` by default)
    :type first_item: bool
    :param community: Alternate way of defining the structure type as a ``community`` (``False`` by default)
    :type community: bool
    :returns: The details for the structure type as a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if first_item is not False and (community is False and structure_type != 'community'):
        first_item = True
    if community or structure_type == 'community':
        liql_table = Mapping.structure_types_to_tables.get('community')
        first_item = False if first_item is not True else True
    elif structure_type not in Mapping.structure_types and '/' not in identifier:
        if structure_type:
            raise errors.exceptions.InvalidStructureTypeError(val=structure_type)
        else:
            raise errors.exceptions.MissingRequiredDataError(
                "A structure type (e.g. 'category' or 'node') must be supplied if a " +
                "full URL is not passed as an identifier.")
    elif '/' in identifier:
        if not structure_type:
            structure_type = get_structure_type_from_url(identifier, ignore_exceptions=True)
            if not structure_type:
                raise errors.exceptions.InvalidStructureTypeError("No structure type was provided and unable to " +
                                                                  "define a structure type using the provided URL.")
        liql_table = Mapping.structure_types_to_tables.get(structure_type)
    else:
        liql_table = Mapping.structure_types_to_tables.get(structure_type)
    is_href = True if ('/' in identifier and structure_type != 'node') else False
    where_filter = {True: 'view_href', False: 'id'}
    if '/' in identifier and structure_type == 'node':
        identifier = get_structure_id(identifier)
    try:
        # TODO: Update the query below to be less greedy or at least to provide the option to define fields
        query = f'SELECT * FROM {liql_table}'       # nosec
        if not community and structure_type != 'community':
            query = f'{query} WHERE {where_filter.get(is_href)} = "{identifier}"'
        response = liql.perform_query(khoros_object, liql_query=query, verify_success=True)
    except NameError:
        raise errors.exceptions.MissingRequiredDataError("The LiQL table was not defined")
    if first_item:
        response = response['data']['items'][0]
    return response


def structure_exists(khoros_object, structure_type, structure_id=None, structure_url=None):
    """This function checks to see if a structure (i.e. node, board, category or group hub) exists.

    .. versionadded:: 2.7.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param structure_type: The type of structure (e.g. ``board``, ``category``, ``node`` or ``grouphub``)
                           .. note:: The ``group hub`` value (as two words) is also acceptable.
    :type structure_type: str
    :param structure_id: The ID of the structure to check
    :type structure_id: str, None
    :param structure_url: The URL of the structure to check
    :type structure_url: str, None
    :returns: Boolean value indicating whether or not the structure already exists
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not any((structure_id, structure_url)):
        raise errors.exceptions.MissingRequiredDataError("Must provide at least one lookup value.")
    if structure_type not in Mapping.structure_types_to_tables.values():
        if structure_type not in Mapping.structure_types_to_tables.keys():
            raise errors.exceptions.InvalidStructureTypeError(val=structure_type)
        else:
            structure_type = Mapping.structure_types_to_tables.get(structure_type)
    if not structure_id:
        structure_id = get_structure_id(structure_url)
    count = liql.get_total_count(khoros_object, structure_type, f'id = "{structure_id}"')
    return True if count > 0 else False


def get_structure_id(url):
    """This function retrieves the Node ID from a full URL.

    .. versionchanged:: 2.6.0
       The function was renamed from ``_get_node_id`` to ``get_structure_id`` and converted from private to public.

    .. versionadded:: 2.1.0

    :param url: The full URL of the node
    :type url: str
    :returns: The ID in string format
    """
    node_id = ''
    for node_url_code in Mapping.node_url_identifiers:
        if node_url_code in url:
            node_id = url.split(node_url_code)[1]
            break
    if not node_id:
        raise errors.exceptions.InvalidURLError(f"Unable to identify the Node ID from the following URL: {url}")
    return node_id


def _check_url_for_identifier(_url, _id_type, _ignore_exceptions=False):
    """This function checks a URL to see if it has a particular identifier associated with a category or node.

    .. versionadded:: 2.1.0

    :param _url: The URL to be evaluated
    :type _url: str
    :param _id_type: The type of identifier (e.g. ``category``, ``node``)
    :type _id_type: str
    :param _ignore_exceptions: Determines if exceptions should not be raised
    :type _ignore_exceptions: bool
    :returns: Boolean value indicating if a match was found
    :raises: :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`
    """
    if _id_type not in Mapping.structure_types and not _ignore_exceptions:
        raise errors.exceptions.InvalidStructureTypeError(val=_id_type)
    _match_found = False
    _id_lists = {
        'category': Mapping.category_url_identifiers,
        'node': Mapping.node_url_identifiers
    }
    for _identifier in _id_lists.get(_id_type):
        if _identifier in _url:
            _match_found = True
            break
    return _match_found


def limit_to_first_child(structure_data):
    """This function limits structure data to be only for the first child.

    .. versionadded:: 2.1.0

    :param structure_data: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type structure_data: dict
    :returns: The data dictionary that has been restricted to the first child
    :raises: :py:exc:`TypeError`, :py:exc:`KeyError`
    """
    return structure_data['data']['items'][0]


def get_structure_field(khoros_object, field, identifier='', details=None,
                        structure_type=None, first_item=True, community=False):
    """This function returns a specific API field value for a community, category or node collection.

    .. versionadded:: 2.1.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param field: The field from the :py:class:`khoros.structures.base.Mapping` class whose value should be returned
    :type field: str
    :param identifier: The identifier (Category/Node ID or URL) by which to filter the results in the ``WHERE`` clause.
    :type identifier: str
    :type details: The data captured from the :py:func:`khoros.structures.base.get_details` function
    :type details: dict, None
    :param structure_type: Designates the structure as a ``category``, ``node`` or ``community``

                           .. note:: Optional if the ``identifier`` is a URL or the ``community`` Boolean is ``True``

    :type structure_type: str, None
    :param first_item: Filters the response data to the first item returned (``True`` by default)
    :type first_item: bool
    :param community: Alternate way of defining the structure type as a ``community`` (``False`` by default)
    :type community: bool
    :returns: The API field value in its appropriate format
    :raises: :py:exc:`khoros.errors.exceptions.InvalidFieldError`,
             :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not details:
        details = get_details(khoros_object, identifier, structure_type, first_item, community)
    structure_type = verify_structure_type(identifier, structure_type, community)
    field_dicts = {
        'category': Mapping.category_fields,
        'community': Mapping.community_fields,
        'node': Mapping.node_fields
    }
    data_fields = field_dicts.get(structure_type)
    if field not in data_fields:
        raise errors.exceptions.InvalidFieldError(val=field)
    api_field = data_fields.get(field)
    if len(api_field) == 1:
        return_field = details[api_field[0]]
    elif len(api_field) == 2:
        return_field = details[api_field[0]][api_field[1]]
    else:
        return_field = details[api_field[0]][api_field[1]][api_field[2]]
    return return_field


def is_category_url(url, ignore_exceptions=False):
    """This function identifies if a provided URL is for a category in the environment.

    .. versionadded:: 2.1.0

    :param url: The URL to be evaluated
    :type url: str
    :param ignore_exceptions: Determines if exceptions should not be raised
    :type ignore_exceptions: bool
    :returns: Boolean value indicating if the URL is associated with a category
    :raises: :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`
    """
    return _check_url_for_identifier(url, 'category', ignore_exceptions)


def is_node_url(url, ignore_exceptions=False):
    """This function identifies if a provided URL is for a node in the environment.

    .. versionadded:: 2.1.0

    :param url: The URL to be evaluated
    :type url: str
    :param ignore_exceptions: Determines if exceptions should not be raised
    :type ignore_exceptions: bool
    :returns: Boolean value indicating if the URL is associated with a node
    :raises: :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`
    """
    return _check_url_for_identifier(url, 'node', ignore_exceptions)


def verify_structure_type(identifier, structure_type, community=False):
    """This function verifies the structure type by examining the identifier(s) and provided structure type value.

    .. versionadded:: 2.1.0

    :param identifier: The identifier (Category/Node ID or URL) by which to filter the results in the parent function
    :type identifier: str
    :param structure_type: Designates the structure as a ``category``, ``node`` or ``community``

                           .. note:: Optional if the ``identifier`` is a URL or the ``community`` Boolean is ``True``

    :type structure_type: str
    :param community: Alternate way of defining the structure type as a ``community`` (``False`` by default)
    :type community: bool
    :returns: The appropriately labeled and verified structure type
    :raises: :py:exc:`khoros.errors.exceptions.InvalidStructureTypeError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    accepted_structure_types = ['category', 'community', 'node']
    if community:
        structure_type = 'community'
    if structure_type:
        if structure_type in accepted_structure_types:
            return structure_type
        elif structure_type not in accepted_structure_types and '/' not in identifier:
            raise errors.exceptions.InvalidStructureTypeError(val=structure_type)
        else:
            display_warning(f"The structure type '{structure_type}' is invalid. Will attempt to identify via URL.")
    structure_type = get_structure_type_from_url(identifier, ignore_exceptions=True)
    if not structure_type:
        raise errors.exceptions.MissingRequiredDataError(
            "A structure type (e.g. 'category' or 'node') must be supplied if a " +
            "full URL is not passed as an identifier.")
    return structure_type


def get_structure_type_from_url(url, ignore_exceptions=False):
    """This function determines if a URL is for a category or node (or neither).

    .. versionadded:: 2.1.0

    :param url: The URL to be evaluated
    :type url: str
    :param ignore_exceptions: Determines if exceptions should not be raised
    :type ignore_exceptions: bool
    :returns: A string with ``category`` or ``node``, or a blank string if neither

    """
    structure_type = ''
    if is_category_url(url, ignore_exceptions):
        structure_type = 'category'
    elif is_node_url(url, ignore_exceptions):
        structure_type = 'node'
    return structure_type


class Mapping:
    """This class contains lists and dictionaries used to map structure data."""
    category_url_identifiers = ['ct-p/']
    node_url_identifiers = ['bg-p/', 'con-p/', 'bd-p/', 'gp-p/', 'idb-p/', 'qa-p/', 'tkb-p/', 'gh-p/', 'ct-p/']
    structure_types = ['category', 'node']
    structure_types_to_tables = {
        'board': 'boards',
        'category': 'categories',
        'community': 'communities',
        'group hub': 'grouphubs',
        'grouphub': 'grouphubs',
        'node': 'nodes'
    }
    category_fields = {
        'type': ('type',),
        'id': ('id',),
        'href': ('href',),
        'view_href': ('view_href',),
        'full_title': ('title',),
        'short_title': ('short_title',),
        'description': ('description',),
        'parent_details': ('parent_category',),
        'parent_type': ('parent_category', 'type'),
        'parent_id': ('parent_category', 'id'),
        'parent_href': ('parent_category', 'href'),
        'parent_view_href': ('parent_category', 'view_href'),
        'root_details': ('root_category',),
        'root_type': ('root_category', 'type'),
        'root_id': ('root_category', 'id'),
        'root_href': ('root_category', 'href'),
        'root_view_href': ('root_category', 'view_href'),
        'ancestors_query': ('ancestor_categories', 'query'),
        'descendants_query': ('descendant_categories', 'query'),
        'children_query': ('child_categories', 'query'),
        'boards_query': ('boards', 'query'),
        'language': ('language',),
        'hidden': ('hidden',),
        'messages_query': ('messages', 'query'),
        'topics_query': ('topics', 'query'),
        'views': ('views',),
        'date_pattern': ('date_pattern',),
        'friendly_date_enabled': ('friendly_date_enabled',),
        'friendly_date_max_age': ('friendly_date_max_age',),
        'skin': ('skin',),
        'depth': ('depth',),
        'position': ('position',),
        'user_context_details': ('user_context',),
        'user_context_type': ('user_context', 'type'),
        'user_context_sort_order': ('user_context', 'sort_order'),
        'user_context_sort_field': ('user_context', 'sort_field'),
        'creation_date': ('creation_date',),
    }
    community_fields = {
        'type': ('type',),
        'id': ('id',),
        'full_title': ('title',),
        'short_title': ('short_title',),
        'description': ('description',),
        'href': ('href',),
        'view_href': ('view_href',),
        'user_context_details': ('user_context',),
        'user_context_type': ('user_context', 'type'),
        'user_context_sort_order': ('user_context', 'sort_order'),
        'user_context_sort_field': ('user_context', 'sort_field'),
        'attachment_max_per_message': ('attachment_max_per_message',),
        'attachment_file_types': ('attachment_file_types',),
        'email_confirmation_required_to_post': ('email_confirmation_required_to_post',),
        'language': ('language',),
        'ooyala_player_branding_id': ('ooyala_player_branding_id',),
        'date_pattern': ('date_pattern',),
        'friendly_date_enabled': ('friendly_date_enabled',),
        'friendly_date_max_age': ('friendly_date_max_age',),
        'skin': ('skin',),
        'web_ui_details': ('web_ui',),
        'web_ui_type': ('web_ui', 'type'),
        'web_ui_sign_out_url': ('web_ui', 'sign_out_url'),
        'web_ui_redirect_param': ('web_ui', 'redirect_param'),
        'web_ui_redirect_reason_param': ('web_ui', 'redirect_reason_param'),
        'top_level_categories_enabled': ('top_level_categories_enabled',),
        'tlc_show_community_node_in_breadcrumb': ('tlc_show_community_node_in_breadcrumb',),
        'tlc_show_breadcrumb_at_top_level': ('tlc_show_breadcrumb_at_top_level',),
        'tlc_set_on_community_page': ('tlc_set_on_community_page',),
        'creation_date': ('creation_date',)
    }
    node_fields = {
        'type': ('type',),
        'id': ('id',),
        'href': ('href',),
        'node_type': ('node_type',),
        'discussion_style': ('conversation_style',),
        'full_title': ('title',),
        'short_title': ('short_title',),
        'description': ('description',),
        'parent_details': ('parent',),
        'parent_type': ('parent', 'type'),
        'parent_id': ('parent', 'id'),
        'parent_href': ('parent', 'href'),
        'root_details': ('root_category',),
        'root_type': ('root_category', 'type'),
        'root_id': ('root_category', 'id'),
        'root_href': ('root_category', 'href'),
        'ancestors_query': ('ancestors', 'query'),
        'avatar_details': ('avatar',),
        'avatar_type': ('avatar', 'type'),
        'avatar_tiny_href': ('avatar', 'tiny_href'),
        'avatar_small_href': ('avatar', 'small_href'),
        'avatar_medium_href': ('avatar', 'medium_href'),
        'avatar_large_href': ('avatar', 'large_href'),
        'creation_date': ('creation_date',),
        'creation_date_friendly': ('creation_date_friendly',),
        'children_query': ('children', 'query'),
        'depth': ('depth',),
        'position': ('position',),
        'hidden': ('hidden',),
        'user_context_details': ('user_context',),
        'user_context_type': ('user_context', 'type'),
        'user_context_sort_order': ('user_context', 'sort_order'),
        'user_context_sort_field': ('user_context', 'sort_field'),
        'messages_query': ('messages', 'query'),
        'topics_query': ('topics', 'query'),
        'views': ('views',)
    }
