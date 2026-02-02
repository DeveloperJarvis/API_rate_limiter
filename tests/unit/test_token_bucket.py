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
# test_token_bucket MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import time

from limiter.token_bucket import TokenBucketLimiter
from config.settings import RateLimitConfig
from state.memory_store import InMemoryBucketRepository
from concurrency.locks import LockManager
from protocol.request import Request


def test_token_bucket_allows_burst_then_throttles():
    repo = InMemoryBucketRepository()
    locks = LockManager()
    config = RateLimitConfig(capacity=2, refill_rate=1)

    limiter = TokenBucketLimiter(repo, locks, config)
    req = Request(client_id="client", enpoint="/api")

    assert limiter.allow(req).allowed is True
    assert limiter.allow(req).allowed is True
    assert limiter.allow(req).allowed is False


def test_token_bucket_refills_over_time():
    repo = InMemoryBucketRepository()
    locks = LockManager()
    config = RateLimitConfig(capacity=1, refill_rate=1)

    limiter = TokenBucketLimiter(repo, locks, config)
    req = Request(client_id="client", enpoint="/api")

    assert limiter.allow(req).allowed is True
    assert limiter.allow(req).allowed is False

    time.sleep(1.1)
    assert limiter.allow(req).allowed is True