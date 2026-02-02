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
# test_repository MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
from state.memory_store import InMemoryBucketRepository
from state.bucket import TokenBucketState


def test_in_memory_repository_crud():
    repo = InMemoryBucketRepository()

    bucket = TokenBucketState(
        capacity=10,
        refill_rate=1,
        current_tokens=5,
        last_refill_timestamp=0,
    )

    repo.save("client", bucket)
    assert repo.get("client") is bucket

    repo.delete("client")
    assert repo.get("client") is None
