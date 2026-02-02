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
# clock MODULE
# --------------------------------------------------
"""
Purpose: Deterministic, mockable time source.

Clock abstraction

Avoids direct calls to time.time() throughout the 
codebase.
Critical for testing and deterministic behaviour.
"""
# --------------------------------------------------
# imports
# --------------------------------------------------
import time
# from abc import ABC, abstractmethod


# --------------------------------------------------
# clock
# --------------------------------------------------
class Clock():
    """Abstract clock interface."""

    def now(self) -> float:
        """Returns current time in seconds."""
        raise NotImplementedError
    

# --------------------------------------------------
# system clock
# --------------------------------------------------
class SystemClock(Clock):
    """Production clock using system time."""

    def now(self) -> float:
        return time.time()
    
