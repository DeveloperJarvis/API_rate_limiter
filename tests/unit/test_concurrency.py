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
# test_concurrency MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import threading
from concurrency.locks import LockManager


def test_lock_manager_serializes_access():
    locks = LockManager()
    key = "client_x"
    counter = 0

    def critical_section():
        nonlocal counter
        locks.acquire(key)
        try:
            tmp = counter
            counter = tmp + 1
        finally:
            locks.release(key)
    
    threads = [threading.Thread(target=critical_section)
               for _ in range(50)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert counter == 50
