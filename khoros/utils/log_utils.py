# -*- coding: utf-8 -*-
"""
:Module:            khoros.utils.log_utils
:Synopsis:          Collection of logging utilities and functions
:Usage:             ``from khoros.utils import log_utils``
:Example:           ``logger = log_utils.initialize_logging(__name__)``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     08 Jan 2021
"""

import os
import sys
import logging
import logging.handlers
from pathlib import Path

LOGGING_DEFAULTS = {
    'logger_name': __name__,
    'log_level': 'info',
    'formatter': logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'),
    'date_format': '%Y-%m-%d %I:%M:%S',
}
HANDLER_DEFAULTS = {
    'file_log_level': 'info',
    'console_log_level': 'warning',
    'syslog_log_level': 'info',
    'syslog_address': 'localhost',
    'syslog_port': 514,
}


def initialize_logging(logger_name=None, log_level=None, formatter=None, debug=None, no_output=None, file_output=None,
                       file_log_level=None, log_file=None, overwrite_log_files=None, console_output=None,
                       console_log_level=None, syslog_output=None, syslog_log_level=None, syslog_address=None,
                       syslog_port=None):
    # TODO: Add docstring
    logger_name, log_levels, formatter = _apply_defaults(logger_name, formatter, debug, log_level, file_log_level,
                                                         console_log_level, syslog_log_level)
    log_level, file_log_level, console_log_level, syslog_log_level = _get_log_levels_from_dict(log_levels)
    logger = logging.getLogger(logger_name)
    logger = _set_logging_level(logger, log_level)
    logger = _add_handlers(logger, formatter, no_output, file_output, file_log_level, log_file, overwrite_log_files,
                           console_output, console_log_level, syslog_output, syslog_log_level, syslog_address,
                           syslog_port)
    return logger


class LessThanFilter(logging.Filter):
    """This class allows filters to be set to limit log levels to only less than a specified level.

    .. versionadded:: 3.0.0

    .. seealso:: `Zoey Greer <https://stackoverflow.com/users/5124424/zoey-greer>`_ is the original author of
                 this class which was provided on `Stack Overflow <https://stackoverflow.com/a/31459386>`_.
    """
    def __init__(self, exclusive_maximum, name=""):
        """This method instantiates the :py:class:`khoros.utils.log_utils.LessThanFilter` class object.

        .. versionadded:: 3.0.0
        """
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        """This method returns a Boolean integer value indicating whether or not a message should be logged.

        .. versionadded:: 3.0.0

        .. note:: A non-zero return indicates that the message will be logged.
        """
        return 1 if record.levelno < self.max_level else 0


def _apply_defaults(_logger_name, _formatter, _debug, _log_level, _file_level, _console_level, _syslog_level):
    """This function applies default values to the configuration settings if not explicitly defined.

    .. versionadded:: 3.0.0

    :param _logger_name: The name of the logger instance
    :type _logger_name: str, None
    :param _formatter: The log format to utilize for the logger instance
    :type _formatter: str, None
    :param _debug: Defines if debug mode is enabled
    :type _debug: bool, None
    :param _log_level: The general logging level for the logger instance
    :type _log_level: str, None
    :returns: The values that will be used for the configuration settings
    """
    _log_levels = {
        'general': _log_level,
        'file': _file_level,
        'console': _console_level,
        'syslog': _syslog_level,
    }
    _logger_name = LOGGING_DEFAULTS.get('logger_name') if not _logger_name else _logger_name
    if _debug:
        for _log_type in _log_levels:
            _log_levels[_log_type] = 'debug'
    else:
        if _log_level:
            for _lvl_type, _lvl_value in _log_levels.items():
                if _lvl_type != 'general' and _lvl_value is None:
                    _log_levels[_lvl_type] = _log_level
        else:
            _log_level = LOGGING_DEFAULTS.get('log_level')
    if _formatter and isinstance(_formatter, str):
        _formatter = logging.Formatter(_formatter)
    _formatter = LOGGING_DEFAULTS.get('formatter') if not _formatter else _formatter
    return _logger_name, _log_levels, _formatter


def _get_log_levels_from_dict(_log_levels):
    """This function returns the individual log level values from a dictionary.

    .. versionadded:: 3.0.0

    :param _log_levels: Dictionary containing log levels for different handlers
    :type _log_levels: dict
    :returns: Individual string values for each handler
    """
    _general = _log_levels.get('general')
    _file = _log_levels.get('file')
    _console = _log_levels.get('console')
    _syslog = _log_levels.get('syslog')
    return _general, _file, _console, _syslog


def _set_logging_level(_logger, _log_level):
    """This function sets the logging level for a :py:class:`logging.Logger` instance.

    .. versionadded:: 3.0.0

    :param _logger: The :py:class:`logging.Logger` instance
    :type _logger: Logger
    :param _log_level: The log level as a string (``debug``, ``info``, ``warning``, ``error`` or ``critical``)
    :type _log_level: str
    :returns: The :py:class:`logging.Logger` instance with a logging level set where applicable
    """
    if _log_level == 'debug':
        _logger.setLevel(logging.DEBUG)
    elif _log_level == 'info':
        _logger.setLevel(logging.INFO)
    elif _log_level == 'warning':
        _logger.setLevel(logging.WARNING)
    elif _log_level == 'error':
        _logger.setLevel(logging.ERROR)
    elif _log_level == 'critical':
        _logger.setLevel(logging.CRITICAL)
    return _logger


def _add_handlers(_logger, _formatter, _no_output, _file_output, _file_log_level, _log_file, _overwrite_log_files,
                  _console_output, _console_log_level, _syslog_output, _syslog_log_level, _syslog_address,
                  _syslog_port):
    # TODO: Add docstring
    if _no_output or not any((_file_output, _console_output, _syslog_output)):
        _logger.addHandler(logging.NullHandler())
    else:
        if _file_output:
            # Add the FileHandler to the Logger object
            _logger = _add_file_handler(_logger, _file_log_level, _log_file, _overwrite_log_files, _formatter)
        if _console_output:
            # Add the StreamHandler to the Logger object
            _logger = _add_stream_handler(_logger, _console_log_level, _formatter)
        if _syslog_output:
            # Add the SyslogHandler to the Logger object
            _logger = _add_syslog_handler(_logger, _syslog_log_level, _formatter, _syslog_address, _syslog_port)
    return _logger


def _add_file_handler(_logger, _log_level, _log_file, _overwrite, _formatter):
    """This function adds a :py:class:`logging.FileHandler` to the :py:class:`logging.Logger` instance.

    .. versionadded:: 3.0.0

    :param _logger: The :py:class:`logging.Logger` instance
    :type _logger: Logger
    :param _log_level: The log level to set for the handler
    :type _log_level: str
    :param _log_file: The log file (as a file name or a file path) to which messages should be written

    .. note:: If a file path isn't provided then the default directory is the home directory of the user instantiating
              the :py:class:`logging.Logger` object. If a file name is also no provided then it will default to
              using ``khoros.log`` as the file name.

    :param _overwrite: Determines if messages should be appended to the file (default) or overwrite it
    :type _overwrite: bool
    :param _formatter: The :py:class:`logging.Formatter` to apply to messages passed through the handler
    :type _formatter: Formatter
    :returns: The :py:class:`logging.Logger` instance with the added :py:class:`logging.FileHandler`
    """
    # Define the log file to use
    _home_dir = str(Path.home())
    if _log_file:
        if not any((('/' in _log_file), ('\\' in _log_file))):
            _log_file = os.path.join(_home_dir, _log_file)
    else:
        _log_file = os.path.join(_home_dir, 'khoros.log')

    # Identify if log file should be overwritten
    _write_mode = 'w' if _overwrite else 'a'

    # Instantiate the handler
    _handler = logging.FileHandler(_log_file, _write_mode)
    _log_level = HANDLER_DEFAULTS.get('file_log_level') if not _log_level else _log_level
    _handler = _set_logging_level(_handler, _log_level)
    _handler.setFormatter(_formatter)

    # Add the handler to the logger
    _logger.addHandler(_handler)
    return _logger


def _add_stream_handler(_logger, _log_level, _formatter):
    """This function adds a :py:class:`logging.StreamHandler` to the :py:class:`logging.Logger` instance.

    .. versionadded:: 3.0.0

    :param _logger: The :py:class:`logging.Logger` instance
    :type _logger: Logger
    :param _log_level: The log level to set for the handler
    :type _log_level: str
    :param _formatter: The :py:class:`logging.Formatter` to apply to messages passed through the handler
    :type _formatter: Formatter
    :returns: The :py:class:`logging.Logger` instance with the added :py:class:`logging.StreamHandler`
    """
    _log_level = HANDLER_DEFAULTS.get('console_log_level') if not _log_level else _log_level
    _stdout_levels = ['DEBUG', 'INFO']
    if _log_level.upper() in _stdout_levels:
        _logger = _add_split_stream_handlers(_logger, _log_level, _formatter)
    else:
        _handler = logging.StreamHandler()
        _handler = _set_logging_level(_handler, _log_level)
        _handler.setFormatter(_formatter)
        _logger.addHandler(_handler)
    return _logger


def _add_split_stream_handlers(_logger, _log_level, _formatter):
    """This function splits messages into q ``stdout`` or ``stderr`` handler depending on the log level.

    .. versionadded:: 3.0.0

    .. seealso:: Refer to the documentation for the :py:class:`khoros.utils.log_utils.LessThanFilter` for
                 more information on how this filtering is implemented and for credit to the original author.

    :param _logger: The :py:class:`logging.Logger` instance
    :type _logger: Logger
    :param _log_level: The log level provided for the stream handler (i.e. console output)
    :type _log_level: str
    :param _formatter: The :py:class:`logging.Formatter` to apply to messages passed through the handlers
    :type _formatter: Formatter
    :returns: The logger instance with the two handlers added
    """
    # Configure and add the STDOUT handler
    _stdout_handler = logging.StreamHandler(sys.stdout)
    _stdout_handler = _set_logging_level(_stdout_handler, _log_level)
    _stdout_handler.addFilter(LessThanFilter(logging.WARNING))
    _stdout_handler.setFormatter(_formatter)
    _logger.addHandler(_stdout_handler)

    # Configure and add the STDERR handler
    _stderr_handler = logging.StreamHandler(sys.stderr)
    _stderr_handler.setLevel(logging.WARNING)
    _stderr_handler.setFormatter(_formatter)
    _logger.addHandler(_stderr_handler)

    # Return the logger with the added handlers
    return _logger


def _add_syslog_handler(_logger, _log_level, _formatter, _address, _port):
    # TODO: Add docstring
    _log_level = HANDLER_DEFAULTS.get('syslog_log_level') if not _log_level else _log_level
    _address = HANDLER_DEFAULTS.get('syslog_address') if not _address else _address
    _port = HANDLER_DEFAULTS.get('syslog_port') if not _port else _port
    _handler = logging.handlers.SysLogHandler(address=(_address, _port))
    _handler = _set_logging_level(_handler, _log_level)
    _handler.setFormatter(_formatter)
    _logger.addHandler(_handler)
    return _logger
