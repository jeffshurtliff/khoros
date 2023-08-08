# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.labels
:Synopsis:          This module includes functions that handle labels within a Khoros Community environment
:Usage:             ``from khoros.objects import labels``
:Example:           ``labels = khoros.labels.get_labels_for_message(12345)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     06 Jul 2023
"""

from .. import api, liql, errors
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def get_labels_for_message(khoros_object, message_id):
    """This function retrieves the labels associated with a specific message.

    .. versionadded:: 5.3.0

    :param khoros_object: The Khoros object initialized via the :py:mod:`khoros.core` module
    :type khoros_object: class[khoros.Khoros]
    :param message_id: The ID associated with the message to query
    :type message_id: str, int
    :returns: A list of strings for the labels
    :raises: :py:exc:`khoros.errors.exceptions.GETRequestError`
    """
    # Query for the labels
    query = f"SELECT * FROM labels WHERE messages.id = '{message_id}'"
    response = liql.perform_query(khoros_object, liql_query=query)

    # Identify the labels and store in a list
    message_labels = []
    for item in response['data']['items']:
        msg_label = item.get('text')
        message_labels.append(msg_label)

    # Return the compiled list
    return message_labels
