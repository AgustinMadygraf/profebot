"""
Path: utils/logging/dependency_injection.py
Simplified dependency injection for logging.
Provides access to loggers without complex configuration.
"""

import sys
from utils.logging.simple_logger import get_logger, set_verbose, is_verbose, initialize

# Initialize logging before anything else
initialize()

# Get command line arguments
verbose_mode = "--verbose" in sys.argv
no_colors = "--no-colors" in sys.argv

# Configure verbose mode based on command line arguments
set_verbose(verbose_mode)

# Get a logger for this module
_logger = get_logger("dependency_injection")

# Log initialization information
if verbose_mode:
    _logger.debug("[VERBOSE] Verbose mode enabled from command line arguments")
else:
    _logger.info("[INFO] Standard logging mode (use --verbose for debug messages)")

# Import and configure CLI interface for colors
try:
    from src.cli.interface import set_colors, set_verbose as cli_set_verbose
    set_colors(not no_colors)
    cli_set_verbose(verbose_mode)

    if no_colors:
        _logger.info("[INFO] Color output disabled (--no-colors)")
except ImportError:
    _logger.debug("CLI interface not available - color settings not applied")

# For backward compatibility with any code that might use these
def get_debug_verbose():
    """For backward compatibility"""
    return is_verbose()

def set_debug_verbose(enabled=True):
    """For backward compatibility"""
    set_verbose(enabled)

def log_debug(message, *args, **kwargs):
    """For backward compatibility"""
    get_logger().debug(message, *args, **kwargs)

# Export public functions
__all__ = ['get_logger', 'set_verbose', 'is_verbose']
