# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_communities
:Synopsis:          This module is used by pytest to verify that the ``communities`` module functions properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     29 Sep 2022
"""

import os
import sys

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


def test_community_details():
    """This function tests the ability to retrieve community details.

    .. versionchanged:: 5.1.1
       The function has been updated to support GitHub Workflows control data.

    .. versionadded:: 5.1.0
    """
    # Retrieve the control data
    control_data = resources.get_control_data('communities')

    # Instantiate the Khoros object
    set_package_path()
    khoros_object = resources.get_core_object()

    # Test retrieving the community title
    title = khoros_object.communities.get_title()
    assert title == control_data.get('community_title')

    # Test retrieving the community description
    description = khoros_object.communities.get_description()
    assert description == control_data.get('description')

    # Test retrieving the tenant ID
    tenant_id = khoros_object.communities.get_tenant_id()
    assert tenant_id == control_data.get('tenant_id')

    # Test retrieving the primary URL
    primary_url = khoros_object.communities.get_primary_url()
    assert primary_url == control_data.get('primary_url')

    # Test retrieving the sign-out URL
    sign_out_url = khoros_object.communities.get_sign_out_url()
    assert sign_out_url == control_data.get('sign_out_url')

    # Test retrieving the active skin
    active_skin = khoros_object.communities.get_active_skin()
    assert active_skin == control_data.get('active_skin')

    # Test retrieving the community language
    language = khoros_object.communities.get_language()
    assert language == control_data.get('language')

    # Test retrieving the date pattern
    date_pattern = khoros_object.communities.get_date_pattern()
    assert date_pattern == control_data.get('date_pattern')

    # Test retrieving the email confirmation requirement setting
    email_conf_req = khoros_object.communities.email_confirmation_required_to_post()
    assert email_conf_req == control_data.get('email_confirmation')

    # Test retrieving the friendly date setting
    friendly_date = khoros_object.communities.friendly_date_enabled()
    assert friendly_date == control_data.get('friendly_date')

    # Test retrieving the community creation date
    creation_date = khoros_object.communities.get_creation_date()
    assert creation_date == control_data.get('creation_date')

    # Test retrieving the friendly date max age
    friendly_max_age = khoros_object.communities.get_friendly_date_max_age()
    assert friendly_max_age == control_data.get('friendly_max_age')

    # Test retrieving the maximum attachments
    max_attachments = khoros_object.communities.get_max_attachments()
    assert max_attachments == control_data.get('max_attachments')

    # Test retrieving the permitted attachment types
    attachments = khoros_object.communities.get_permitted_attachment_types()
    assert isinstance(attachments, list) and 'jpg' in attachments

    # TODO: Test retrieving Ooyala Player branding ID

    # TODO: Test retrieving top-level breadcrumb setting

    # TODO: Test retrieving show community node in breadcrumb setting

    # TODO: Test retrieving top-level categories enabled setting

    # TODO: Test retrieving top-level categories on community page setting

