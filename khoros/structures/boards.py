# -*- coding: utf-8 -*-
"""
:Module:            khoros.structures.boards
:Synopsis:          This module contains functions specific to boards within the Khoros Community platform
:Usage:             ``from khoros.structures import boards``
:Example:           ``board_url = boards.create(khoros_object, 'my-board', 'My Board', 'forum', return_url=True)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

import warnings

from .. import api, errors
from ..objects import users
from ..utils import log_utils
from . import base

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)

VALID_DISCUSSION_STYLES = ['blog', 'contest', 'forum', 'idea', 'qanda', 'tkb']


def create(khoros_object, board_id, board_title, discussion_style, description=None, parent_category_id=None,
           hidden=None, allowed_labels=None, use_freeform_labels=None, use_predefined_labels=None,
           predefined_labels=None, media_type=None, blog_authors=None, blog_author_ids=None, blog_author_logins=None,
           blog_comments_enabled=None, blog_moderators=None, blog_moderator_ids=None, blog_moderator_logins=None,
           one_entry_per_contest=None, one_kudo_per_contest=None, posting_date_end=None, posting_date_start=None,
           voting_date_end=None, voting_date_start=None, winner_announced_date=None, full_response=None, return_id=None,
           return_url=None, return_api_url=None, return_http_code=None, return_status=None, return_error_messages=None,
           split_errors=False):
    """This function creates a new board within a Khoros Community environment.

    .. versionchanged:: 2.5.2
       Changed the functionality around the ``return_error_messages`` argument and added the ``split_errors`` argument.

    .. versionadded:: 2.5.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param board_id: The unique identifier (i.e. ``id`` field) for the new board **(Required)**
    :type board_id: str
    :param board_title: The title of the new board **(Required)**
    :type board_title: str
    :param discussion_style: Defines the board as a ``blog``, ``contest``, ``forum``, ``idea``, ``qanda`` or ``tkb``
                             **(Required)**
    :type discussion_style: str
    :param description: A brief description of the board
    :type description: str, None
    :param parent_category_id: The ID of the parent category (if applicable)
    :type parent_category_id: str, None
    :param hidden: Defines whether or not the new board should be hidden from lists and menus (disabled by default)
    :type hidden: bool, None
    :param allowed_labels: The type of labels allowed on the board (``freeform-only``, ``predefined-only`` or
                           ``freeform and pre-defined``)
    :type allowed_labels: str, None
    :param use_freeform_labels: Determines if freeform labels should be utilized
    :type use_freeform_labels: bool, None
    :param use_predefined_labels: Determines if pre-defined labels should be utilized
    :type use_predefined_labels: bool, None
    :param predefined_labels: The pre-defined labels to utilized on the board as a list of dictionaries

                              .. todo:: The ability to provide labels as a simple list and optionally standardize
                                        their format (e.g. Pascal Case, etc.) will be available in a future release.

    :type predefined_labels: list, None
    :param media_type: The media type associated with a contest. (``image``, ``video`` or ``story`` meaning text)
    :type media_type: str, None
    :param blog_authors: The approved blog authors in a blog board as a list of user data dictionaries
    :type blog_authors: list, None
    :param blog_author_ids: A list of User IDs representing the approved blog authors in a blog board
    :type blog_author_ids: list, None
    :param blog_author_logins: A list of User Logins (i.e. usernames) representing approved blog authors in a blog board
    :type blog_author_logins: list, None
    :param blog_comments_enabled: Determines if comments should be enabled on blog posts within a blog board
    :type blog_comments_enabled: bool, None
    :param blog_moderators: The designated blog moderators in a blog board as a list of user data dictionaries
    :type blog_moderators: list, None
    :param blog_moderator_ids: A list of User IDs representing the blog moderators in a blog board
    :type blog_moderator_ids: list, None
    :param blog_moderator_logins: A list of User Logins (i.e. usernames) representing blog moderators in a blog board
    :type blog_moderator_logins: list, None
    :param one_entry_per_contest: Defines whether a user can submit only one entry to a single contest
    :type one_entry_per_contest: bool, None
    :param one_kudo_per_contest: Defines whether a user can vote only once per contest
    :type one_kudo_per_contest: bool, None
    :param posting_date_end: The date/time when the contest is closed to submissions
    :type posting_date_end: type[datetime.datetime], None
    :param posting_date_start: The date/time when the voting period for a contest begins
    :type posting_date_start: type[datetime.datetime], None
    :param voting_date_end: The date/time when the voting period for a contest ends
    :type voting_date_end: type[datetime.datetime], None
    :param voting_date_start: The date/time when the voting period for a contest begins
    :type voting_date_start: type[datetime.datetime], None
    :param winner_announced_date: The date/time the contest winner will be announced
    :type winner_announced_date: type[datetime.datetime], None
    :param full_response: Determines whether the full, raw API response should be returned by the function

                          .. caution:: This argument overwrites the ``return_id``, ``return_url``, ``return_api_url``,
                                       ``return_http_code``, ``return_status`` and ``return_error_messages`` arguments.

    :type full_response: bool, None
    :param return_id: Determines if the **ID** of the new board should be returned by the function
    :type return_id: bool, None
    :param return_url: Determines if the **URL** of the new board should be returned by the function
    :type return_url: bool, None
    :param return_api_url: Determines if the **API URL** of the new board should be returned by the function
    :type return_api_url: bool, None
    :param return_http_code: Determines if the **HTTP Code** of the API response should be returned by the function
    :type return_http_code: bool, None
    :param return_status: Determines if the **Status** of the API response should be returned by the function
    :type return_status: bool, None
    :param return_error_messages: Determines if the **Developer Response Message** (if any) associated with the
           API response should be returned by the function
    :type return_error_messages: bool, None
    :param split_errors: Defines whether or not error messages should be merged when applicable
    :type split_errors: bool
    :returns: Boolean value indicating a successful outcome (default), the full API response or one or more specific
              fields defined by function arguments
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`,
             :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`
    """
    payload = structure_payload(khoros_object, board_id, board_title, discussion_style, description, parent_category_id,
                                hidden, allowed_labels, use_freeform_labels, use_predefined_labels, predefined_labels,
                                media_type, blog_authors, blog_author_ids, blog_author_logins, blog_comments_enabled,
                                blog_moderators, blog_moderator_ids, blog_moderator_logins, one_entry_per_contest,
                                one_kudo_per_contest, posting_date_end, posting_date_start, voting_date_end,
                                voting_date_start, winner_announced_date)
    # TODO: Add a new api.make_v2_request() function that just takes an endpoint rather than the full URL
    api_url = f"{khoros_object.core['v2_base']}/boards"
    headers = {'content-type': 'application/json'}
    response = api.post_request_with_retries(api_url, payload, khoros_object=khoros_object, headers=headers)
    return api.deliver_v2_results(response, full_response, return_id, return_url, return_api_url, return_http_code,
                                  return_status, return_error_messages, split_errors)


def structure_payload(khoros_object, board_id, board_title, discussion_style, description=None, parent_category_id=None,
                      hidden=None, allowed_labels=None, use_freeform_labels=None, use_predefined_labels=None,
                      predefined_labels=None, media_type=None, blog_authors=None, blog_author_ids=None,
                      blog_author_logins=None, blog_comments_enabled=None, blog_moderators=None,
                      blog_moderator_ids=None, blog_moderator_logins=None, one_entry_per_contest=None,
                      one_kudo_per_contest=None, posting_date_end=None, posting_date_start=None, voting_date_end=None,
                      voting_date_start=None, winner_announced_date=None):
    """This function structures the payload to use in a Community API v2 request involving a board.

    .. versionadded:: 2.5.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param board_id: The unique identifier (i.e. ``id`` field) for the new board **(Required)**
    :type board_id: str
    :param board_title: The title of the new board **(Required)**
    :type board_title: str
    :param discussion_style: Defines the board as a ``blog``, ``contest``, ``forum``, ``idea``, ``qanda`` or ``tkb``
                             **(Required)**
    :type discussion_style: str
    :param description: A brief description of the board
    :type description: str, None
    :param parent_category_id: The ID of the parent category (if applicable)
    :type parent_category_id: str, None
    :param hidden: Defines whether or not the new board should be hidden from lists and menus (disabled by default)
    :type hidden: bool, None
    :param allowed_labels: The type of labels allowed on the board (``freeform-only``, ``predefined-only`` or
                           ``freeform and pre-defined``)
    :type allowed_labels: str, None
    :param use_freeform_labels: Determines if freeform labels should be utilized
    :type use_freeform_labels: bool, None
    :param use_predefined_labels: Determines if pre-defined labels should be utilized
    :type use_predefined_labels: bool, None
    :param predefined_labels: The pre-defined labels to utilized on the board as a list of dictionaries

                              .. todo:: The ability to provide labels as a simple list and optionally standardize
                                        their format (e.g. Pascal Case, etc.) will be available in a future release.

    :type predefined_labels: list, None
    :param media_type: The media type associated with a contest. (``image``, ``video`` or ``story`` meaning text)
    :type media_type: str, None
    :param blog_authors: The approved blog authors in a blog board as a list of user data dictionaries
    :type blog_authors: list, None
    :param blog_author_ids: A list of User IDs representing the approved blog authors in a blog board
    :type blog_author_ids: list, None
    :param blog_author_logins: A list of User Logins (i.e. usernames) representing approved blog authors in a blog board
    :type blog_author_logins: list, None
    :param blog_comments_enabled: Determines if comments should be enabled on blog posts within a blog board
    :type blog_comments_enabled: bool, None
    :param blog_moderators: The designated blog moderators in a blog board as a list of user data dictionaries
    :type blog_moderators: list, None
    :param blog_moderator_ids: A list of User IDs representing the blog moderators in a blog board
    :type blog_moderator_ids: list, None
    :param blog_moderator_logins: A list of User Logins (i.e. usernames) representing blog moderators in a blog board
    :type blog_moderator_logins: list, None
    :param one_entry_per_contest: Defines whether a user can submit only one entry to a single contest
    :type one_entry_per_contest: bool, None
    :param one_kudo_per_contest: Defines whether a user can vote only once per contest
    :type one_kudo_per_contest: bool, None
    :param posting_date_end: The date/time when the contest is closed to submissions
    :type posting_date_end: type[datetime.datetime], None
    :param posting_date_start: The date/time when the voting period for a contest begins
    :type posting_date_start: type[datetime.datetime], None
    :param voting_date_end: The date/time when the voting period for a contest ends
    :type voting_date_end: type[datetime.datetime], None
    :param voting_date_start: The date/time when the voting period for a contest begins
    :type voting_date_start: type[datetime.datetime], None
    :param winner_announced_date: The date/time the contest winner will be announced
    :type winner_announced_date: type[datetime.datetime], None
    :returns: The full and properly formatted payload for the API request
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    # Define the minimum payload framework
    payload = {
        "data": {
            "type": "board"
        }
    }

    # Populate relevant sections of the payload
    required_error_msg = "The 'board_id', 'board_title' and 'discussion_style' fields are required to create a board."
    payload = _structure_id_and_title(board_id, board_title, payload, required_error_msg)
    payload = _structure_discussion_style(discussion_style, payload, required_error_msg)
    payload = _structure_parent_category(parent_category_id, payload)

    # Populate the remaining simple fields
    simple_fields = {
        'description': description,
        'hidden': hidden,
        'media_type': media_type,
    }
    payload = _structure_simple_fields(simple_fields, payload)

    # Populate the label settings
    label_settings = {
        'allowed_labels': allowed_labels,
        'use_freeform_labels': use_freeform_labels,
        'use_predefined_labels': use_predefined_labels,
        'predefined_labels': predefined_labels,
    }
    payload = _structure_label_settings(label_settings, payload)

    # Populate the blog-related settings
    blog_settings = {
        'authors': blog_authors,
        'author_ids': blog_author_ids,
        'author_logins': blog_author_logins,
        'comments_enabled': blog_comments_enabled,
        'moderators': blog_moderators,
        'moderator_ids': blog_moderator_ids,
        'moderator_logins': blog_moderator_logins,
    }
    payload = _structure_blog_settings(khoros_object, blog_settings, payload, discussion_style)

    # Populate the contest-related settings
    contest_settings = {
        'one_entry_per_contest': one_entry_per_contest,
        'one_kudo_per_contest': one_kudo_per_contest,
        'posting_date_end': posting_date_end,
        'posting_date_start': posting_date_start,
        'voting_date_end': voting_date_end,
        'voting_date_start': voting_date_start,
        'winner_announced_date': winner_announced_date,
    }
    payload = _structure_contest_settings(contest_settings, payload, discussion_style)
    return payload


def _structure_id_and_title(_board_id, _board_title, _payload, _missing_error):
    """This function structures the portion of the payload for the Board ID and Board Title.

    .. versionadded:: 2.5.0

    :param _board_id: The unique identifier (i.e. ``id`` field) for the new board **(Required)**
    :type _board_id: str
    :param _board_title: The title of the new board **(Required)**
    :type _board_title: str
    :param _payload: The partially constructed payload for the API request
    :type _payload: dict
    :param _missing_error: The error message to use when raising the
                           :py:exc:`khoros.errors.exceptions.MissingRequiredDataError` exception class when the
                           Board ID and/or Board Title have not been provided.
    :returns: The API request payload with appended entries for ``id`` and ``title``
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not _board_id or not _board_title:
        raise errors.exceptions.MissingRequiredDataError(_missing_error)
    _payload['data']['id'] = _board_id
    _payload['data']['title'] = _board_title
    return _payload


def _structure_discussion_style(_discussion_style, _payload, _missing_error):
    """This function structures the portion of the payload for the Discussion Style. (i.e. board type)

    .. versionadded:: 2.5.0

    :param _discussion_style: Defines the board as a ``blog``, ``contest``, ``forum``, ``idea``, ``qanda`` or ``tkb``
                              **(Required)**
    :type _discussion_style: str
    :param _payload: The partially constructed payload for the API request
    :type _payload: dict
    :param _missing_error: The error message to use when raising the
                           :py:exc:`khoros.errors.exceptions.MissingRequiredDataError` exception class when the
                           Discussion Style have not been provided.
    :returns: The API request payload with appended entries for ``conversation_style``
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`,
             :py:exc:`khoros.errors.exceptions.InvalidNodeTypeError`
    """
    if not _discussion_style:
        raise errors.exceptions.MissingRequiredDataError(_missing_error)
    if _discussion_style not in VALID_DISCUSSION_STYLES:
        raise errors.exceptions.InvalidNodeTypeError(f"'{_discussion_style}' is not a valid discussion style.")
    _payload['data']['conversation_style'] = _discussion_style
    return _payload


def _structure_parent_category(_parent_id, _payload):
    """This function structures the portion of the payload for the parent category.

    .. versionadded:: 2.5.0

    :param _parent_id: The ID of the parent category (if applicable)
    :type _parent_id: str, None
    :param _payload: The partially constructed payload for the API request
    :type _payload: dict
    :returns: The API request payload with appended entries for ``parent_category``
    """
    if _parent_id:
        _payload['data']['parent_category'] = {
            'id': _parent_id
        }
    return _payload


def _structure_simple_fields(_simple_fields, _payload):
    """This function structures the portion of the payload for the simple string and Boolean fields.

    .. versionadded:: 2.5.0

    :param _simple_fields: A dictionary containing the simple string and Boolean fields for the API payload
    :type _simple_fields: dict
    :param _payload: The partially constructed payload for the API request
    :type _payload: dict
    :returns: The API request payload with appended entries for the simple string and Boolean fields
    """
    for _field, _value in _simple_fields.items():
        if _value:
            _payload['data'][_field] = _value
    return _payload


def _structure_label_settings(_label_settings, _payload):
    """This function structures the portion of the payload for the setting fields relating to labels.

    .. versionadded:: 2.5.0

    :param _label_settings: A dictionary containing the settings involving labels
    :type _label_settings: dict
    :param _payload: The partially constructed payload for the API request
    :type _payload: dict
    :returns: The API request payload with appended entries for the field settings relating to labels
    """
    # Verify that any string passed in 'allowed_labels' is valid when applicable
    _valid_allowed_labels = ['freeform-only', 'predefined-only', 'freeform and pre-defined']
    if _label_settings.get('allowed_labels'):
        if _label_settings.get('allowed_labels') in _valid_allowed_labels:
            _payload['data']['allowed_labels'] = _label_settings.get('allowed_labels')
        else:
            # TODO: Leverage the logger instead of warnings
            warn_msg = f"The string '{_label_settings.get('allowed_labels')}' for the 'allowed_labels' field is " \
                       f"not valid and will be ignored."
            warnings.warn(warn_msg, UserWarning)
            _label_settings['allowed_labels'] = None

    # Inform the user that the value will be overwritten by any defined Boolean label settings values
    if _label_settings.get('allowed_labels') and (
            _label_settings.get('allowed_labels') is not None or
            _label_settings.get('allowed_labels') is not None):
        # TODO: Leverage the logger instead of warnings
        warn_msg = f"The defined 'allowed_labels' field will be overwritten when the 'use_freeform_labels' and/or " \
                   f"'use_predefined_labels' Boolean values are also configured."
        warnings.warn(warn_msg, UserWarning)

    # Define the 'allowed_labels' value based on the defined Boolean values when applicable
    _boolean_values = (_label_settings.get('use_freeform_labels'), _label_settings.get('use_predefined_labels'))
    if any(_boolean_values):
        if all(_boolean_values):
            _payload['data']['allowed_labels'] = 'freeform and pre-defined'
        elif _label_settings.get('use_freeform_labels'):
            _payload['data']['allowed_labels'] = 'freeform-only'
        elif _label_settings.get('use_predefined_labels'):
            _payload['data']['allowed_labels'] = 'predefined-only'

    # Add the predefined labels if present
    # TODO: Check to ensure that they are in the proper format (In Studio they are a comma-separated list)
    # TODO: Provide the option to format the labels into all lowercase or Pascal Case
    # TODO: Set up unit test to see what happens if 'use_predefined_labels' is True but no labels are predefined
    if _label_settings.get('predefined_labels'):
        _payload['data']['predefined_labels'] = _label_settings.get('predefined_labels')
    return _payload


def _structure_blog_settings(_khoros_object, _blog_settings, _payload, _discussion_style):
    """This function structures the portion of the payload for the setting fields relating to blogs.

    .. versionadded:: 2.5.0

    :param _khoros_object:
    :param _blog_settings: A dictionary containing the settings involving labels
    :type _blog_settings: dict
    :param _payload: The partially constructed payload for the API request
    :type _payload: dict
    :param _discussion_style: The discussion style for the new board to ensure that these settings apply
    :type _discussion_style: str
    :returns: The API request payload with appended entries for the field settings relating to labels
    """
    if any(_blog_settings.values()) and _discussion_style != 'blog':
        _warn_about_ignored_settings('blog', _discussion_style)
    else:
        # Populate the 'comments_enabled' setting if applicable
        if _blog_settings.get('comments_enabled'):
            _payload['data']['comments_enabled'] = _blog_settings.get('comments_enabled')

        # Populate the blog authors list
        if any((_blog_settings['authors'], _blog_settings['author_ids'], _blog_settings['author_logins'])):
            authors = users.structure_user_dict_list(_khoros_object, _blog_settings['authors'],
                                                     _blog_settings['author_ids'], _blog_settings['author_logins'])
            _payload['data']['authors'] = authors

        # Populate the blog moderators list
        if any((_blog_settings['moderators'], _blog_settings['moderator_ids'], _blog_settings['moderator_logins'])):
            moderators = users.structure_user_dict_list(_khoros_object, _blog_settings['moderators'],
                                                        _blog_settings['moderator_ids'],
                                                        _blog_settings['moderator_logins'])
            _payload['data']['moderators'] = moderators
    return _payload


def _structure_contest_settings(_contest_settings, _payload, _discussion_style):
    """This function structures the portion of the payload for the setting fields relating to contests.

    .. versionadded:: 2.5.0

    :param _contest_settings: A dictionary containing the settings involving contests
    :type _contest_settings: dict
    :param _payload: The partially constructed payload for the API request
    :type _payload: dict
    :param _discussion_style: The discussion style for the new board to ensure that these settings apply
    :type _discussion_style: str
    :returns: The API request payload with appended entries for the field settings relating to contests
    """
    if any(_contest_settings.values()) and _discussion_style != 'contest':
        _warn_about_ignored_settings('contest', _discussion_style)
    else:
        for _field, _value in _contest_settings.items():
            if _value:
                # TODO: Verify proper format for datetime values
                _payload['data'][_field] = _value
    return _payload


def _warn_about_ignored_settings(_settings_type, _discussion_style):
    """This function displays a ``UserWarning`` that provided fields will be ignored if the discussion style does not
       match the style for which the field are specific.

    .. versionadded:: 2.5.0

    :param _settings_type: The discussion style relating to the supplied fields and values
    :type _settings_type: str
    :param _discussion_style: The discussion style of the new board
    :type _discussion_style: str
    :returns: None
    """
    # TODO: Leverage the logger instead of warnings
    warn_msg = f"Because the discussion style is '{_discussion_style}' all {_settings_type}-specific fields " \
               "provided will be ignored."
    warnings.warn(warn_msg, UserWarning)
    return


def get_board_id(url):
    """This function retrieves the Board ID for a given board when provided its URL.

    .. versionadded:: 2.6.0

    :param url: The URL from which to parse out the Board ID
    :type url: str
    :returns: The Board ID retrieved from the URL
    :raises: :py:exc:`khoros.errors.exceptions.InvalidURLError`
    """
    return base.get_structure_id(url)


def board_exists(khoros_object, board_id=None, board_url=None):
    """This function checks to see if a board (i.e. blog, contest, forum, idea exchange, Q&A or TKB) exists.

    .. versionadded:: 2.7.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param board_id: The ID of the board to check
    :type board_id: str, None
    :param board_url: The URL of the board to check
    :type board_url: str, None
    :returns: Boolean value indicating whether or not the board already exists
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    return base.structure_exists(khoros_object, 'board', board_id, board_url)
