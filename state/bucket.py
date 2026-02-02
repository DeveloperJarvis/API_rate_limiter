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
# bucket MODULE
# --------------------------------------------------
"""
Bucket state is intentionally dumb.

Concurrency control is handled outside
(via LockManager or atomic store ops).
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
from dataclasses import dataclass


# --------------------------------------------------
# token bucket state
# --------------------------------------------------
@dataclass
class TokenBucketState:
    """
    Mutable token bucket state.
    """
    
    capacity: int
    refill_rate: float  # tokens per second
    current_tokens: float
    last_refill_timestamp: float

    def refill(self, now: float) -> None:
        """
        Refill tokens based on elapsed time.
        """
        elapsed = now - self.last_refill_timestamp
        if elapsed <= 0:
            return
        
        added_tokens = elapsed * self.refill_rate
        self.current_tokens = min(
            self.capacity,
            self.current_tokens + added_tokens
        )
        self.last_refill_timestamp = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens.
        """
        if self.current_tokens >= tokens:
            self.current_tokens -= tokens
            return True
        return False
