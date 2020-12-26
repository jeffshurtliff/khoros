# -*- coding: utf-8 -*-
"""
:Module:            khoros.errors.translations
:Synopsis:          Provides more relevant translations for error messages in API responses where possible
:Usage:             ``from khoros.errors import translations``
:Example:           ``error_msg = translations.translate_error(error_msg, khoros_object)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     26 Dec 2020
"""

ERROR_TRANSLATIONS = {
    'page.post.error.attachment_bad_extension':
        'The attachment does not have an extension permitted in Community Admin > System > File Attachments'
}


def translate_error(error_msg, khoros_object=None, translate_errors=True):
    """This function translates API response errors into more relevant messages where possible and permitted.

    :param error_msg: The original error message
    :type error_msg: str
    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None
    :param translate_errors: Defines if errors can be transmitted (``True`` by default) even with no core object
    :type translate_errors: bool
    :return:
    """
    if translation_enabled(translate_errors, khoros_object):
        error_msg = parse_message(error_msg)
        if error_msg in ERROR_TRANSLATIONS:
            error_msg = ERROR_TRANSLATIONS.get(error_msg)
    return error_msg


def translation_enabled(translate_errors=True, khoros_object=None):
    """This function identifies whether or not error translation is permitted.

    .. versionchanged:: 3.3.0
       Updated ``khoros_object._settings`` to be ``khoros_object.core_settings``.

    :param translate_errors: Defines if errors can be transmitted (``True`` by default) even with no core object
    :type translate_errors: bool
    :param khoros_object: The core :py:class:`khoros.Khoros` object
    :type khoros_object: class[khoros.Khoros], None
    :returns: Boolean value defining if translation is enabled
    """
    if khoros_object and 'translate_errors' in khoros_object.core_settings:
        translate_errors = khoros_object.core_settings.get('translate_errors')
    return translate_errors


def parse_message(error_msg):
    """This function parses error messages when necessary to prepare them for translation.

    :param error_msg: The original error message
    :type error_msg: str
    :returns: The prepared error message
    """
    split_sequences = ['\n', '\r']
    for sequence in split_sequences:
        if sequence in error_msg:
            error_msg = error_msg.split(sequence)[0]
            break
    return error_msg
