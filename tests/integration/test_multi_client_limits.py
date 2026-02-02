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
# test_multi_client_limits MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
from limiter.manager import RateLimitManager
from config.settings import RateLimitConfig
from protocol.request import Request


def test_multiple_clients_isolated_limits():
    manager = RateLimitManager()
    config = RateLimitConfig(capacity=1, refill_rate=1)

    manager.register_leaky_bucket("client_A", config)
    manager.register_leaky_bucket("client_B", config)

    req_a = Request(client_id="client_A", enpoint="/a")
    req_b = Request(client_id="client_B", enpoint="/x")

    assert manager.allow_request(req_a).allowed is True
    assert manager.allow_request(req_a).allowed is False

    # Client B unaffected
    assert manager.allow_request(req_b).allowed is True
