# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_communities
:Synopsis:          This module is used by pytest to verify that the communities module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     26 Sep 2022
"""

import os
import sys

import pytest

from . import resources

# Define a global variable to define when the package path has been set
package_path_defined = False


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list.

    .. versionadded:: 5.1.0
    """
    global package_path_defined
    if not package_path_defined:
        sys.path.insert(0, os.path.abspath('../..'))
        package_path_defined = True


