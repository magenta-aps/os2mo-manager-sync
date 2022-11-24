# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Generator
from datetime import datetime
from datetime import timedelta
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID

import pytest
from fastapi.encoders import jsonable_encoder
from gql import gql  # type: ignore
from more_itertools import one

from sd_managerscript.holstebro_managers import filter_managers
from sd_managerscript.holstebro_managers import get_active_engagements
from sd_managerscript.holstebro_managers import get_manager_org_units
from sd_managerscript.holstebro_managers import terminate_association
from sd_managerscript.models import EngagementFrom
from sd_managerscript.models import OrgUnitManagers
from tests.test_data.sample_test_data import get_active_engagements_data  # type: ignore
from tests.test_data.sample_test_data import get_filter_managers_data
from tests.test_data.sample_test_data import get_filter_managers_error_data
from tests.test_data.sample_test_data import get_filter_managers_terminate
from tests.test_data.sample_test_data import get_sample_data

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


@pytest.fixture()
def gql_client() -> Generator[MagicMock, None, None]:
    """Fixture to mock GraphQLClient."""
    yield MagicMock()


@patch("sd_managerscript.holstebro_managers.query_org_unit")
async def test_get_manager_org_units(mock_query_org_unit: AsyncMock) -> None:
    """Test the "get_manager_org_units" method returns correct '_leder' org-units."""

    sample_data, expected_managers = get_sample_data()
    mock_query_org_unit.side_effect = sample_data
    uuid = UUID("23a2ace2-52ca-458d-bead-d1a42080579f")
    gql_client = AsyncMock()

    returned_managers = await get_manager_org_units(gql_client, org_unit_uuid=uuid)

    assert returned_managers == expected_managers


@pytest.mark.parametrize(
    "employee_uuid, engagement, expected", get_active_engagements_data()
)
@patch("sd_managerscript.holstebro_managers.query_graphql")
async def test_get_active_engagements(
    mock_query_gql: AsyncMock,
    gql_client: MagicMock,
    employee_uuid: UUID,
    engagement: dict,
    expected: dict,
) -> None:
    """Test the "get_active_engagements" method returns correct Manager objects."""

    mock_query_gql.return_value = engagement
    returned_managers = await get_active_engagements(gql_client, employee_uuid)

    assert returned_managers == EngagementFrom.parse_obj(expected)


@pytest.mark.parametrize("org_unit, managers, expected", get_filter_managers_data())
@patch("sd_managerscript.holstebro_managers.get_active_engagements")
async def test_filter_managers(
    mock_get_active_engagements: MagicMock,
    gql_client: MagicMock,
    org_unit: OrgUnitManagers,
    managers: list[dict],
    expected: OrgUnitManagers,
) -> None:
    """Test "filter_managers" returns the correct OrgUnitManagers object"""

    mock_get_active_engagements.side_effect = managers

    returned_org_unit = await filter_managers(gql_client, org_unit)

    assert returned_org_unit == expected


@patch("sd_managerscript.holstebro_managers.get_active_engagements")
async def test_filter_managers_error_raised(
    mock_get_active_engagements: MagicMock, gql_client: MagicMock
) -> None:
    """
    Test that filter_managers raises an exception if two managers
    have same engagement from date
    """
    test_data = get_filter_managers_error_data()

    (org_unit, managers) = test_data

    mock_get_active_engagements.side_effect = managers

    with pytest.raises(Exception):
        _ = await filter_managers(gql_client, org_unit)


@patch("sd_managerscript.holstebro_managers.terminate_association")
@patch("sd_managerscript.holstebro_managers.get_active_engagements")
async def test_filter_managers_calls_terminate(
    mock_get_active_engagements: MagicMock,
    mock_terminate_association: MagicMock,
    gql_client: MagicMock,
) -> None:
    """Test terminate manager is called when a manager doesn't have an active engagement"""

    test_data = get_filter_managers_terminate()

    org_unit, engagement_return = test_data

    org_unit_uuid = jsonable_encoder(org_unit)["uuid"]

    mock_get_active_engagements.side_effect = engagement_return

    _ = await filter_managers(gql_client, org_unit)

    mock_terminate_association.assert_called_once_with(
        gql_client, org_unit_uuid, one(engagement_return)["employee_uuid"]
    )


@pytest.mark.parametrize(
    "employee_uuid, org_unit_uuid, association_uuid",
    [
        (
            "02ee43bd-4fba-48f6-9d3d-b98048372fc4",
            "267e5e49-3abd-49df-9bd9-38d41d2294ff",
            "36b5be05-7323-418f-bbd4-7be23c9ca150",
        ),
        (
            "02ee43bb-4fba-48f6-9d3d-b98044372fc4",
            "4c88d5a3-199f-454b-9349-a24ab218ca54",
            "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
        ),
    ],
)
@patch("sd_managerscript.holstebro_managers.query_graphql", new_callable=AsyncMock)
@patch("sd_managerscript.holstebro_managers.execute_mutator", new_callable=AsyncMock)
async def test_terminate_association(
    mock_execute_mutator: AsyncMock,
    mock_query_graphql: AsyncMock,
    gql_client: MagicMock,
    employee_uuid: str,
    org_unit_uuid: str,
    association_uuid: str,
) -> None:
    """Test "terminate_manager" is called."""

    mock_query_graphql.return_value = association_uuid

    asso_query = gql(
        """
        query ($employees: [UUID!]!, $org_units: [UUID!]!){
            associations(employees: $employees, org_units: $org_units) {
                uuid
            }
        }
    """
    )

    query_input = {
        "input": {"employees": UUID(employee_uuid), "org_units": UUID(org_unit_uuid)}
    }

    mut_query = gql(
        """
        mutation($input: AssociationTerminateInput!){
            association_terminate(input: $input){
                uuid
            }
        }
    """
    )

    input = {
        "input": {
            "uuid": association_uuid,
            "to": (datetime.today() - timedelta(days=1)).date().isoformat(),
        }
    }

    await terminate_association(gql_client, UUID(org_unit_uuid), UUID(employee_uuid))

    mock_query_graphql.assert_called_once_with(gql_client, asso_query, query_input)
    mock_execute_mutator.assert_called_once_with(gql_client, mut_query, input)
