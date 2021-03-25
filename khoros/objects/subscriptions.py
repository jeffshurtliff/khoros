# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.sub
:Synopsis:          This module includes functions that handle tags within a Khoros Community environment
:Usage:             ``from khoros.objects import subscriptions``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     25 Mar 2021
"""

from .. import api, errors
from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def subscribe_to_node(khoros_object, node_id, node_type='board', included_boards=None, excluded_boards=None):
    # TODO: Add docstring
    if node_type not in ['board', 'category', 'grouphub']:
        raise errors.exceptions.InvalidNodeTypeError(val=node_type)
    # TODO: Finish the function
    return


def _construct_target_subscription(_target_id, _target_type='board'):
    """This function constructs a dictionary for an individual subscription target to be used in a payload.

    .. versionadded:: 3.5.0

    :param _target_id: The unique identifier for the target (e.g. Node ID)
    :type _target_id: str
    :param _target_type: The target type (``board`` by default)
    :type _target_type: str
    :returns: The dictionary for the individual target
    :raises: :py:exc:`TypeError`
    """
    _target = {
        "type": "subscription",
        "target": {
            "type": _target_type,
            "id": _target_id
        }
    }
    return _target


# noinspection PyTypeChecker
def _construct_category_payload(_node_id, _included_boards=None, _excluded_boards=None):
    """This function constructs the payload for a full or partial category subscription.

    .. versionadded:: 3.5.0

    :param _node_id: The unique identifier (i.e. Node ID) of the category
    :type _node_id: str
    :param _included_boards: One or more boards (represented by Node ID) to be included in the partial subscription
    :type _included_boards: list, tuple, set, str, None
    :param _excluded_boards: One or more boards (represented by Node ID) to be excluded from the partial subscription
    :type _excluded_boards: list, tuple, set, str, None
    :returns: The payload to use in the API call as a dictionary
    :raises: :py:exc:`khoros.errors.exceptions.DataMismatchError`
    """
    # Construct the base data dictionary
    _data = _construct_target_subscription(_node_id, 'category')

    # Ensure that only one populated partial option has been provided
    if _included_boards and _excluded_boards:
        raise errors.exceptions.DataMismatchError("Partial category subscriptions only support internal or external "
                                                  "boards but not both")

    # Added included or excluded boards when applicable
    _partials = {
        "includes": _included_boards,
        "excludes": _excluded_boards
    }
    for _partial_field, _boards in _partials.items():
        _boards = [_boards] if _boards and isinstance(_boards, str) else _boards
        if _boards and core_utils.is_iterable(_boards):
            _container = []
            for _board in _boards:
                _container.append(_construct_target_subscription(_board))
            _data[_partial_field] = _container

    # Wrap the data within the 'data' field in the payload
    _payload = {'data': _data}
    return _payload


def subscribe_to_category(khoros_object, node_id, included_boards=None, excluded_boards=None):
    """This function subscribes the current user to a full or partial category.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param node_id: The unique identifier (i.e. Node ID) for the category
    :type node_id: str
    :param included_boards: One or more boards (represented by Node ID) to be included in the partial subscription
    :type included_boards: list, tuple, set, str, None
    :param excluded_boards: One or more boards (represented by Node ID) to be excluded from the partial subscription
    :type excluded_boards: list, tuple, set, str, None
    :returns: The API response in JSON format
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    uri = f"{khoros_object.core_settings.get('v2_base')}/subscriptions"
    payload = _construct_category_payload(node_id, included_boards, excluded_boards)
    response = api.post_request_with_retries(uri, json_payload=payload, khoros_object=khoros_object)
    return response


