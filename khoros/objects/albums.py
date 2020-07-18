# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.albums
:Synopsis:          This module includes functions that handle albums that contain images
:Usage:             ``from khoros.objects import albums``
:Example:           ``response = albums.create_album(khoros_obj, title='My Album', hidden=True)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     17 Jul 2020
"""

from .. import api, liql, errors
from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def create(khoros_object, title=None, description=None, owner_id=None, hidden=False, default=False,
           full_response=False):
    """This function creates a new image album for a user.

    .. versionadded:: 2.3.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param title: The title of the album to be created
    :type title: str, None
    :param description: The description of the album
    :type description: str, None
    :param owner_id: The User ID of the album owner

                     .. note:: If not defined, the owner will be the user performing the API call.

    :type owner_id: str, int, None
    :param hidden: Defines if the album should be public (default) or hidden
    :type hidden: bool
    :param default: Defines if this will be the default album for the user (``False`` by default)
    :type default: bool
    :param full_response: Defines if the full response should be returned instead of the outcome (``False`` by default)
    :type full_response: bool
    :returns: Boolean value indicating a successful outcome (default) or the full API response
    """
    # TODO: Add functionality for "cover" field with "image" datatype
    album_json = format_album_json(title, description, owner_id, hidden, default)
    query_uri = f"{khoros_object.core['v2_base']}albums"
    response = api.post_request_with_retries(query_uri, album_json, khoros_object=khoros_object)
    result = api.query_successful(response)
    return response.json() if full_response else result


def format_album_json(title=None, description=None, owner_id=None, hidden=None, default=False):
    """This function formats the JSON payload for the API call.

    .. versionadded:: 2.3.0

    :param title: The title of the album to be created
    :type title: str, None
    :param description: The description of the album
    :type description: str, None
    :param owner_id: The User ID of the album owner

                     .. note:: If not defined, the owner will be the user performing the API call.

    :type owner_id: str, int, None
    :param hidden: Defines if the album should be public (default) or hidden
    :type hidden: bool
    :param default: Defines if this will be the default album for the user (``False`` by default)
    :type default: bool
    :returns: The JSON payload for the album API call
    """
    # TODO: Add functionality for "cover" field with "image" datatype
    privacy_level = {True: "private", False: "public"}
    album_json = {
        "data": {
            "type": "album",
            "title": _null_to_blank(title),
            "description": _null_to_blank(description),
            "owner": {
                "id": f"{owner_id}"
            },
            "privacy_level": privacy_level.get(hidden),
            "default": default
        }
    }
    return album_json


def _null_to_blank(_value):
    """This function returns a blank string when a null / NoneType value is passed.

    .. versionadded:: 2.3.0
    """
    return "" if _value is None else _value


def get_albums_for_user(khoros_object, user_id=None, login=None, public=None, private=None, verify_success=False,
                        allow_exceptions=True):
    """This function returns data for the albums owned by a given user.

    .. versionadded:: 2.3.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param user_id: The User ID for the album owner
    :type user_id: str, int
    :param login: The username of the album owner
    :type login: str
    :param public: Indicates that **public** albums should be returned (all albums returned by default)
    :type public: bool
    :param private: Indicates that **private** albums should be returned (all albums returned by default)
    :type private: bool
    :param verify_success: Optionally check to confirm that the API query was successful (``False`` by default)
    :type verify_success: bool
    :param allow_exceptions: Defines whether or not exceptions can be raised for responses returning errors

                             .. caution:: This does not apply to exceptions for missing required data.

    :type allow_exceptions: bool
    :returns: A list of dictionaries representing each album
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`,
             :py:exc:`khoros.errors.exceptions.MissingAuthDataError`,
             :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not user_id and not login:
        raise errors.exceptions.MissingRequiredDataError("A 'user_id' or 'login' is required to retrieve data")
    query = "SELECT * FROM albums WHERE"
    if user_id:
        if not core_utils.is_numeric(user_id) and not login:
            raise errors.exceptions.MissingRequiredDataError("The 'user_id' must be numeric or a 'login' is needed")
        query = f"{query} owner.id = '{user_id}'"
    else:
        query = f"{query} owner.login = '{login}'"
    if not public or not private:
        if public:
            query = f"{query} AND privacy_level = 'public'"
        else:
            query = f"{query} AND privacy_level = 'hidden'"
    response = liql.perform_query(khoros_object, liql_query=query, verify_success=verify_success,
                                  allow_exceptions=allow_exceptions)
    return response
