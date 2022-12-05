# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Generator
from datetime import datetime
from datetime import timedelta
from unittest import mock
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID
from uuid import uuid4

import pytest
from gql import gql  # type: ignore

from sd_managerscript.holstebro_managers import create_manager_object
from sd_managerscript.holstebro_managers import filter_managers
from sd_managerscript.holstebro_managers import get_active_engagements
from sd_managerscript.holstebro_managers import get_current_manager
from sd_managerscript.holstebro_managers import get_manager_level
from sd_managerscript.holstebro_managers import get_manager_org_units
from sd_managerscript.holstebro_managers import terminate_association
from sd_managerscript.holstebro_managers import update_manager
from sd_managerscript.models import EngagementFrom
from sd_managerscript.models import Manager
from sd_managerscript.models import ManagerLevel
from sd_managerscript.models import OrgUnitManagers
from tests.test_data.sample_test_data import get_active_engagements_data  # type: ignore
from tests.test_data.sample_test_data import get_create_manager_data
from tests.test_data.sample_test_data import get_filter_managers_data
from tests.test_data.sample_test_data import get_filter_managers_error_data
from tests.test_data.sample_test_data import get_filter_managers_terminate
from tests.test_data.sample_test_data import get_manager_level_data
from tests.test_data.sample_test_data import get_sample_data
from tests.test_data.sample_test_data import get_update_managers_data


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


@pytest.mark.parametrize("org_unit, engagements, expected", get_filter_managers_data())
@patch("sd_managerscript.holstebro_managers.terminate_association")
@patch("sd_managerscript.holstebro_managers.get_active_engagements")
async def test_filter_managers(
    mock_get_active_engagements: MagicMock,
    gql_client: MagicMock,
    org_unit: OrgUnitManagers,
    engagements: list[dict],
    expected: OrgUnitManagers,
) -> None:
    """Test "filter_managers" returns the correct OrgUnitManagers object"""

    mock_get_active_engagements.side_effect = engagements

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


@pytest.mark.parametrize(
    "org_unit, engagement_return, association_uuids", get_filter_managers_terminate()
)
@patch("sd_managerscript.holstebro_managers.terminate_association")
@patch("sd_managerscript.holstebro_managers.get_active_engagements")
async def test_filter_managers_calls_terminate(
    mock_get_active_engagements: MagicMock,
    mock_terminate_association: MagicMock,
    gql_client: MagicMock,
    org_unit: OrgUnitManagers,
    engagement_return: dict,
    association_uuids: list[UUID],
) -> None:
    """Test terminate association is called for employees not assigned as manager"""

    mock_calls = [mock.call(gql_client, asso_uuid) for asso_uuid in association_uuids]

    mock_get_active_engagements.side_effect = engagement_return

    _ = await filter_managers(gql_client, org_unit)

    # Assert that terminate_associate get called with correct parameters in correct order.
    mock_terminate_association.assert_has_calls(mock_calls)


@pytest.mark.parametrize(
    "association_uuid",
    [
        "36b5be05-7323-418f-bbd4-7be23c9ca150",
        "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
    ],
)
@patch("sd_managerscript.holstebro_managers.execute_mutator", new_callable=AsyncMock)
async def test_terminate_association(
    mock_execute_mutator: AsyncMock,
    gql_client: MagicMock,
    association_uuid: str,
) -> None:
    """Test "terminate_manager" is called."""

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

    await terminate_association(gql_client, UUID(association_uuid))

    mock_execute_mutator.assert_called_once_with(gql_client, mut_query, input)


@patch("sd_managerscript.holstebro_managers.query_graphql")
async def test_get_current_manager_uuid(
    mock_query_graphql: MagicMock,
    gql_client: MagicMock,
) -> None:
    """Test "get_current_manager" returns correct values"""

    ou_uuid = "3e702dd1-4103-4116-bb2d-b150aebe807d"
    manager_uuid = "27935dbb-c173-4116-a4b5-75022315749d"

    return_dict: dict = {
        "org_units": [{"objects": [{"managers": [{"uuid": manager_uuid}]}]}]
    }

    mock_query_graphql.return_value = return_dict
    returned_uuid = await get_current_manager(gql_client, UUID(ou_uuid))

    assert returned_uuid == UUID(manager_uuid)


@patch("sd_managerscript.holstebro_managers.query_graphql")
async def test_get_current_manager_none(
    mock_query_graphql: MagicMock,
    gql_client: MagicMock,
) -> None:
    """Test "get_current_manager" returns correct values"""

    ou_uuid = "27935dbb-c173-4116-a4b5-75022315749d"

    return_dict: dict = {"org_units": [{"objects": [{"managers": []}]}]}

    mock_query_graphql.return_value = return_dict
    returned_uuid = await get_current_manager(gql_client, UUID(ou_uuid))

    assert returned_uuid is None


@pytest.mark.parametrize(
    "manager, query, current_manager_uuid, variables", get_update_managers_data()
)
@patch("sd_managerscript.holstebro_managers.execute_mutator")
@patch("sd_managerscript.holstebro_managers.get_current_manager")
async def test_update_manager_object(
    mock_get_current_manager: MagicMock,
    mock_execute_mutator: AsyncMock,
    gql_client: MagicMock,
    manager: Manager,
    query: str,
    current_manager_uuid: str,
    variables: dict,
) -> None:
    """Test update_manager can update and create new manager object"""

    org_unit_uuid = uuid4()

    mock_get_current_manager.return_value = current_manager_uuid

    await update_manager(gql_client, org_unit_uuid, manager)

    mock_execute_mutator.assert_called_once_with(gql_client, query, variables)


@pytest.mark.parametrize(
    "employee_uuid, from_date, manager_level, expected_manager",
    get_create_manager_data(),
)
async def test_create_manager_object(
    employee_uuid: UUID,
    from_date: datetime,
    manager_level: ManagerLevel,
    expected_manager: Manager,
) -> None:
    """Test creation of Manager object based on OrgUnitManagers object"""

    returned_manager = await create_manager_object(
        employee_uuid, from_date, manager_level
    )

    assert returned_manager == expected_manager


@pytest.mark.parametrize(
    "org_unit, parent_org_unit, expected_manager_lvl", get_manager_level_data()
)
@patch("sd_managerscript.holstebro_managers.query_org_unit")
async def test_get_manager_level(
    mock_query_org_unit: AsyncMock,
    org_unit: OrgUnitManagers,
    parent_org_unit: OrgUnitManagers,
    expected_manager_lvl: ManagerLevel,
) -> None:
    """Test getting correct org-unit level uuid"""

    mock_query_org_unit.return_value = parent_org_unit

    returned_manager_lvl = await get_manager_level(gql_client, org_unit)

    assert returned_manager_lvl == expected_manager_lvl
