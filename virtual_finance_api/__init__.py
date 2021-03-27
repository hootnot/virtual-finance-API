"""Top-level package for Virtual Finance API."""

import logging
from .client import Client  # noqa F401
from .exceptions import VirtualFinanceAPIError  # noqa F401


__author__ = """Feite Brekeveld"""
__email__ = 'f.brekeveld@gmail.com'
__version__ = '0.2.1'

# Version synonym
VERSION = __version__

# Set default logging handler to avoid "No handler found" warnings.
try:
    from logging import NullHandler

except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

__all__ = (
    'Client',
    'VirtualFinanceAPIError'
)
