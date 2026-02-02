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
# middleware_example MODULE
# --------------------------------------------------
"""
Use case: API gateway / framework integration.
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
from limiter.manager import RateLimitManager
from config.settings import RateLimitConfig
from protocol.request import Request
from middleware.api_middleware import RateLimitMiddleware


def api_handler(request: Request):
    return {"status": 200, "message": "OK"}


def run():
    manager = RateLimitManager()

    config = RateLimitConfig(
        capacity=2,
        refill_rate=0.5     # 1 request every 2 seconds
    )

    manager.register_leaky_bucket("user_42", config)

    middleware = RateLimitMiddleware(manager)

    print("== Middleware Example ==")

    for i in range(5):
        request = Request(
            client_id="user_42",
            enpoint="/v1/orders"
        )

        decision = middleware.handle(request)

        if decision.allowed:
            response = api_handler(request)
        else:
            response = {
                "status": 429,
                "retry_after": decision.retry_after,
            }
        
        print(f"[{i}] Response: ", response)


if __name__ == "__main__":
    run()
