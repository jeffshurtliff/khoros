# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_categories
:Synopsis:          This module is used by pytest to verify that the ``categories`` module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     27 Sep 2022
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


def get_core_object():
    """This function instantiates and returns the core object using a local helper file.

    .. versionadded:: 5.1.0
    """
    if not resources.local_test_config_exists() or not resources.local_helper_exists():
        pytest.skip('skipping local-only tests')

    # Instantiate the Khoros object
    set_package_path()
    khoros_object = resources.instantiate_with_local_helper(production=False)
    return khoros_object


def get_control_data():
    """This function retrieves the control data used in various tests.

    .. versionadded:: 5.1.0
    """
    if not resources.control_data_exists('categories'):
        pytest.skip('skipping tests where control data is unavailable')

    # Import the control data
    control_data = resources.import_control_data('categories')

    # Return the control data and the core object
    return control_data


def test_get_category_id():
    """This function tests the ability to get a category ID from a URL.

    .. versionadded:: 5.1.0
    """
    # Get the control data and core object
    control_data, khoros_object = get_control_data(), get_core_object()

    # Test retrieving the category ID from an example URL
    category_id = khoros_object.categories.get_category_id(control_data.get('url'))
    assert category_id == control_data.get('id')


def test_total_count():
    """This function tests the ability to retrieve the total category count.

    .. versionadded:: 5.1.0
    """
    # Instantiate the core object
    khoros_object = get_core_object()

    # Test retrieving the total category count
    total_count = khoros_object.categories.get_total_count()
    assert isinstance(total_count, int) and total_count > 0


def test_if_category_exists():
    """This function tests if the existence of categories can be successfully determined.

    .. versionadded:: 5.1.0
    """
    # Get the control data and core object
    control_data, khoros_object = get_control_data(), get_core_object()

    # Test both methods
    exists_by_id = khoros_object.categories.category_exists(category_id=control_data.get('id'))
    exists_by_url = khoros_object.categories.category_exists(category_url=control_data.get('url'))
    assert exists_by_id is True and exists_by_url is True


def test_category_details():
    """This function tests the retrieval of various category details.

    .. versionadded:: 5.1.0
    """
    # Get the control data and core object
    control_data, khoros_object = get_control_data(), get_core_object()

    # Test retrieval of URL
    url = khoros_object.categories.get_url(control_data.get('id'))
    assert url == control_data.get('url')

    # Test retrieval of title
    title = khoros_object.categories.get_title(control_data.get('id'))
    assert title == control_data.get('title')

    # Test retrieval of description
    desc = khoros_object.categories.get_description(control_data.get('id'))
    assert desc == control_data.get('description')

    # TODO: Test retrieval of get_parent_type()

    # TODO: Test retrieval of get_parent_id()

    # TODO: Test retrieval of get_parent_url()

    # TODO: Test retrieval of get_root_type()

    # TODO: Test retrieval of get_root_id()

    # TODO: Test retrieval of get_root_url()

    # Test retrieval of language
    language = khoros_object.categories.get_language(control_data.get('id'))
    assert language == control_data.get('language')

    # Test retrieval of hidden setting
    hidden = khoros_object.categories.is_hidden(control_data.get('id'))
    assert hidden == control_data.get('hidden')

    # Test retrieval of views
    views = khoros_object.categories.get_views(control_data.get('id'))
    assert isinstance(views, int) and views > 0

    # Test retrieval of friendly date enabled setting
    friendly_date = khoros_object.categories.friendly_date_enabled(control_data.get('id'))
    assert friendly_date == control_data.get('friendly_date')

    # TODO: Test retrieval of friendly date max age

    # Test retrieval of active skin
    active_skin = khoros_object.categories.get_active_skin(control_data.get('id'))
    assert active_skin == control_data.get('active_skin')

    # Test retrieval of depth
    depth = khoros_object.categories.get_depth(control_data.get('id'))
    assert isinstance(depth, int)

    # Test retrieval of position
    position = khoros_object.categories.get_position(control_data.get('id'))
    assert isinstance(position, int)

    # TODO: Test retrieval of get_creation_date()
