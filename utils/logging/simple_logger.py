"""
Simple logging module that only handles console output.
Provides basic logging functionality with control over debug messages via verbose mode.
"""

import logging
import sys
from typing import Dict

class LoggerConfig:
    " Configuration for the logging system "
    verbose_mode = False
    initialized = False

config = LoggerConfig()

# Cache of loggers to avoid creating multiple instances
_loggers: Dict[str, logging.Logger] = {}

# Simple console formatter
_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def set_verbose(enabled: bool = True) -> bool:
    """
    Enable or disable verbose mode (debug messages)
    
    Args:
        enabled: True to enable debug messages, False to disable
        verbose_mode: Current state of verbose mode
        
    Returns:
        Updated state of verbose mode
    """
    config.verbose_mode = enabled

    # Update all existing loggers
    root_level = logging.DEBUG if enabled else logging.INFO
    logging.getLogger().setLevel(root_level)

    for logger in _loggers.values():
        logger.setLevel(logging.DEBUG if enabled else logging.INFO)

        # Update handlers
        for handler in logger.handlers:
            if handler.level <= logging.INFO:  # Don't change ERROR handlers
                handler.setLevel(logging.DEBUG if enabled else logging.INFO)

    # Get a fresh logger for reporting
    logger = get_logger("logging_system")
    if enabled:
        logger.debug("Verbose mode enabled - debug messages will be displayed")
    else:
        logger.info("Standard mode - debug messages hidden (use --verbose to show them)")

def is_verbose() -> bool:
    """
    Check if verbose mode is enabled
    
    Returns:
        True if verbose mode is enabled, False otherwise
    """
    return config.verbose_mode
def _clear_handlers(logger: logging.Logger) -> None:
    """
    Remove all handlers from a logger
    
    Args:
        logger: Logger to clear handlers from
    """
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

def get_logger(name: str = "profebot") -> logging.Logger:
    """
    Get a configured logger by name
    
    Args:
        name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    global _loggers, VERBOSE_MODE, _initialized
    global _loggers, config
    # Ensure system is initialized
    if not _initialized:
        initialize()

    # Return cached logger if it exists
    if name in _loggers:
        return _loggers[name]

    # Create new logger
    logger = logging.getLogger(name)

    # Clear any existing handlers to avoid duplicates
    _clear_handlers(logger)

    # Set appropriate level based on verbose mode
    logger.setLevel(logging.DEBUG if VERBOSE_MODE else logging.INFO)
    logger.setLevel(logging.DEBUG if config.verbose_mode else logging.INFO)
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_formatter)
    handler.setLevel(logging.DEBUG if VERBOSE_MODE else logging.INFO)
    handler.setLevel(logging.DEBUG if config.verbose_mode else logging.INFO)

    # Avoid duplicate messages in root logger
    logger.propagate = False

    # Cache the logger
    _loggers[name] = logger
    return logger

def initialize() -> None:
    """
    Initialize the logging system with command line arguments
    """
    global _initialized, VERBOSE_MODE
    global config

    if config.initialized:
        return

    # Check if verbose mode is enabled via command line
    VERBOSE_MODE = "--verbose" in sys.argv
    config.verbose_mode = "--verbose" in sys.argv
    # Reset all existing loggers and handlers
    logging.root.handlers = []  # Remove all handlers from the root logger

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if VERBOSE_MODE else logging.INFO)
    root_logger.setLevel(logging.DEBUG if config.verbose_mode else logging.INFO)
    # Clear existing handlers
    _clear_handlers(root_logger)

    # Add console handler to root logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_formatter)
    handler.setLevel(logging.DEBUG if VERBOSE_MODE else logging.INFO)
    root_logger.addHandler(handler)

    # Mark as initialized
    _initialized = True
    config.initialized = True
    # Get the main app logger
    main_logger = get_logger("profebot")

    if VERBOSE_MODE:
        main_logger.debug("Verbose mode enabled - debug messages will be displayed")
