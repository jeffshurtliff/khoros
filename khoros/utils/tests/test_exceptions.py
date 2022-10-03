# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.tests.test_exceptions
:Synopsis:          This module is used by pytest to verify that the exceptions can be raised properly
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Oct 2022
"""

import pytest

from . import resources
from ...errors import exceptions


def test_raising_exceptions():
    """This function tests that exceptions are raised successfully.

    .. versionadded:: 5.1.2
    """
    with pytest.raises(exceptions.InvalidStructureTypeError):
        raise exceptions.InvalidStructureTypeError()

    with pytest.raises(exceptions.InvalidStructureTypeError):
        raise exceptions.InvalidStructureTypeError(val='testing')

