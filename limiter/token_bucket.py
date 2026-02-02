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
# token_bucket MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
from limiter.base import BaseRateLimiter
from protocol.request import Request
from protocol.response import RateLimitDecision
from state.bucket import TokenBucketState
from concurrency.clock import Clock, SystemClock
from concurrency.locks import LockManager
from state.repository import BucketRepository
from config.settings import RateLimitConfig


# --------------------------------------------------
# token bucket limiter
# --------------------------------------------------
class TokenBucketLimiter(BaseRateLimiter):
    def __init__(
            self,
            repository: BucketRepository,
            lock_manager: LockManager,
            config: RateLimitConfig,
            clock: Clock = None,
        ):
        self._repo = repository
        self._locks = lock_manager
        self._config = config
        self._clock = clock or SystemClock()
    
    def allow(self, request: Request) -> RateLimitDecision:
        key = request.client_id
        now = self._clock.now()

        self._locks.acquire(key)
        try:
            bucket = self._repo.get(key)
            if bucket is None:
                bucket = TokenBucketState(
                    capacity=self._config.capacity,
                    refill_rate=self._config.refill_rate,
                    current_tokens=self._config.capacity,
                    last_refill_timestamp=now,
                )
            
            bucket.refill(now)

            if bucket.consume(1):
                self._repo.save(key, bucket)
                return RateLimitDecision(
                    allowed=True,
                    remaining=int(bucket.current_tokens),
                )
            
            retry_after = (1 / self._config.refill_rate)
            self._repo.save(key, bucket)
            return RateLimitDecision(
                allowed=False,
                remaining=int(bucket.current_tokens),
                retry_after=retry_after,
            )
        finally:
            self._locks.release(key)
