# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.handlers
:Synopsis:          Functions that handle various error situations within the namespace
:Usage:             ``from khoros.errors import handlers``
:Example:           ``error_msg = handlers.get_error_from_html(html_string)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Mar 2020
"""

import re
import sys


def eprint(*args, **kwargs):
    """This function behaves the same as the ``print()`` function but is leveraged to print errors to ``sys.stderr``."""
    print(*args, file=sys.stderr, **kwargs)
    return


def get_error_from_html(html_error):
    """This function parses an error message from Khoros displayed in HTML format.

    :param html_error: The raw HTML returned via the :py:mod:`requests` module
    :type html_error: str
    :returns: The concise error message parsed from the HTML
    """
    error_title = re.sub(r'</h1>.*$', r'', re.sub(r'^.*<body><h1>', r'', html_error))
    error_description = re.sub(r'</u>.*$', r'', re.sub(r'^.*description</b>\s*<u>', r'', html_error))
    return f"{error_title}{error_description}"
