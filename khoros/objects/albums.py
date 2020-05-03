# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.albums
:Synopsis:          This module includes functions that handle albums that contain images
:Usage:             ``from khoros.objects import albums``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 May 2020
"""

from .. import api, errors


def create_album(khoros_object, title, description, owner_id, hidden, default, full_response=False):
    # TODO: Add functionality for "cover" field with "image" datatype
    album_json = format_album_json(title, description, owner_id, hidden, default)
    query_uri = f"{khoros_object.core['v2_base']}albums"
    response = api.post_request_with_retries(query_uri, album_json, khoros_object=khoros_object)
    result = api.query_successful(response)
    return response.json() if full_response else result


def format_album_json(title, description, owner_id, hidden, default):
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
    """This function returns a blank string when a null / NoneType value is passed."""
    return "" if _value is None else _value
