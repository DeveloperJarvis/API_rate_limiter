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
# leaky_bucket_basic MODULE
# --------------------------------------------------
"""
Use case: Smooth, internal service traffic.
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
import time

from limiter.manager import RateLimitManager
from config.settings import RateLimitConfig
from protocol.request import Request


def run():
    manager = RateLimitManager()

    config = RateLimitConfig(
        capacity=3,
        refill_rate=1   # drain 1 request / second
    )

    manager.register_leaky_bucket("service_X", config)

    print("== Leaky Bucket Example ==")

    for i in range(6):
        request = Request(
            client_id="service_X",
            enpoint="/internal/job"
        )

        decision = manager.allow_request(request)

        print(
            f"[{i}]",
            ("✅ Allowed" if decision.allowed 
             else "❌ Rejected"),
             f"| remaining={decision.remaining}",
        )

        time.sleep(0.2)


if __name__ == "__main__":
    run()
