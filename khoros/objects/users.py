# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.users
:Synopsis:          This module includes functions that handle user-related operations.
:Usage:             ``from khoros.objects import users``
:Example:           ``khoros.users.create(username='john_doe', email='john.doe@example.com')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Jan 2022
"""

import warnings

from .. import api, auth, liql, errors
from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


# Create an ImpersonatedUser class to pass to other functions
class ImpersonatedUser(object):
    """This class is used for impersonating another user when performing other functions throughout the library.

    .. versionchanged:: 4.2.0
       Added support for user impersonation with LithiumSSO token authentication.

    .. versionadded:: 4.0.0
    """
    def __init__(self, user_login=None, admin_object=None):
        """This method instantiates the :py:class:`khoros.objects.users.ImpersonatedUser` object.

        .. versionadded:: 4.0.0

        :param user_login: The username (i.e. login) of the user to be impersonated
        :type user_login: str, None
        :param admin_object: The :py:class:`khoros.core.Khoros` object of a user with an Administrator role
        :type admin_object: class[khoros.Khoros], None
        """
        # Define default object values
        self.configured = False
        self.login = user_login
        self.session_key = None
        self.session_header = None

        # Authenticate the user if possible
        if not user_login:
            logger.error('The ImpersonatedUser object cannot be configured as no user login was provided')
        else:
            if not admin_object:
                logger.error('The ImpersonatedUser object cannot be configured as no admin-level Khoros object '
                             'was provided to authenticate the new user')
            else:
                if "session_key" in admin_object.auth:
                    self.session_key = auth.get_session_key(admin_object, user_login)
                    if self.session_key:
                        self.session_header = auth.get_session_header(self.session_key)
                        self.configured = True
                    else:
                        logger.warning('The session header for the impersonated user was not populated because a '
                                       'session key was not successfully acquired')
                else:
                    logger.error('The ImpersonatedUser object cannot be configured as the admin-level Khoros object '
                                 'has not been authenticated.')

    def __del__(self):
        """This method fully destroys the instance.

        .. versionadded:: 4.0.0
        """
        self.close()

    def close(self):
        """This method destroys the instance.

        .. versionadded:: 4.0.0
        """


def impersonate_user(khoros_object, user_login):
    """This function instantiates and returns the :py:class`khoros.objects.users.ImpersonatedUser` object which
       can then be passed to other methods and functions to perform operations as a secondary user.

    .. versionadded:: 4.0.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object

                          .. note:: The authenticated user must have the **Administrator** role and/or have the
                                    **Switch User** permission enabled.

    :type khoros_object: class[khoros.Khoros]
    :param user_login: The username (i.e. login) of ther user to be impersonated
    :type user_login: str
    :returns: The instantiated :py:class`khoros.objects.users.ImpersonatedUser` object
    """
    return ImpersonatedUser(user_login=user_login, admin_object=khoros_object)


def create(khoros_object, user_settings=None, login=None, email=None, password=None, first_name=None, last_name=None,
           biography=None, sso_id=None, web_page_url=None, cover_image=None, ignore_exceptions=False):
    """This function creates a new user in the Khoros Community environment.

    .. versionchanged:: 4.0.0
       This function now returns the API response and the ``ignore_exceptions`` parameter has been introduced.

    .. versionchanged:: 3.3.0
       Updated ``khoros_object._settings`` to be ``khoros_object.core_settings``.

    .. versionchanged:: 2.7.4
       The HTTP headers were changed to be all lowercase in order to be standardized across the library.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: Allows all user settings to be passed to the function within a single dictionary
    :type user_settings: dict, None
    :param login: The username (i.e. ``login``) for the user (**required**)
    :type login: str, None
    :param email: The email address for the user (**required**)
    :type email: str, None
    :param password: The password for the user
    :type password: str, None
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, None
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, None
    :param biography: The user's biography for their profile
    :type biography: str, None
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, None
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, None
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, None
    :param ignore_exceptions: Defines whether to raise the :py:exc:`khoros.errors.exceptions.UserCreationError`
                              exception if the creation attempt fails (``False`` by default)
    :type ignore_exceptions: bool
    :returns: The response to the user creation API request
    :raises: :py:exc:`KeyError`, :py:exc:`khoros.errors.exceptions.UserCreationError`
    """
    # TODO: Add functionality for followers, following, rank, roles, user_avatar and user_badges
    payload = structure_payload(user_settings, login, email, password, first_name, last_name, biography, sso_id,
                                web_page_url, cover_image)
    query_url = f"{khoros_object.core_settings.get('v2_base')}/users"
    headers = {'content-type': 'application/json'}
    response = api.post_request_with_retries(query_url, payload, auth_dict=khoros_object.auth, headers=headers)
    if not api.query_successful(response) and not ignore_exceptions:
        raise errors.exceptions.UserCreationError(user=payload.get('login'), exc_msg=response.get('message'))
    return response


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
    :type user_settings: dict, None
    :param user_id: The unique User ID associated with the user
    :type user_id: int, str, None
    :param albums: The image albums associated with the user's profile
    :type albums: dict, None
    :param avatar: The avatar (profile image) of the user
    :type avatar: str, None
    :param banned: Defines whether or not the user is banned (``True`` if banned)
    :type banned: bool, None
    :param biography: The user's biography for their profile
    :type biography: str, None
    :param bonus_points: Bonus points that an admin has assigned to the user
    :type bonus_points: int, None
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, None
    :param deleted: Defines whether or not the user's account is deleted. (``True`` if deleted)
    :type deleted: bool, None
    :param email: The email address for the user
    :type email: str, None
    :param email_excluded: Defines whether or not the user has selected the "don't send me any community emails" option
    :type email_excluded: bool, None
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, None
    :param followers: The community members who are subscribed to the user (i.e. "friends")
    :type followers: dict, None
    :param following: The community members who the user follows (i.e. "friends")
    :type following: dict, None
    :param href: Relative href to the user resource (i.e. canonical path to the resource relative to the API root)
    :type href: str, None
    :param images: Images uploaded by the user
    :type images: dict, None
    :param kudos_given: The kudos given to the user by other community members
    :type kudos_given: dict, None
    :param kudos_received: The kudos received by the user from other community members
    :type kudos_received: dict, None
    :param kudos_weight: The weight of the kudos awarded
    :type kudos_weight: int, None
    :param language: The default language selected by the user
    :type language: str, None
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, None
    :param last_visit_time: The date/time the user was last active on the community
    :type last_visit_time: type[datetime.datetime], None
    :param location: The user's location
    :type location: str, None
    :param login: The username (i.e. ``login``) for the user
    :type login: str, None
    :param messages: The messages (topics and replies) posted by the user
    :type messages: dict, None
    :param metrics: The metrics of the user activity
    :param online_status: The status of the user (``ONLINE`` or ``OFFLINE``)
    :type online_status: str, None
    :param password: The password for the user
    :type password: str, None
    :param personal_data: The ``personal_data`` object associated with the user account containing PII about the user
    :param public_images: Images uploaded by the user that the user has made public
    :type public_images: dict, None
    :param rank: The rank of the user in the community (Value is ``-1`` if no rank has been achieved)
    :type rank: dict, None
    :param registration_data: Registration information about the user
    :type registration_data: dict, None
    :param reviews: Product reviews written by the user
    :type reviews: dict, None
    :param roles: The roles that have been assigned to the user
    :type roles: dict, None
    :param signature_topics: Topics of interest associated with this user account that the user has selected to display
    :param solutions_authored: The solutions authored by the user (i.e posts selected as an accepted solutions)
    :type solutions_authored: dict, None
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, None
    :param threads_participated: The topic IDs of message threads in which the user has participated
    :type threads_participated: list, None
    :param topics: Topic messages (i.e the root message of a conversation) authored by the user
    :type topics: dict, None
    :param user_badges: Badges earned by the user (as well as visible but unearned badges depending on admin settings)
    :param videos: Videos uploaded by the user
    :type videos: dict, None
    :param view_href: The fully-qualified href to the user resource in the Web UI (i.e. the URI of the ViewProfile page)
    :type view_href: str, None
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, None
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
        if default_settings.get(field_name):
            user_settings[field_name] = field_value

    # Ensure the User ID uses 'id' rather than 'user_id' as the field name
    if 'user_id' in user_settings and 'id' not in user_settings:
        user_settings['id'] = user_settings['user_id']
        del user_settings['user_id']
    return user_settings


def structure_payload(user_settings=None, login=None, email=None, password=None, first_name=None, last_name=None,
                      biography=None, sso_id=None, web_page_url=None, cover_image=None):
    """This function properly structures the payload to be passed when creating or manipulating users via the API.

    .. versionchanged:: 4.0.0
       Fixed an issue that was resulting in a :py:exc:`KeyError` exception potentially getting raised, and added
       the missing ``type`` key that was preventing users from getting created successfully.

    :param user_settings: Allows all user settings to be passed to the function within a single dictionary
    :type user_settings: dict, None
    :param login: The username (i.e. ``login``) for the user (**required**)
    :type login: str, None
    :param email: The email address for the user (**required**)
    :type email: str, None
    :param password: The password for the user
    :type password: str, None
    :param first_name: The user's first name (i.e. given name)
    :type first_name: str, None
    :param last_name: The user's last name (i.e. surname)
    :type last_name: str, None
    :param biography: The user's biography for their profile
    :type biography: str, None
    :param sso_id: The Single Sign-On (SSO) ID for the user
    :type sso_id: str, None
    :param web_page_url: The URL to the user's website
    :type web_page_url: str, None
    :param cover_image: The cover image to be used on the user's profile
    :type cover_image: str, None
    :returns: The properly formatted payload within a dictionary
    """
    payload_mapping = {
        'type': 'user',
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
        if payload_mapping.get(field_name):
            payload[field_name] = field_value
    payload = {'data': payload}
    return payload


def update_sso_id(khoros_object, new_sso_id, user_id=None, user_login=None):
    """This function updates the SSO ID for a user.

    .. versionadded:: 4.5.0

    .. caution:: This functionality is currently unsupported directly via REST API. It is recommended that FreeMarker
                 and a custom endpoint be leveraged instead. See `Khoros Atlas <https://bit.ly/33iGZmW>`_
                 for more details.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param new_sso_id: The new SSO ID for the user
    :type new_sso_id: str
    :param user_id: The numeric User ID that identifies the user
    :type user_id: str, int, None
    :param user_login: The username that identifies the user
    :type user_login: str, None
    :returns: The API response
    :raises: py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    # TODO: Remove the raised exception below if/when the functionality becomes available directly via REST API
    raise errors.exceptions.CurrentlyUnsupportedError(message='Updating the SSO ID via REST API is currently '
                                                      'unsupported. It is recommended that FreeMarker and a custom '
                                                      'endpoint be used instead. Refer: https://bit.ly/33iGZmW')
    # if not user_id and not user_login:
    #     raise errors.exceptions.MissingRequiredDataError('A user ID or login is required to update a user.')
    # payload = {'value': f'{new_sso_id}'}
    # if user_id:
    #     endpoint = f'/users/id/{user_id}/sso_id/set'
    # else:
    #     endpoint = f'/users/id/{user_login}/sso_id/set'
    # return api.make_v1_request(khoros_object, endpoint, payload, 'POST')


def delete(khoros_object, user_id, return_json=False):
    """This function deletes a user from the Khoros Community environment.

    .. versionchanged:: 3.3.0
       Updated ``khoros_object._settings`` to be ``khoros_object.core_settings``.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID of the user to be deleted
    :type user_id: str, int
    :param return_json: Determines if the API response should be returned in JSON format (``False`` by default)
    :type return_json: bool
    :returns: The API response (optionally in JSON format)
    :raises: :py:exc:`khoros.errors.exceptions.FeatureNotConfiguredError`
    """
    # TODO: Allow other identifiers (e.g. login, email, etc.) to be provided instead of just the User ID
    query_url = f"{khoros_object.core_settings['v2_base']}/users/{user_id}"
    response = api.delete(query_url, return_json, auth_dict=khoros_object.auth)
    if response.status_code == 403 and 'Feature is not configured' in response.text:
        try:
            identifier = response.text.split('identifier: ')[1].split('"')[0]
            raise errors.exceptions.FeatureNotConfiguredError(identifier=identifier)
        except IndexError:
            raise errors.exceptions.FeatureNotConfiguredError()
    if return_json:
        response = response.json()
    return response


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


def _get_where_clause_for_username(_user_settings):
    """This function defines the WHERE clause syntax for the LiQL query to retrieve the username for a user.

    :param _user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type _user_settings: dict
    :returns: The WHERE clause in string format
    :raises: py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if _user_settings['id']:
        _where_clause = f'id = "{_user_settings["id"]}"'
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
        _exc_msg = "Missing requisite information to accurately look up the username of the user."
        raise errors.exceptions.MissingRequiredDataError(_exc_msg)
    return _where_clause


def _get_where_clause_for_email(_user_settings):
    """This function defines the WHERE clause syntax for the LiQL query to retrieve the email address for a user.

    :param _user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type _user_settings: dict
    :returns: The WHERE clause in string format
    :raises: py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if _user_settings['id']:
        _where_clause = f'id = "{_user_settings["id"]}"'
    elif _user_settings['login']:
        _where_clause = f'login = "{_user_settings["login"]}"'
    elif _user_settings['first_name'] or _user_settings['last_name']:
        if _user_settings['first_name'] and _user_settings['last_name']:
            _where_clause = f'first_name = "{_user_settings["first_name"]}" and ' + \
                            f'last_name = "{_user_settings["last_name"]}"'
        elif _user_settings['last_name']:
            _where_clause = f'last_name = "{_user_settings["last_name"]}"'
        else:
            _where_clause = f'first_name = "{_user_settings["first_name"]}"'
    else:
        _exc_msg = "Missing requisite information to accurately look up the email address of the user."
        raise errors.exceptions.MissingRequiredDataError(_exc_msg)
    return _where_clause


def _get_user_identifier(_khoros_object, _identifier, _where_clause, _allow_multiple, _display_warnings):
    """Retrieves a user identifier (e.g. ``email``, ``last_visit_timer``, etc.) using a LiQL query.

    .. versionchanged:: 2.4.0
       Fixed how and when values should be cast to integers.
    """
    _liql_query = f"select {_identifier} from users where {_where_clause}"
    _api_response = liql.perform_query(_khoros_object, liql_query=_liql_query, verify_success=True)
    _num_results = api.get_results_count(_api_response)
    if _num_results == 0:
        raise errors.exceptions.NotFoundResponseError
    elif _num_results > 1:
        _multiple_results_msg = "Multiple results were retrieved when querying for the user in question."
        if _display_warnings:
            warnings.warn(_multiple_results_msg, RuntimeWarning)
        if not _allow_multiple:
            raise errors.exceptions.TooManyResultsError(_multiple_results_msg)
        _user_identifier = []
        for _user in _api_response['data']['items']:
            _item_val = int(_user[_identifier]) if _user[_identifier].isnumeric() else _user[_identifier]
            _user_identifier.append(_item_val)
    else:
        _item_val = _api_response['data']['items'][0][_identifier]
        _user_identifier = int(_item_val) if _item_val.isnumeric() else _item_val
    return _user_identifier


def get_user_id(khoros_object, user_settings=None, login=None, email=None, first_name=None, last_name=None,
                allow_multiple=False, display_warnings=True, fail_on_no_results=False):
    """This function looks up and retrieves the User ID for a user by leveraging supplied user information.

    .. note:: The priority of supplied fields are as follows: login, email, first and last name, last name, first name

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :param first_name: The first name (i.e. given name) of the user
    :type first_name: str, None
    :param last_name: The last name (i.e. surname) of the user
    :type last_name: str, None
    :param allow_multiple: Allows a list of User IDs to be returned if multiple results are found (``False`` by default)
    :type allow_multiple: bool
    :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
    :type display_warnings: bool
    :param fail_on_no_results: Raises an exception if no results are returned (``False`` by default)
    :type fail_on_no_results: bool
    :returns: The username of the user as a string or a list of usernames if ``allow_multiple`` is ``True``
    """
    user_settings = process_user_settings(user_settings, login=login, email=email,
                                          first_name=first_name, last_name=last_name)
    where_clause = _get_where_clause_for_user_id(user_settings)
    if 'email' in where_clause:
        user_id = get_user_data_with_v1(khoros_object, 'id', user_settings['email'], 'email', fail_on_no_results)
    else:
        user_id = _get_user_identifier(khoros_object, 'id', where_clause, allow_multiple, display_warnings)
    return user_id


def get_username(khoros_object, user_settings=None, user_id=None, email=None, first_name=None, last_name=None,
                 allow_multiple=False, display_warnings=True, fail_on_no_results=False):
    """This function looks up and retrieves the username for a user by leveraging supplied user information.

    .. note:: The priority of supplied fields are as follows: User ID, email, first and last name, last name, first name

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID of the user
    :type user_id: str, None
    :param email: The email address of the user
    :type email: str, None
    :param first_name: The first name (i.e. given name) of the user
    :type first_name: str, None
    :param last_name: The last name (i.e. surname) of the user
    :type last_name: str, None
    :param allow_multiple: Allows a list of usernames to be returned if multiple results are found
    :type allow_multiple: bool
    :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
    :type display_warnings: bool
    :param fail_on_no_results: Raises an exception if no results are returned (``False`` by default)
    :type fail_on_no_results: bool
    :returns: The User ID of the user as an integer or a list of User IDs if ``allow_multiple`` is ``True``
    """
    user_settings = process_user_settings(user_settings, user_id=user_id, email=email,
                                          first_name=first_name, last_name=last_name)
    where_clause = _get_where_clause_for_username(user_settings)
    if 'email' in where_clause:
        username = get_user_data_with_v1(khoros_object, 'login', user_settings['email'], 'email', fail_on_no_results)
    else:
        username = _get_user_identifier(khoros_object, 'login', where_clause, allow_multiple, display_warnings)
    return username


def get_login(khoros_object, user_settings=None, user_id=None, email=None, first_name=None, last_name=None,
              allow_multiple=False, display_warnings=True):
    """This is an alternative function name for the :py:func:`khoros.objects.users.get_username` function."""
    return get_username(khoros_object, user_settings, user_id, email, first_name, last_name,
                        allow_multiple, display_warnings)


def get_email(khoros_object, user_settings=None, user_id=None, login=None, first_name=None, last_name=None,
              allow_multiple=False, display_warnings=True):
    """This function looks up and retrieves the email address for a user by leveraging supplied user information.

    .. note:: The priority of supplied fields are as follows: User ID, username, first and last name, last name,
              first name

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID of the user
    :type user_id: str, None
    :param login: The username of the user
    :type login: str, None
    :param first_name: The first name (i.e. given name) of the user
    :type first_name: str, None
    :param last_name: The last name (i.e. surname) of the user
    :type last_name: str, None
    :param allow_multiple: Allows a list of email addresses to be returned if multiple results are found
    :type allow_multiple: bool
    :param display_warnings: Determines if warning messages should be displayed (``True`` by default)
    :type display_warnings: bool
    :returns: The email address of the user as a string or a list of email addresses if ``allow_multiple`` is ``True``
    """
    user_settings = process_user_settings(user_settings, user_id=user_id, login=login,
                                          first_name=first_name, last_name=last_name)
    where_clause = _get_where_clause_for_email(user_settings)
    return _get_user_identifier(khoros_object, 'email', where_clause, allow_multiple, display_warnings)


def query_users_table_by_id(khoros_object, select_fields, user_id, first_item=False):
    """This function queries the ``users`` table for one or more given SELECT fields for a specific User ID using LiQL.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param select_fields: One or more SELECT field (e.g. ``login``, ``messages.count(*)``, etc.) to query
    :type select_fields: str, tuple, list, set
    :param user_id: The User ID associated with the user
    :type user_id: int, str
    :param first_item: Determines if only the first item should be returned (``False`` by default)
    :type first_item: bool
    :returns: The API response for the performed LiQL query
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    if type(select_fields) == tuple or type(select_fields) == list or type(select_fields) == set:
        select_fields = ','.join(select_fields)
    liql_query = f"select {select_fields} from users where id = '{user_id}'"
    api_response = liql.perform_query(khoros_object, liql_query=liql_query, verify_success=True)
    if first_item:
        api_response = api_response['data']['items'][0]
    return api_response


def _get_count(_khoros_object, _user_id, _object_type):
    """This function returns the count of a specific user object (e.g. ``albums``, ``followers``, etc.) for a user.

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _user_id: The User ID associated with the user
    :type _user_id: int, str
    :param _object_type: The type of object for which to get the count (e.g. ``albums``, ``followers``, etc.)
    :returns: The user object count as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    _api_response = query_users_table_by_id(_khoros_object, f'{_object_type}.count(*)', _user_id)
    return int(_api_response['data']['items'][0][_object_type]['count'])


def _get_sum_weight(_khoros_object, _user_id, _object_type):
    """This function returns the sum weight (e.g. ``kudos_received``, ``kudos_given``) for a specific User ID.

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _user_id: The User ID associated with the user
    :type _user_id: int, str
    :param _object_type: The type of object for which to get the count (e.g. ``albums``, ``followers``, etc.)
    :returns: The sum weight for the object type as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    _api_response = query_users_table_by_id(_khoros_object, f'{_object_type}.sum(weight)', _user_id)
    return int(_api_response['data']['items'][0][_object_type]['sum']['weight'])


def _process_settings_and_user_id(_khoros_object, _user_settings, _user_id, _login, _email):
    """This function processes the user settings and ensures that the User ID is present.

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :param _user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type _user_settings: dict, None
    :param _user_id: The User ID associated with the user
    :type _user_id: int, str, None
    :param _login: The username associated with the user
    :type _login: str, None
    :param _email: The email address associated with the user
    :returns: An updated user settings dictionary
    """
    _user_settings = process_user_settings(_user_settings, user_id=_user_id, login=_login, email=_email)
    if not _user_settings['id']:
        _user_settings['id'] = get_user_id(_khoros_object, _user_settings)
    return _user_settings


def get_user_data(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function retrieves all user data for a given user.

    :param khoros_object: he core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: A dictionary containing the user data for the user
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    api_response = query_users_table_by_id(khoros_object, '*', user_settings['id'])
    return api_response['data']


def get_user_data_with_v1(khoros_object, return_field, filter_value, filter_field='email', fail_on_no_results=False):
    """This function retrieves user data using a Community API v1 call.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param return_field: The field being retrieved by the function (e.g. ``id``, ``login``, etc.)
    :type return_field: str
    :param filter_value: The value for which to filter the user data being queried
    :type filter_value: str, int
    :param filter_field: The field by which the API call should be filtered (``email`` by default)
    :type filter_field: str
    :param fail_on_no_results: Raises an exception if no results are returned (``False`` by default)
    :type fail_on_no_results: bool
    :returns: The value of the return field for the user being queried
    """
    response = api.perform_v1_search(khoros_object, 'users', filter_field, filter_value, return_json=True,
                                     fail_on_no_results=fail_on_no_results)
    try:
        # TODO: Handle situations where more than one user is returned in the API response
        return_value = response['users']['user'][0][return_field]['$']
    except IndexError:
        return_value = ''
    return return_value


def get_album_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the number of albums for a user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of albums found for the user as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'albums')


def get_followers_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of community members who have added the user as a friend in the community.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of community members who have added the user as a friend in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'followers')


def get_following_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of community members the user has added as a friend in the community.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of community members the user has added as a friend in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'following')


def get_images_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of images uploaded by the user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of images uploaded by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'images')


def get_public_images_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of public images uploaded by the user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of public images uploaded by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'public_images')


def get_messages_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of messages (topics and replies) posted by the user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of messages (topics and replies) posted by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'messages')


def get_roles_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of roles applied to the user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of roles applied to the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'roles')


def get_solutions_authored_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of messages created by the user that are marked as accepted solutions.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of messages created by the user that are marked as accepted solutions in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'solutions_authored')


def get_topics_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of topic messages (excluding replies) posted by the user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of topic messages (excluding replies) posted by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'topics')


def get_replies_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of replies posted by the user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of replies posted by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    select_fields = ('messages.count(*)', 'topics.count(*)')
    api_response = query_users_table_by_id(khoros_object, select_fields, user_settings['id'])
    items_list = api.get_items_list(api_response)
    return int(items_list['messages']['count']) - int(items_list['topics']['count'])


def get_videos_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of videos uploaded by the user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of videos uploaded by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_count(khoros_object, user_settings['id'], 'videos')


def get_kudos_given_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of kudos a user has given.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of kudos given by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_sum_weight(khoros_object, user_settings['id'], 'kudos_given')


def get_kudos_received_count(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function gets the count of kudos a user has received.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The number of kudos received by the user in integer format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    return _get_sum_weight(khoros_object, user_settings['id'], 'kudos_received')


def get_online_user_count(khoros_object):
    """This function retrieves the number of users currently online.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :returns: The user count for online users as an integer
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    liql_query = "select count(*) from users where online_status = 'online'"
    api_response = liql.perform_query(khoros_object, liql_query=liql_query, verify_success=True)
    return int(api_response['data']['count'])


def get_registration_data(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function retrieves the registration data for a given user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: A dictionary containing the registration data for the user
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    api_response = query_users_table_by_id(khoros_object, 'registration_data', user_settings['id'], first_item=True)
    return api_response['registration_data']


def get_registration_timestamp(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function retrieves the timestamp for when a given user registered for an account.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The registration timestamp in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    registration_data = get_registration_data(khoros_object, user_settings, user_id, login, email)
    # TODO: Add the ability to parse the timestamp into a datetime object or change the string format
    return registration_data['registration_time']


def get_registration_status(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function retrieves the registration status for a given user.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The registration status in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    registration_data = get_registration_data(khoros_object, user_settings, user_id, login, email)
    return registration_data['status']


def get_last_visit_timestamp(khoros_object, user_settings=None, user_id=None, login=None, email=None):
    """This function retrieves the timestamp for the last time the user logged into the community.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_settings: A dictionary containing all relevant user settings supplied in the parent function
    :type user_settings: dict, None
    :param user_id: The User ID associated with the user
    :type user_id: int, str, None
    :param login: The username of the user
    :type login: str, None
    :param email: The email address of the user
    :type email: str, None
    :returns: The last visit timestamp in string format
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    user_settings = _process_settings_and_user_id(khoros_object, user_settings, user_id, login, email)
    api_response = query_users_table_by_id(khoros_object, 'last_visit_time', user_settings['id'], first_item=True)
    # TODO: Add the ability to parse the timestamp into a datetime object or change the string format
    return api_response['last_visit_time']


def structure_user_dict_list(khoros_object=None, user_dicts=None, id_list=None, login_list=None):
    """This function structures a list of user data dictionaries for use in various API request payloads.

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_dicts: A list of dictionaries (or single dictionary) containing user data (``id`` at a minimum)
    :type user_dicts: list, dict, None
    :param id_list: A list of user IDs to be converted into user data dictionaries
    :type id_list: list, tuple, set, None
    :param login_list: A list of usernames (i.e. logins) to be converted into user data dictionaries
    :type login_list: list, tuple, set, None
    :returns: The properly formatted list of user data dictionaries for the supplied users
    :raises: :py:exc:`TypeError`, :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not any((user_dicts, id_list, login_list)):
        raise errors.exceptions.MissingRequiredDataError("At least one of the required function arguments (i.e. "
                                                         "'user_dicts', 'id_list' or 'login_list') must be provided.")

    # Ensure that the user dictionary list is in the correct format
    user_dicts = [] if not user_dicts else user_dicts
    ids_from_dicts, logins_from_dicts = [], []
    if user_dicts:
        if isinstance(user_dicts, tuple):
            user_dicts = list(user_dicts)
        elif isinstance(user_dicts, dict):
            user_dicts = [user_dicts]
        user_dicts = core_utils.convert_dict_id_values_to_strings(user_dicts)
        ids_from_dicts = core_utils.extract_key_values_from_dict_list('id', user_dicts)
        logins_from_dicts = core_utils.extract_key_values_from_dict_list('login', user_dicts, exclude_if_present='id')

    # Retrieve the IDs from the list of logins if applicable
    ids_from_dicts.append(get_ids_from_login_list(khoros_object, logins_from_dicts))

    # Ensure that the supplied ID and login lists are in the correct format
    id_list = [] if not id_list else list(id_list)
    id_list = core_utils.convert_list_values(id_list, convert_to='str')
    login_list = [] if not login_list else list(login_list)

    # Add the IDs from the login list to the existing IDs list
    id_list.extend(get_ids_from_login_list(khoros_object, login_list))

    # Populate and return the final user dictionary list
    final_dict_list = []
    for user_id in id_list:
        final_dict_list.append({"id": str(user_id)})
    return final_dict_list


def get_ids_from_login_list(khoros_object, login_list, return_type='list'):
    """This function identifies the User IDs associated with a list of user logins. (i.e. usernames)

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param login_list: List of user login (i.e. username) values in string format
    :type login_list: list, tuple
    :param return_type: Determines if the data should be returned as a ``list`` (default) or a ``dict``
    :type return_type: str
    :returns: A list or dictionary with the User IDs
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    id_list, id_dict = [], {}
    for login in login_list:
        user_id = get_user_id(khoros_object, login=login)
        id_list.append(user_id)
        id_dict[login] = user_id
    return id_list if return_type == 'list' else id_dict
