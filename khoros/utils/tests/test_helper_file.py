# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_helper_file
:Synopsis:       This module is used by pytest to verify that the helper configuration files work properly
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


def get_helper_path():
    """This function defines the appropriate path to the helper file."""
    if os.getenv('USERNAME') == 'shurtj' and sys.platform == 'win32':
        helper_path = f"{os.getenv('USERPROFILE')}\\Development\\khoros\\local\\"
    else:
        helper_path = f"{os.getenv('HOME')}/secrets/"
    return helper_path


def test_yaml_file():
    """This function tests the import of a YAML file."""
    # Import the package
    set_package_path()
    from khoros import Khoros

    # Define the full path to the helper file
    helper_path = get_helper_path()
    yaml_file = f"{helper_path}khoros_helper.yml"

    # Initialize the core object using the helper file
    khoros = Khoros(helper=yaml_file, auto_connect=False)

    # Verify that the helper configuration was imported successfully
    assert 'connection' in khoros._helper_settings      # nosec
