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
# api_middleware MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
from limiter.manager import RateLimitManager
from protocol.request import Request
from observability.logger import log_throttled
from observability.metrics import record_decision


# --------------------------------------------------
# rate limit middleware
# --------------------------------------------------
class RateLimitMiddleware:
    def __init__(self, rate_limiter: RateLimitManager):
        self._rate_limiter = rate_limiter
    
    def handle(self, request: Request):
        decision = self._rate_limiter.allow_request(request)

        record_decision(request.client_id,
                        decision.allowed)
        
        if not decision.allowed:
            log_throttled(request.client_id,
                          request.enpoint)
        
        return decision
