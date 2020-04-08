# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.users
:Synopsis:          This module includes functions that handle user-related operations.
:Usage:             ``from khoros.objects import users``
:Example:           ``users.create(khoros_object, username='john_doe', email='john.doe@example.com')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     08 Apr 2020
"""

import warnings

from .. import api, liql, errors


def create(khoros_object, user_settings=None, login=None, email=None, password=None, first_name=None, last_name=None,
           biography=None, sso_id=None, web_page_url=None, cover_image=None):
    """This function creates a new user in the Khoros Community environment.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: Allows all user settings to be passed to the function within a single dictionary
    :type user_settings: dict, NoneType
    :param login: The username (i.e. ``login``) for the user (**required**)
    :type login: str, NoneType
    :param email: The email address for the user (**required**)
    :type email: str, NoneType
    :param password: The password for the user
    :type password: str, NoneType
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, NoneType
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, NoneType
    :param biography: The user's biography for their profile
    :type biography: str, NoneType
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, NoneType
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, NoneType
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, NoneType
    :returns: None
    :raises: :py:exc:`khoros.errors.exceptions.UserCreationError`
    """
    # TODO: Add functionality for followers, following, rank, roles, user_avatar and user_badges
    payload = structure_payload(user_settings, login, email, password, first_name, last_name, biography, sso_id,
                                web_page_url, cover_image)
    query_url = f"{khoros_object._settings['v2_base']}/users"
    headers = {'Content-Type': 'application/json'}
    response = api.post_request_with_retries(query_url, payload, auth_dict=khoros_object.auth, headers=headers)
    if not api.query_successful(response):
        raise errors.exceptions.UserCreationError(user=payload['login'], exc_msg=response['message'])
    return


def process_user_settings(user_settings=None, user_id=None, albums=None, avatar=None, banned=None, biography=None,
                          bonus_points=None, cover_image=None, deleted=None, email=None, email_excluded=None,
                          first_name=None, followers=None, following=None, href=None, images=None, kudos_given=None,
                          kudos_received=None, kudos_weight=None, language=None, last_name=None, last_visit_time=None,
                          location=None, login=None, messages=None, metrics=None, online_status=None, password=None,
                          personal_data=None, public_images=None, rank=None, registration_data=None, reviews=None,
                          roles=None, signature_topics=None, solutions_authored=None, sso_id=None,
                          threads_participated=None, topics=None, user_badges=None, videos=None, view_href=None,
                          web_page_url=None):
    """This function processes the ``user_settings`` for functions and formats them into a normalized dictionary.

    :param user_settings: Allows all user settings to be passed to the function within a single dictionary
    :type user_settings: dict, NoneType
    :param user_id: The unique User ID associated with the user
    :type user_id: int, str, NoneType
    :param albums: The image albums associated with the user's profile
    :type albums: dict, NoneType
    :param avatar: The avatar (profile image) of the user
    :type avatar: str, NoneType
    :param banned: Defines whether or not the user is banned (``True`` if banned)
    :type banned: bool, NoneType
    :param biography: The user's biography for their profile
    :type biography: str, NoneType
    :param bonus_points: Bonus points that an admin has assigned to the user
    :type bonus_points: int, NoneType
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, NoneType
    :param deleted: Defines whether or not the user's account is deleted. (``True`` if deleted)
    :type deleted: bool, NoneType
    :param email: The email address for the user
    :type email: str, NoneType
    :param email_excluded: Defines whether or not the user has selected the "don't send me any community emails" option
    :type email_excluded: bool, NoneType
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, NoneType
    :param followers: The community members who are subscribed to the user (i.e. "friends")
    :type followers: dict, NoneType
    :param following: The community members who the user follows (i.e. "friends")
    :type following: dict, NoneType
    :param href: Relative href to the user resource (i.e. canonical path to the resource relative to the API root)
    :type href: str, NoneType
    :param images: Images uploaded by the user
    :type images: dict, NoneType
    :param kudos_given: The kudos given to the user by other community members
    :type kudos_given: dict, NoneType
    :param kudos_received: The kudos received by the user from other community members
    :type kudos_received: dict, NoneType
    :param kudos_weight: The weight of the kudos awarded
    :type kudos_weight: int, NoneType
    :param language: The default language selected by the user
    :type language: str, NoneType
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, NoneType
    :param last_visit_time: The date/time the user was last active on the community
    :type last_visit_time: type[datetime.datetime], NoneType
    :param location: The user's location
    :type location: str, NoneType
    :param login: The username (i.e. ``login``) for the user
    :type login: str, NoneType
    :param messages: The messages (topics and replies) posted by the user
    :type messages: dict, NoneType
    :param metrics: The metrics of the user activity
    :param online_status: The status of the user (``ONLINE`` or ``OFFLINE``)
    :type online_status: str, NoneType
    :param password: The password for the user
    :type password: str, NoneType
    :param personal_data: The ``personal_data`` object associated with the user account containing PII about the user
    :param public_images: Images uploaded by the user that the user has made public
    :type public_images: dict, NoneType
    :param rank: The rank of the user in the community (Value is ``-1`` if no rank has been achieved)
    :type rank: dict, NoneType
    :param registration_data: Registration information about the user
    :type registration_data: dict, NoneType
    :param reviews: Product reviews written by the user
    :type reviews: dict, NoneType
    :param roles: The roles that have been assigned to the user
    :type roles: dict, NoneType
    :param signature_topics: Topics of interest associated with this user account that the user has selected to display
    :param solutions_authored: The solutions authored by the user (i.e posts selected as an accepted solutions)
    :type solutions_authored: dict, NoneType
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, NoneType
    :param threads_participated: The topic IDs of message threads in which the user has participated
    :type threads_participated: list, NoneType
    :param topics: Topic messages (i.e the root message of a conversation) authored by the user
    :type topics: dict, NoneType
    :param user_badges: Badges earned by the user (as well as visible but unearned badges depending on admin settings)
    :param videos: Videos uploaded by the user
    :type videos: dict, NoneType
    :param view_href: The fully-qualified href to the user resource in the Web UI (i.e. the URI of the ViewProfile page)
    :type view_href: str, NoneType
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, NoneType
    :returns: The dictionary containing the user settings
    """
    default_settings = {
        'id': user_id,
        'albums': albums,
        'avatar': avatar,
        'banned': banned,
        'biography': biography,
        'bonus_points': bonus_points,
        'cover_image': cover_image,
        'deleted': deleted,
        'email': email,
        'email_excluded': email_excluded,
        'first_name': first_name,
        'followers': followers,
        'following': following,
        'href': href,
        'images': images,
        'kudos_given': kudos_given,
        'kudos_received': kudos_received,
        'kudos_weight': kudos_weight,
        'language': language,
        'last_name': last_name,
        'last_visit_time': last_visit_time,
        'location': location,
        'login': login,
        'messages': messages,
        'metrics': metrics,
        'online_status': online_status,
        'password': password,
        'personal_data': personal_data,
        'public_images': public_images,
        'rank': rank,
        'registration_data': registration_data,
        'reviews': reviews,
        'roles': roles,
        'signature_topics': signature_topics,
        'solutions_authored': solutions_authored,
        'sso_id': sso_id,
        'threads_participated': threads_participated,
        'topics': topics,
        'user_badges': user_badges,
        'videos': videos,
        'view_href': view_href,
        'web_page_url': web_page_url
    }
    # Use the default settings if settings are not explicitly defined
    if not user_settings:
        user_settings = default_settings

    # Overwrite any settings where fields are explicitly passed as arguments
    for field_name, field_value in default_settings.items():
        if default_settings[field_name]:
            user_settings[field_name] = field_value

    # Ensure the User ID uses 'id' rather than 'user_id' as the field name
    if 'user_id' in user_settings and 'id' not in user_settings:
        user_settings['id'] = user_settings['user_id']
        del user_settings['user_id']
    return user_settings


def structure_payload(user_settings=None, login=None, email=None, password=None, first_name=None, last_name=None,
                      biography=None, sso_id=None, web_page_url=None, cover_image=None):
    """This function properly structures the payload to be passed when creating or manipulating users via the API.

    :param user_settings: Allows all user settings to be passed to the function within a single dictionary
    :type user_settings: dict, NoneType
    :param login: The username (i.e. ``login``) for the user (**required**)
    :type login: str, NoneType
    :param email: The email address for the user (**required**)
    :type email: str, NoneType
    :param password: The password for the user
    :type password: str, NoneType
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, NoneType
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, NoneType
    :param biography: The user's biography for their profile
    :type biography: str, NoneType
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, NoneType
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, NoneType
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, NoneType
    :returns: The properly formatted payload within a dictionary
    """
    payload_mapping = {
        'biography': biography,
        'cover_image': cover_image,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'login': login,
        'password': password,
        'sso_id': sso_id,
        'web_page_url': web_page_url
    }
    payload = {}
    if user_settings:
        payload.update(user_settings)
    for field_name, field_value in payload_mapping.items():
        if payload_mapping[field_name]:
            payload[field_name] = field_value
    payload = {'data': payload}
    return payload


def delete(khoros_object, user_id, return_json=False):
    """This function deletes a user from the Khoros Community environment.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID of the user to be deleted
    :type user_id: str, int
    :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :returns: The API response (optionally in JSON format)
    """
    query_url = f"{khoros_object._settings['v2_base']}/users/{user_id}"
    return api.delete(query_url, return_json, auth_dict=khoros_object.auth)


def _get_where_clause_for_user_id(_user_settings):
    """This function defines the WHERE clause syntax for the LiQL query to retrieve the User ID for a user.

    :param _user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type _user_settings: dict
    :returns: The WHERE clause in string format
    :raises: py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if _user_settings['login']:
        _where_clause = f'login = "{_user_settings["login"]}"'
    elif _user_settings['email']:
        _where_clause = f'email = "{_user_settings["email"]}"'
    elif _user_settings['first_name'] or _user_settings['last_name']:
        if _user_settings['first_name'] and _user_settings['last_name']:
            _where_clause = f'first_name = "{_user_settings["first_name"]}" and ' + \
                           f'last_name = "{_user_settings["last_name"]}"'
        elif _user_settings['last_name']:
            _where_clause = f'last_name = "{_user_settings["last_name"]}"'
        else:
            _where_clause = f'first_name = "{_user_settings["first_name"]}"'
    else:
        _exc_msg = "Missing requisite information to accurately look up the User ID of the user."
        raise errors.exceptions.MissingRequiredDataError(_exc_msg)
    return _where_clause


def get_user_id(khoros_object, user_settings=None, login=None, email=None, first_name=None, last_name=None,
                allow_multiple=False, display_warnings=True):
    """This function looks up and retrieves the User ID for a user by leveraging supplied user information.

    .. note:: The priority of supplied fields are as follows: login, email, first and last name, last name, first name

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, NoneType
    :param login: The username of the user
    :type login: str, NoneType
    :param email: The email address of the user
    :type email: str, NoneType
    :param first_name: The first name (i.e. given name) of the user
    :type first_name: str, NoneType
    :param last_name: The last name (i.e. surname) of the user
    :type last_name: str, NoneType
    :param allow_multiple: Allows a list of User IDs to be returned if multiple results are found (``False`` by default)
    :type allow_multiple: bool
    :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
    :type display_warnings: bool
    :returns: The User ID of the user as an integer or a list of User IDs if ``allow_multiple`` is ``True``
    """
    user_settings = process_user_settings(user_settings, login=login, email=email,
                                          first_name=first_name, last_name=last_name)
    where_clause = _get_where_clause_for_user_id(user_settings)
    liql_query = f"select id from users where {where_clause}"
    query_url = liql.get_query_url(khoros_object.core, liql_query)
    api_response = liql.perform_query(khoros_object, query_url)
    if not api.query_successful(api_response):
        # TODO: Pass the actual failure information to the exception class for a more customized error
        raise errors.exceptions.GETRequestError
    num_results = api.get_results_count(api_response)
    if num_results == 0:
        raise errors.exceptions.NotFoundResponseError
    elif num_results > 1:
        multiple_results_msg = "Multiple results were retrieved when querying for the user in question."
        if display_warnings:
            warnings.warn(multiple_results_msg, RuntimeWarning)
        if not allow_multiple:
            raise errors.exceptions.TooManyResultsError(multiple_results_msg)
        user_id = []
        for user in api_response['data']['items']:
            user_id.append(int(user['id']))
    else:
        user_id = int(api_response['data']['items'][0]['id'])
    return user_id
