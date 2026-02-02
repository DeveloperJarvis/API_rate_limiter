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
# settings MODULE
# --------------------------------------------------
"""
Purpose: Immutable, validated rate-limit configuration.
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
from dataclasses import dataclass
from config.constants import (
    DEFAULT_CAPACITY,
    DEFAULT_REFILL_RATE
)


# --------------------------------------------------
# rate limit config
# --------------------------------------------------
@dataclass(frozen=True)
class RateLimitConfig:
    """
    Configuration for a rate limiter bucket.

    capacity:
        Maximum tokens (or queue size)
    
    refill_rate:
        Tokens added per second (Token Bucket)
        OR
        Requests drained per second (Leaky Bucket)
    """

    capacity: int = DEFAULT_CAPACITY
    refill_rate: float = DEFAULT_REFILL_RATE

    def __post_init__(self):
        if self.capacity <= 0:
            raise ValueError("capacity must be > 0")
        
        if self.refill_rate <= 0:
            raise ValueError("refill_rate must be > 0")
