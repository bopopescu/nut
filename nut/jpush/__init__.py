"""Python package for using the JPush API"""
from .core import JPush
from .common import JPushFailure, Unauthorized

<<<<<<< HEAD
__version__ = '3.0.2'
=======
__version__ = '3.0.1'
>>>>>>> 72e43586aba0244e68985f37dafbfd46d5a59172
VERSION = tuple(map(int,  __version__.split('.')))

from .push import (
    Push,
    all_,
    tag,
    tag_and,
    alias,
    registration_id,
    notification,
    ios,
    android,
    winphone,
    platform,
    audience,
    options,
    message,
)

<<<<<<< HEAD
from .device import (
    Device,
    add,
    remove,
    device_tag,
    device_alias,
    device_regid,
)

=======
>>>>>>> 72e43586aba0244e68985f37dafbfd46d5a59172
__all__ = [
    JPush,
    JPushFailure,
    Unauthorized,
    all_,
    Push,
    tag,
    tag_and,
    alias,
    registration_id,
    notification,
    ios,
    android,
    winphone,
    message,
    platform,
    audience,
    options,
<<<<<<< HEAD
    Device,
    add,
    remove,
    device_tag,
    device_alias,
    device_regid,
=======
>>>>>>> 72e43586aba0244e68985f37dafbfd46d5a59172
]

# Silence urllib3 INFO logging by default

import logging
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
