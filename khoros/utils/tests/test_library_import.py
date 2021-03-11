# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_library_import
:Synopsis:       This module is used by pytest to verify that the primary package can be imported successfully
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  11 Mar 2021
"""

import os
import sys


def set_package_path():
    """This function adds the high-level khoros directory to the sys.path list."""
    sys.path.insert(0, os.path.abspath('../..'))
    return


# Test importing the primary khoros package
def import_pkg_operation():
    """This function imports the primary package and returns ``True`` when successful."""
    import khoros
    return True


# Verify that the overall package can be successfully imported
def test_library_import():
    """This function tests to confirm that the primary package can be imported successfully."""
    set_package_path()
    assert import_pkg_operation() is True       # nosec
