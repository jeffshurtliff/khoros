# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.sub
:Synopsis:          This module includes functions that handle tags within a Khoros Community environment
:Usage:             ``from khoros.objects import subscriptions``
:Example:           ``response = subscribe_to_board(khoros_object, 'my-forum')``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     07 Apr 2021
"""

from .. import api, errors
from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def add_subscription(khoros_object, target_id, target_type='board', payload=None, included_boards=None,
                     excluded_boards=None, label_board=None, proxy_user_object=None):
    """This function adds a subscription to a given target for the current user.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param target_id: The unique identifier for the target (e.g. Node ID, Message ID, etc.)
    :type target_id: str, int
    :param target_type: The target type such as ``board`` (default), ``message``, ``category``, etc.
    :param payload: Pre-constructed payload to use in the API call
    :type payload: dict, None
    :param included_boards: One or more boards (represented by Node ID) to be included in the partial subscription
    :type included_boards: list, tuple, set, str, None
    :param excluded_boards: One or more boards (represented by Node ID) to be excluded from the partial subscription
    :type excluded_boards: list, tuple, set, str, None
    :param label_board: The Board ID associated with a label (required for label subscriptions)
    :type label_board: str, int, None
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response in JSON format
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    if not payload:
        if target_type == 'category':
            payload = {"data": _construct_category_payload(target_id, included_boards, excluded_boards)}
        elif target_type == 'label':
            if not label_board:
                raise errors.exceptions.MissingRequiredDataError("A board ID is required when subscribing to labels")
            payload = {
                "data": _construct_target_subscription(target_id, target_type),
                "board": {"id": f"{label_board}"}
            }
        else:
            payload = {"data": _construct_target_subscription(target_id, target_type)}
    else:
        payload = {"data": payload} if not payload.get('data') else payload
    uri = get_subscription_uri(khoros_object)
    response = api.post_request_with_retries(uri, json_payload=payload, khoros_object=khoros_object,
                                             proxy_user_object=proxy_user_object)
    return response


def get_subscription_uri(khoros_object):
    """This function returns the subscriptions URI for the v2 API to perform API calls.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :returns: The full (absolute) URI for the ``subscriptions`` v2 API endpoint
    """
    return f"{khoros_object.core_settings.get('v2_base')}/subscriptions"


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
            "id": f"{_target_id}"
        }
    }
    return _target


# noinspection PyTypeChecker
def _construct_category_payload(_node_id, _included_boards=None, _excluded_boards=None):
    """This function constructs the payload for a full or partial category subscription.

    .. versionchanged:: 4.0.0
       Fixed an issue where the payload was getting double-wrapped with the ``data`` dictionary key.

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
    _payload = _construct_target_subscription(_node_id, 'category')

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
            _payload[_partial_field] = _container
    return _payload


def subscribe_to_board(khoros_object, node_id, proxy_user_object=None):
    """This function subscribes the current user to an individual message.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param node_id: The unique identifier for a board (i.e. Board ID)
    :type node_id: str
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response in JSON format
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    return add_subscription(khoros_object, node_id, 'board', proxy_user_object=proxy_user_object)


def subscribe_to_category(khoros_object, node_id, included_boards=None, excluded_boards=None, proxy_user_object=None):
    """This function subscribes the current user to a full or partial category.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param node_id: The unique identifier (i.e. Node ID) for the category
    :type node_id: str
    :param included_boards: One or more boards (represented by Node ID) to be included in the partial subscription
    :type included_boards: list, tuple, set, str, None
    :param excluded_boards: One or more boards (represented by Node ID) to be excluded from the partial subscription
    :type excluded_boards: list, tuple, set, str, None
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response in JSON format
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    return add_subscription(khoros_object, node_id, 'category',
                            included_boards=included_boards, excluded_boards=excluded_boards,
                            proxy_user_object=proxy_user_object)


def subscribe_to_label(khoros_object, label, board_id, proxy_user_object=None):
    """This function subscribes the current user to label found on a board.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param label: The label to which to subscribe
    :type label: str, int
    :param board_id: The unique identifier (i.e. Node ID) for the board where the label is found
    :type board_id: str
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response in JSON format
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    return add_subscription(khoros_object, label, 'label', label_board=board_id, proxy_user_object=proxy_user_object)


def subscribe_to_message(khoros_object, msg_id, proxy_user_object=None):
    """This function subscribes the current user to an individual message.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param msg_id: The unique identifier for an individual message
    :type msg_id: str, int
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response in JSON format
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    return add_subscription(khoros_object, msg_id, 'message', proxy_user_object=proxy_user_object)


def subscribe_to_product(khoros_object, product_id, proxy_user_object=None):
    """This function subscribes the current user to a product.

    .. versionchanged:: 4.0.0
       Introduced the ``proxy_user_object`` parameter to allow API requests to be performed on behalf of other users.

    .. versionadded:: 3.5.0

    :param khoros_object: The core Khoros object
    :type khoros_object: class[khoros.Khoros]
    :param product_id: The unique identifier for a product
    :type product_id: str, int
    :param proxy_user_object: Instantiated :py:class:`khoros.objects.users.ImpersonatedUser` object to perform the
                              API request on behalf of a secondary user.
    :type proxy_user_object: class[khoros.objects.users.ImpersonatedUser], None
    :returns: The API response in JSON format
    :raises: :py:exc:`ValueError`, :py:exc:`khoros.errors.exceptions.APIConnectionError`,
             :py:exc:`khoros.errors.exceptions.POSTRequestError`,
             :py:exc:`khoros.errors.exceptions.PayloadMismatchError`
    """
    return add_subscription(khoros_object, product_id, 'product', proxy_user_object=proxy_user_object)
