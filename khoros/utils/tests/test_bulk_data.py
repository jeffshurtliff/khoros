# -*- coding: utf-8 -*-
"""
:Module:         khoros.utils.tests.test_bulk_data
:Synopsis:       This module is used by pytest to test the Bulk Data API module
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  13 Mar 2022
"""

from . import resources


def test_base_url_without_helper():
    # Test without parameters
    base_url = bulk_data.get_base_url()
    assert base_url == 'https://api.lithium.com/lsi-data/v2/data/export/community/'

    # Test European URL
    base_url = bulk_data.get_base_url(europe=True)
    assert base_url == 'https://eu.api.lithium.com/lsi-data/v2/data/export/community/'

    # Test with explicitly defined Community ID
    amer_base_url = bulk_data.get_base_url(community_id='something.prod')
    eu_base_url = bulk_data.get_base_url(community_id='something.prod', europe=True)
    assert amer_base_url == 'https://api.lithium.com/lsi-data/v2/data/export/community/something.prod'
    assert eu_base_url == 'https://eu.api.lithium.com/lsi-data/v2/data/export/community/something.prod'


# Import modules and initialize the core object
bulk_data, exceptions = resources.import_modules('khoros.bulk_data', 'khoros.errors.exceptions')
