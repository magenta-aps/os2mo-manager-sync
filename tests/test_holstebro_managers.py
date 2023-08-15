# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Generator
from datetime import datetime
from datetime import timedelta
from unittest import mock
from unittest.mock import AsyncMock
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID
from uuid import uuid4

import pytest
from freezegun import freeze_time  # type: ignore
from gql import gql  # type: ignore
from ramodels.mo import Validity  # type: ignore

from sd_managerscript.exceptions import ConflictingManagers  # type: ignore
from sd_managerscript.holstebro_managers import check_manager_engagement
from sd_managerscript.holstebro_managers import create_manager_object
from sd_managerscript.holstebro_managers import create_update_manager
from sd_managerscript.holstebro_managers import filter_managers
from sd_managerscript.holstebro_managers import get_active_engagements
from sd_managerscript.holstebro_managers import get_current_manager
from sd_managerscript.holstebro_managers import get_manager_level
from sd_managerscript.holstebro_managers import get_manager_org_units
from sd_managerscript.holstebro_managers import get_unengaged_managers
from sd_managerscript.holstebro_managers import terminate_association
from sd_managerscript.holstebro_managers import terminate_manager
from sd_managerscript.holstebro_managers import update_manager
from sd_managerscript.models import Association
from sd_managerscript.models import EngagementFrom
from sd_managerscript.models import Manager
from sd_managerscript.models import ManagerLevel
from sd_managerscript.models import OrgUnitManagers
from sd_managerscript.models import Parent
from sd_managerscript.queries import QUERY_ORG_UNIT_LEVEL
from tests.test_data.sample_test_data import get_active_engagements_data  # type: ignore
from tests.test_data.sample_test_data import get_create_manager_data
from tests.test_data.sample_test_data import get_create_update_manager_data
from tests.test_data.sample_test_data import get_create_update_manager_led_adm_data
from tests.test_data.sample_test_data import get_filter_managers_data
from tests.test_data.sample_test_data import get_filter_managers_error_data
from tests.test_data.sample_test_data import get_filter_managers_terminate
from tests.test_data.sample_test_data import get_manager_engagement_data
from tests.test_data.sample_test_data import get_sample_data
from tests.test_data.sample_test_data import get_unengaged_managers_data
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


async def test_get_manager_org_units_recursion_disabled() -> None:
    # Arrange
    _leder_org_unit_uuid = uuid4()
    association_uuid = uuid4()
    employee_uuid = uuid4()
    association_type_uuid = uuid4()
    parent_uuid = uuid4()
    org_uuid = uuid4()
    org_unit_level_uuid = uuid4()

    mock_execute = AsyncMock(
        return_value={
            "org_units": [
                {
                    "objects": [
                        {
                            "uuid": str(uuid4()),
                            "name": "some sub unit with children",
                            "child_count": 5,
                            "associations": [],
                            "parent": {
                                "uuid": parent_uuid,
                                "name": "some unit",
                                "parent_uuid": org_uuid,
                                "org_unit_level_uuid": str(uuid4()),
                            },
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "uuid": str(_leder_org_unit_uuid),
                            "name": "the _leder sub unit_leder",
                            "child_count": 0,
                            "associations": [
                                {
                                    "uuid": str(association_uuid),
                                    "org_unit_uuid": str(_leder_org_unit_uuid),
                                    "employee_uuid": str(employee_uuid),
                                    "association_type_uuid": str(association_type_uuid),
                                    "validity": {
                                        "from": "2006-01-17T00:00:00",
                                        "to": None,
                                    },
                                }
                            ],
                            "parent": {
                                "uuid": str(parent_uuid),
                                "name": "some unit",
                                "parent_uuid": str(org_uuid),
                                "org_unit_level_uuid": str(org_unit_level_uuid),
                            },
                        }
                    ]
                },
            ]
        }
    )
    mock_gql_client = AsyncMock()
    mock_gql_client.execute = mock_execute

    # Act
    manager_org_units = await get_manager_org_units(mock_gql_client, parent_uuid, False)

    # Assert
    assert manager_org_units == [
        OrgUnitManagers(
            uuid=_leder_org_unit_uuid,
            name="the _leder sub unit_leder",
            child_count=0,
            associations=[
                Association(
                    uuid=association_uuid,
                    org_unit_uuid=_leder_org_unit_uuid,
                    employee_uuid=employee_uuid,
                    association_type_uuid=association_type_uuid,
                    validity=Validity(from_date=datetime(2006, 1, 17, 0, 0, 0)),
                )
            ],
            parent=Parent(
                uuid=parent_uuid,
                name="some unit",
                parent_uuid=org_uuid,
                org_unit_level_uuid=org_unit_level_uuid,
            ),
        )
    ]


@pytest.mark.parametrize(
    "org_unit_uuid, root_uuid",
    [
        (
            UUID("23a2ace2-52ca-458d-bead-d1a42080579f"),
            UUID("23a2ace2-52ca-458d-bead-d1a42080579f"),
        ),
        (
            UUID("b6fd7f0e-b47f-4370-a8d3-8003cbfb3be2"),
            UUID("23a2ace2-52ca-458d-bead-d1a42080579f"),
        ),
    ],
)
@patch("sd_managerscript.holstebro_managers.get_unengaged_managers")
@patch("sd_managerscript.holstebro_managers.query_graphql")
async def test_check_manager_engagement(
    mock_query_graphql: AsyncMock,
    mock_get_unengaged_managers: MagicMock,
    gql_client: MagicMock,
    org_unit_uuid: UUID,
    root_uuid: UUID,
) -> None:
    """
    Test check_manager_engagement can check if managers are engaged
    and if not, will terminate the manager role.
    """

    sample_data, managers = get_manager_engagement_data()
    mock_query_graphql.side_effect = sample_data
    mock_get_unengaged_managers.side_effect = managers

    managers_list = await check_manager_engagement(gql_client, org_unit_uuid, root_uuid)
    expected = [x for x in managers if x is not None]

    assert managers_list == expected


@freeze_time("2023-01-01")
@pytest.mark.parametrize("query_dict, expected", get_unengaged_managers_data())
async def test_get_unengaged_managers(
    query_dict: dict[str, str | dict[str, str]], expected: UUID | None
) -> None:
    """Test The input gets filtered correctly to find managers with no active engagement"""

    managers_to_terminate = await get_unengaged_managers(query_dict)

    assert managers_to_terminate == expected


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

    with pytest.raises(ConflictingManagers):
        await filter_managers(gql_client, org_unit)


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
            "to": (datetime.today() - timedelta(days=0)).date().isoformat(),
        }
    }

    await terminate_association(gql_client, UUID(association_uuid))

    mock_execute_mutator.assert_called_once_with(gql_client, mut_query, input)


@pytest.mark.parametrize(
    "manager_uuid",
    [
        "36b5be05-7323-418f-bbd4-7be23c9ca150",
        "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
    ],
)
@patch("sd_managerscript.holstebro_managers.execute_mutator", new_callable=AsyncMock)
async def test_terminate_manager(
    mock_execute_mutator: AsyncMock,
    gql_client: MagicMock,
    manager_uuid: str,
) -> None:
    """Test "terminate_manager" is called."""

    mut_query = gql(
        """
        mutation($input: ManagerTerminateInput!){
            manager_terminate(input: $input){
                uuid
            }
        }
    """
    )

    input = {
        "input": {
            "uuid": manager_uuid,
            "to": (datetime.today() - timedelta(days=0)).date().isoformat(),
        }
    }

    await terminate_manager(gql_client, UUID(manager_uuid))

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
    "manager, org_unit_uuid, query, current_manager_uuid, variables",
    get_update_managers_data(),
)
@patch("sd_managerscript.holstebro_managers.execute_mutator")
@patch("sd_managerscript.holstebro_managers.get_current_manager")
async def test_update_manager_object(
    mock_get_current_manager: MagicMock,
    mock_execute_mutator: AsyncMock,
    gql_client: MagicMock,
    manager: Manager,
    org_unit_uuid: UUID,
    query: str,
    current_manager_uuid: str,
    variables: dict,
) -> None:
    """Test update_manager can update and create new manager object"""

    mock_get_current_manager.return_value = current_manager_uuid

    await update_manager(gql_client, org_unit_uuid, manager)

    mock_execute_mutator.assert_called_once_with(gql_client, query, variables)


@pytest.mark.parametrize(
    "org_unit, manager_level, expected_manager",
    get_create_manager_data(),
)
@freeze_time("2019-01-14", tz_offset=1)
async def test_create_manager_object(
    org_unit: OrgUnitManagers,
    manager_level: ManagerLevel,
    expected_manager: Manager,
) -> None:
    """Test creation of Manager object based on OrgUnitManagers object"""

    returned_manager = await create_manager_object(org_unit, manager_level)

    assert returned_manager == expected_manager


async def test_get_manager_level(gql_client: MagicMock) -> None:
    """
    Test get_manager_level in the case where the OU is a "normal"
    unit, i.e. a unit where the name is not suffixed with _led-adm
    """

    # Arrange
    org_unit_manager = OrgUnitManagers(
        uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
        name="SomeUnit_leder",
        child_count=0,
        parent=Parent(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="SomeUnit",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            org_unit_level_uuid=UUID("0263522a-2c1e-9c80-1880-92c1b97cfead"),
        ),
        associations=[],
    )

    # Act
    actual_manager_level = await get_manager_level(gql_client, org_unit_manager)

    # Assert
    assert actual_manager_level == ManagerLevel(
        uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5")
    )


async def test_get_manager_level_led_adm() -> None:
    """
    Test get_manager_level in the case where the OU is a "led-adm"
    unit, i.e. a unit where the name is suffixed with _led-adm
    """

    # Arrange
    org_unit_manager = OrgUnitManagers(
        uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
        name="SomeUnit_leder",
        child_count=0,
        parent=Parent(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="SomeUnit_led-adm",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            org_unit_level_uuid=UUID("0263522a-2c1e-9c80-1880-92c1b97cfead"),
        ),
        associations=[],
    )
    mock_gql_client = AsyncMock()
    mock_execute = AsyncMock(
        return_value={
            "org_units": [
                {
                    "objects": [
                        {"org_unit_level_uuid": "891603db-cc28-6ed2-6d48-25e14d3f142f"}
                    ]
                }
            ]
        }
    )
    mock_gql_client.execute = mock_execute

    # Act
    actual_manager_level = await get_manager_level(mock_gql_client, org_unit_manager)

    # Assert
    mock_execute.assert_awaited_once_with(
        QUERY_ORG_UNIT_LEVEL,
        variable_values={"uuids": "2665d8e0-435b-5bb6-a550-f275692984ef"},
    )
    assert actual_manager_level == ManagerLevel(
        uuid=UUID("e226821b-4af3-1e91-c53f-ea5c57c6d8d0")
    )


@patch("sd_managerscript.holstebro_managers.update_manager")
@patch("sd_managerscript.holstebro_managers.create_manager_object")
@patch("sd_managerscript.holstebro_managers.get_manager_level")
async def test_create_update_manager(
    mock_get_manager_level: MagicMock,
    mock_create_manager_object: MagicMock,
    mock_update_manager: MagicMock,
) -> None:
    """Test creating and updating Manager object and role"""

    org_unit, manager_lvl, manager = get_create_update_manager_data()

    mock_get_manager_level.return_value = manager_lvl
    mock_create_manager_object.return_value = manager

    await create_update_manager(gql_client, org_unit)

    mock_update_manager.assert_called_once_with(
        gql_client, org_unit.parent.uuid, manager
    )


@patch("sd_managerscript.holstebro_managers.update_manager")
@patch("sd_managerscript.holstebro_managers.create_manager_object")
@patch("sd_managerscript.holstebro_managers.get_manager_level")
async def test_create_update_manager_led_adm(
    mock_get_manager_level: MagicMock,
    mock_create_manager_object: MagicMock,
    mock_update_manager: MagicMock,
) -> None:
    """
    Test creating and updating Manager object and role with
    parent being a "led-adm" org-unit

    """
    org_unit, manager_lvl, manager = get_create_update_manager_led_adm_data()

    mock_get_manager_level.return_value = manager_lvl
    mock_create_manager_object.return_value = manager
    calls = [
        call(gql_client, org_unit.parent.uuid, manager),
        call(gql_client, org_unit.parent.parent_uuid, manager),
    ]

    await create_update_manager(gql_client, org_unit)

    mock_update_manager.assert_has_calls(calls, any_order=True)
