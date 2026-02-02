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
# identifiers MODULE
# --------------------------------------------------
"""
Client identity utilities.

The rate limiter MUST NOT trust client-supplied counters.
Only identity extraction logic lives here.
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
from typing import Optional
from protocol.request import Request


def extract_client_id(request: Request) -> Optional[str]:
    """
    Extracts the canonical client identifier used for rate
    limiting.

    Priority order:
    1. Authenticated API key
    2. User ID
    3. IP address

    Returns:
        client_id (str) or None if not identifiable
    """

    if request.api_key:
        return request.api_key
    
    if request.user_id:
        return request.user_id
    
    return request.ip_address
