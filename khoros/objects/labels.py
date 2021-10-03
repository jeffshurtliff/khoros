# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.labels
:Synopsis:          This module includes functions that handle labels within a Khoros Community environment
:Usage:             ``from khoros.objects import labels``
:Example:           TBD
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Sep 2021
"""

from .. import api, liql, errors
from ..utils import log_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)
