# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from pytest import MonkeyPatch  # type: ignore

ENV_ROOT_UUID = "8315443f-a918-4eea-9605-150472418101"
ENV_CLIENT_SECRET = "08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"
ENV_MANAGER_TYPE_UUID = "75fee2b6-f405-4c77-b62e-32421c2e43d5"
ENV_RESPONSIBILITY_UUID = "d82039a5-f2d5-48e4-8eab-8c9f7694e16f"

# NY6 : 'Kommunal Direktør'
# NY5 : 'Direktør'
# NY4 : 'Chef'
# NY3 : 'Leder'
# NY2 : 'Leder'
# NY1 : 'Leder'
ENV_MANAGER_LEVEL_MAPPING = """
    [{
        "1ec3d3ae-8ad6-f689-57a9-7441f6ffca05": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
        "891603db-cc28-6ed2-6d48-25e14d3f142f": "e226821b-4af3-1e91-c53f-ea5c57c6d8d0",
        "891603db-cc28-6ed2-6d48-25e14d3f142f": "e226821b-4af3-1e91-c53f-ea5c57c6d8d0",
        "0263522a-2c1e-9c80-1880-92c1b97cfead": "a8754726-a4b9-1715-6b41-769c6fe703c5",
        "fc968d00-41f2-3efb-401a-30a3cf854227": "9ffaff0f-8b6e-6e99-a517-f841a04c61c2",
        "750e734e-17b8-0174-6787-a5be55adca31": "9ffaff0f-8b6e-6e99-a517-f841a04c61c2",
        "3ee6f4a5-02cc-41a0-82cc-4b8243664423": "9ffaff0f-8b6e-6e99-a517-f841a04c61c2"
    }]
    """

mp = MonkeyPatch()
mp.setenv("ROOT_UUID", ENV_ROOT_UUID)
mp.setenv("CLIENT_SECRET", ENV_CLIENT_SECRET)
mp.setenv("MANAGER_TYPE_UUID", ENV_MANAGER_TYPE_UUID)
mp.setenv("RESPONSIBILITY_UUID", ENV_RESPONSIBILITY_UUID)
mp.setenv("MANAGER_LEVEL_MAPPING", ENV_MANAGER_LEVEL_MAPPING)
