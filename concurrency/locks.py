# --------------------------------------------------
# -*- Python -*- Compatibility Header
#
# Copyright (C) 2023 Developer Jarvis (Pen Name)
#
# This file is part of the API Rate Limiter Library. This library is free
# software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# API Rate Limiter - Implement token-bucket or leaky-bucket algorithm
#           Skills: algorithms, concurrency, API design
#
# Author: Developer Jarvis (Pen Name)
# Contact: https://github.com/DeveloperJarvis
#
# --------------------------------------------------

# --------------------------------------------------
# locks MODULE
# --------------------------------------------------
"""
Lock management for concurrency control.

Deisgn goal:
- One lock per client bucket
- Avoid global contention
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
import threading
from collections import defaultdict


# --------------------------------------------------
# lock manager
# --------------------------------------------------
class LockManager:
    """
    Manages locks keyed by client ID.

    Ensures serialized  access to per-client bucket
    state without introducing global locks.
    """

    def __init__(self):
        self._locks = defaultdict(threading.Lock)
        self._manager_lock = threading.Lock()
    
    def acquire(self, key: str):
        """
        Aquire lock for a given key
        """
        with self._manager_lock:
            lock = self._locks[key]
        
        lock.acquire()
    
    def release(self, key: str):
        """
        Release lock for a given key
        """
        lock = self._locks.get(key)
        if lock:
            lock.release()
