# -*- coding: utf-8 -*-
"""
:Module:            khoros.objects.saml
:Synopsis:          This module includes functions that relate to SAML SSO.
:Usage:             ``from khoros import saml``
:Example:           ``assertion = saml.import_assertion(file_path)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     26 Sep 2021
"""

from . import api, errors
from .utils import log_utils, core_utils

# Initialize the logger for this module
logger = log_utils.initialize_logging(__name__)


def send_assertion(khoros_object, assertion=None, file_path=None, base64_encode=True, url_encode=True):
    """This function sends a SAML assertion as a POST request in order to provision a new user.

    .. versionadded:: 4.3.0

    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros]
    :param assertion: The SAML assertion in string format and optionally base64- and/or URL-encoded
    :type assertion: str, None
    :param file_path: The file path to the XML file to import that contains the SAML assertion
    :type file_path: str, None
    :param base64_encode: Determines if the assertion should be base64-encoded (``True`` by default)
    :type base64_encode: bool
    :param url_encode: Determines if the assertion should be URL-encoded (``True`` by default)
    :type url_encode: bool
    :returns: The API response from the POST request
    :raises: :py:exc:`khoros.errors.exceptions.MissingRequiredDataError`
    """
    if not any((assertion, file_path)):
        error_msg = "A SAML assertion string or file path must be provided"
        raise errors.exceptions.MissingRequiredDataError(error_msg)
    if assertion:
        if _is_decoded(assertion) and base64_encode:
            assertion = core_utils.encode_base64(assertion, url_encode_object=url_encode)
        elif not _is_decoded(assertion) and '=' in assertion and url_encode:
            assertion = core_utils.url_encode(assertion)
    else:
        assertion = import_assertion(file_path, base64_encode, url_encode)
    uri = _get_api_uri(khoros_object)
    response = api.post_request_with_retries(uri, url_encoded_payload=assertion, return_json=False,
                                             khoros_object=khoros_object)
    return response


def import_assertion(file_path, base64_encode=True, url_encode=True):
    """This function imports an XML SAML assertion as a string and optionally base64- and/or URL-encodes it.

    .. versionadded:: 4.3.0

    :param file_path: The file path to the XML file to import
    :type file_path: str
    :param base64_encode: Determines if the assertion should be base64-encoded (``True`` by default)
    :type base64_encode: bool
    :param url_encode: Determines if the assertion should be URL-encoded (``True`` by default)
    :type url_encode: bool
    :returns: The SAML assertion string
    :raises: :py:exc:`FileNotFoundError`
    """
    with open(file_path, 'r') as file:
        assertion = file.read()
    if base64_encode:
        assertion = core_utils.encode_base64(assertion)
    if url_encode:
        assertion = core_utils.url_encode(assertion)
    return assertion


def _is_decoded(_assertion):
    """This function checks to see if a SAML assertion is base64- or url-encoded.

    .. versionadded:: 4.3.0

    :param _assertion: The SAML assertion string to be examined
    :type _assertion: str
    :returns: Boolean value indicating whether or not the SAML assertion string is encoded
    :raises: :py:exc:`TypeError`
    """
    return True if '<saml' in _assertion else False


def _get_api_uri(_khoros_object):
    """This function retrieves the API URI to call in the POST request.

    .. versionadded:: 4.3.0

    :param _khoros_object: The core :py:class:`khoros.Khoros` object
    :type _khoros_object: class[khoros.Khoros]
    :returns: The absolute URI to be used in the POST request
    """
    _base_url = _khoros_object.core.get('base_url')
    _base_url = _base_url[:-1] if _base_url.endswith('/') else _base_url
    return _base_url + '/auth/saml/login?SAMLResponse'
