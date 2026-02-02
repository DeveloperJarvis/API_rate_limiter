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
# test_high_throughput MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import threading

from limiter.manager import RateLimitManager
from config.settings import RateLimitConfig
from protocol.request import Request
from tests.utils.fake_clock import FakeClock


def test_high_throughput_concurrent_requests():
    manager = RateLimitManager()
    config = RateLimitConfig(capacity=100, refill_rate=100)

    clock = FakeClock(start=0.0)

    manager.register_token_bucket(
        "hot_client", config, clock=clock
    )

    request = Request(client_id="hot_client",
                      enpoint="/load")
    results = []

    def worker():
        decision = manager.allow_request(request)
        results.append(decision.allowed)
    
    threads = [threading.Thread(target=worker)
               for _ in range(200)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Should never allow more than capacity immediately
    assert sum(results) == 100
