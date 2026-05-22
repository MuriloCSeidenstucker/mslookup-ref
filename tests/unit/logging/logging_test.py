# pylint: disable=E0601:used-before-assignment

import json
import logging
import sys
from unittest.mock import MagicMock

from src.logging.formatter import JsonFormatter
from src.logging.logger_handler import LevelName, LoggerHandler


def test_json_formatter_format_normal():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path.py",
        lineno=10,
        msg="Hello %s",
        args=("World",),
        exc_info=None,
    )
    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert data["level"] == "INFO"
    assert data["message"] == "Hello World"
    assert data["stacktrace"] is None
    assert "timestamp" in data
    assert "module" in data


def test_json_formatter_format_exception():
    formatter = JsonFormatter()
    try:
        raise ValueError("Simulated Exception")
    except ValueError:
        exc_info = sys.exc_info()

    record = logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname="test_path.py",
        lineno=20,
        msg="Failed due to error",
        args=(),
        exc_info=exc_info,
    )

    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert data["level"] == "ERROR"
    assert data["message"] == "Failed due to error"
    assert data["stacktrace"] is not None
    assert "ValueError: Simulated Exception" in data["stacktrace"]


def test_logger_handler_sets_level_and_handlers(mocker):
    mocker.patch("src.logging.logger_handler.os.makedirs")
    mock_file_handler_cls = mocker.patch("src.logging.logger_handler.FileHandler")
    mock_stream_handler_cls = mocker.patch(
        "src.logging.logger_handler.logging.StreamHandler"
    )
    mock_get_logger = mocker.patch("src.logging.logger_handler.logging.getLogger")

    mock_logger = MagicMock()
    mock_logger.hasHandlers.return_value = False
    mock_get_logger.return_value = mock_logger

    mock_file_handler = MagicMock()
    mock_file_handler_cls.return_value = mock_file_handler

    mock_stream_handler = MagicMock()
    mock_stream_handler_cls.return_value = mock_stream_handler

    handler = LoggerHandler(LevelName.WARNING)
    logger = handler.get_logger()

    assert logger == mock_logger
    mock_logger.setLevel.assert_called_once_with(logging.WARNING)
    mock_logger.addHandler.assert_any_call(mock_file_handler)
    mock_logger.addHandler.assert_any_call(mock_stream_handler)


def test_logger_handler_does_not_duplicate_handlers(mocker):
    mocker.patch("src.logging.logger_handler.os.makedirs")
    mock_get_logger = mocker.patch("src.logging.logger_handler.logging.getLogger")

    mock_logger = MagicMock()
    mock_logger.hasHandlers.return_value = True
    mock_get_logger.return_value = mock_logger

    handler = LoggerHandler(LevelName.DEBUG)
    logger = handler.get_logger()

    assert logger == mock_logger
    mock_logger.setLevel.assert_not_called()
    mock_logger.addHandler.assert_not_called()
