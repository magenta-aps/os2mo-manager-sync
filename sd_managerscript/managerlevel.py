# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0


def get_managerlevel_mapping() -> dict[str, str]:
    """Dict for mapping org_unit_level UUID -> manager-level UUID"""

    # TODO: UUID of "Kommunal Direktør" is just a placeholder and NOT the correct UUID
    # replace "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c" with correct UUID
    managertype = {
        # NY6 : "Kommunal Direktør"
        "1ec3d3ae-8ad6-f689-57a9-7441f6ffca05": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
        # NY5 : "Direktør"
        "891603db-cc28-6ed2-6d48-25e14d3f142f": "e226821b-4af3-1e91-c53f-ea5c57c6d8d0",
        # NY4 : "Chef"
        "0263522a-2c1e-9c80-1880-92c1b97cfead": "a8754726-a4b9-1715-6b41-769c6fe703c5",
        # NY3 : "Leder"
        "fc968d00-41f2-3efb-401a-30a3cf854227": "9ffaff0f-8b6e-6e99-a517-f841a04c61c2",
        # NY2 : "Leder"
        "750e734e-17b8-0174-6787-a5be55adca31": "9ffaff0f-8b6e-6e99-a517-f841a04c61c2",
        # NY1 : "Leder"
        "3ee6f4a5-02cc-41a0-82cc-4b8243664423": "9ffaff0f-8b6e-6e99-a517-f841a04c61c2",
    }

    return managertype
