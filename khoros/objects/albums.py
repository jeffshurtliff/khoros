# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.albums
:Synopsis:          This module includes functions that handle albums that contain images
:Usage:             ``from khoros.objects import albums``
:Example:           ``response = albums.create_album(khoros_obj, title='My Album', hidden=True)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 May 2020
"""

from .. import api, errors


def create_album(khoros_object, title=None, description=None, owner_id=None, hidden=False, default=False,
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
    privacy_level = {True: "hidden", False: "public"}
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
