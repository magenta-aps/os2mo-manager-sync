# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from unittest.mock import patch
from uuid import UUID

from gql import gql  # type: ignore

from sd_managerscript.holstebro_managers import get_manager_org_units
from tests.test_data.sample_test_data import get_sample_data  # type: ignore


QUERY_ORG_UNITS = gql(
    """
    query ($uuid: [UUID!]!){
        org_units (parents: $uuid){
            objects {
                uuid
                name
                parent_uuid
                child_count
            }
        }
    }
"""
)


@patch("sd_managerscript.holstebro_managers.query_org_unit")
async def test_get_manager_org_units(mock_query_org_unit: AsyncMock) -> None:
    """Test the "get_manager_org_units" method returns correct '_leder' org-units."""

    sample_data, expected_managers = get_sample_data()
    mock_query_org_unit.side_effect = sample_data
    uuid = UUID("23a2ace2-52ca-458d-bead-d1a42080579f")
    gql_client = AsyncMock()

    returned_managers = await get_manager_org_units(gql_client, org_unit_uuid=uuid)

    assert returned_managers == expected_managers
