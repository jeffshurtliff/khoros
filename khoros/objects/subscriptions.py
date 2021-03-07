# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.sub
:Synopsis:          This module includes functions that handle tags within a Khoros Community environment
:Usage:             ``from khoros.objects import subscriptions``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     06 Mar 2021
"""

from .. import api, errors
from ..utils import core_utils, log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def subscribe_user_to_node(khoros_object, node_id, node_type='board', user_id=None, user_email=None, user_login=None,
                           user_sso_id=None):
    # TODO: Add docstring
    if node_type not in ['board', 'category', 'grouphub']:
        raise errors.exceptions.InvalidNodeTypeError(val=node_type)
    user_api_path = api.get_v1_user_path(user_id, user_email, user_login, user_sso_id)
    node_collection = api.get_v1_node_collection(node_type)
    # TODO: Finish the function
    return

