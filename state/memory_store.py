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
# memory_store MODULE
# --------------------------------------------------
"""
In-memory bucket repository.

Used for:
- Single-instance deployments
- Tests
- Local development
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
from typing import Dict, Optional
from state.bucket import TokenBucketState
from state.repository import BucketRepository


# --------------------------------------------------
# in memory bucket repository
# --------------------------------------------------
class InMemoryBucketRepository(BucketRepository):
    def __init__(self):
        self._store: Dict[str, TokenBucketState] = {}
    
    def get(self, key: str) -> Optional[TokenBucketState]:
        return self._store.get(key)
    
    def save(self, key: str,
             bucket: TokenBucketState) -> None:
        self._store[key] = bucket
    
    def delete(self, key: str) -> None:
        self._store.pop(key, None)
