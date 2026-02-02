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
# manager MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
from typing import Dict
from limiter.token_bucket import TokenBucketLimiter
from limiter.leaky_bucket import LeakyBucketLimiter
from concurrency.locks import LockManager
from state.memory_store import InMemoryBucketRepository
from config.settings import RateLimitConfig
from protocol.request import Request
from protocol.response import RateLimitDecision


# --------------------------------------------------
# rate limit manager
# --------------------------------------------------
class RateLimitManager:
    """
    Entry point for rate limiting decisions.
    """

    def __init__(self):
        self._lock_manager = LockManager()
        self._repository = InMemoryBucketRepository()
        self._limiters: Dict[str, object] = {}
    
    def register_leaky_bucket(
            self, key: str, config: RateLimitConfig
        ):
        self._limiters[key] = LeakyBucketLimiter(
            self._repository,
            self._lock_manager,
            config,
        )
    
    def register_token_bucket(
            self,
            key: str,
            config: RateLimitConfig,
            clock=None,
        ):
        self._limiters[key] = TokenBucketLimiter(
            self._repository,
            self._lock_manager,
            config,
            clock=clock,
        )
    
    def allow_request(
            self, request: Request
        ) -> RateLimitDecision:
        limiter = self._limiters.get(request.client_id)
        if not limiter:
            return RateLimitDecision(
                allowed=True, remaining=0
            )
        
        return limiter.allow(request)
