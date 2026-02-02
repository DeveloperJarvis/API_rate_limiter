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
# main MODULE
# --------------------------------------------------
"""
Main entry point for API Rate Limiter library.

This file is intentionally minimal.
In real deployments, the limiter is imported
into an API gateway or middleware layer.
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
from limiter.manager import RateLimitManager
from config.settings import RateLimitConfig
from protocol.request import Request


def main():
    config = RateLimitConfig(
        capacity=10,
        refill_rate=2,  # tokens per second
    )

    rate_limiter = RateLimitManager()
    rate_limiter.register_leaky_bucket(
        "demo_client", config
    )

    for i in range(15):
        request = Request(client_id="demo_client",
                          enpoint="/health")
        decision = rate_limiter.allow_request(request)

        if decision.allowed:
            print(f"[{i}] ✅ Allowed | Remaining: "
                  f"{decision.remaining}")
        else:
            print(f"[{i}] ❌ Rejected | Retry after: "
                  f"{decision.retry_after}s")


if __name__ == "__main__":
    main()
