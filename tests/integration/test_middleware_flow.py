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
# test_middleware_flow MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
from limiter.manager import RateLimitManager
from middleware.api_middleware import RateLimitMiddleware
from config.settings import RateLimitConfig
from protocol.request import Request


def test_middleware_allows_and_blocks_requests():
    manager = RateLimitManager()
    config = RateLimitConfig(capacity=2, refill_rate=1)

    manager.register_leaky_bucket("client_1", config)
    middleware = RateLimitMiddleware(manager)

    req = Request(client_id="client_1", enpoint="/test")

    # First two requests allowed
    assert middleware.handle(req).allowed is True
    assert middleware.handle(req).allowed is True

    # Third request rejected
    decision = middleware.handle(req)
    assert decision.allowed is False
    assert decision.retry_after is not None
