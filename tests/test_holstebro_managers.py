# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Generator
from copy import deepcopy
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
from dateutil.tz import tzoffset  # type: ignore
from freezegun import freeze_time  # type: ignore
from gql import gql  # type: ignore
from ramodels.mo import Validity  # type: ignore

from sd_managerscript.exceptions import ConflictingManagers  # type: ignore
from sd_managerscript.filters import filter_managers
from sd_managerscript.holstebro_managers import check_manager_engagement
from sd_managerscript.holstebro_managers import create_manager_object
from sd_managerscript.holstebro_managers import create_update_manager
from sd_managerscript.holstebro_managers import get_current_manager
from sd_managerscript.holstebro_managers import get_manager_level
from sd_managerscript.holstebro_managers import get_manager_org_units
from sd_managerscript.holstebro_managers import get_unengaged_managers
from sd_managerscript.holstebro_managers import is_manager_correct
from sd_managerscript.holstebro_managers import update_manager
from sd_managerscript.mo import get_active_engagements
from sd_managerscript.models import Association
from sd_managerscript.models import EngagementFrom
from sd_managerscript.models import Manager
from sd_managerscript.models import ManagerLevel
from sd_managerscript.models import ManagerType
from sd_managerscript.models import OrgUnitManager
from sd_managerscript.models import OrgUnitManagers
from sd_managerscript.models import Parent
from sd_managerscript.queries import QUERY_ORG_UNIT_LEVEL
from sd_managerscript.terminate import terminate_association
from sd_managerscript.terminate import terminate_manager
from tests.test_data.sample_test_data import get_active_engagements_data  # type: ignore
from tests.test_data.sample_test_data import get_create_manager_data
from tests.test_data.sample_test_data import get_create_update_manager_data
from tests.test_data.sample_test_data import get_create_update_manager_led_adm_data
from tests.test_data.sample_test_data import get_filter_managers_data
from tests.test_data.sample_test_data import get_filter_managers_error_data
from tests.test_data.sample_test_data import get_filter_managers_terminate
from tests.test_data.sample_test_data import get_manager_engagement_data
from tests.test_data.sample_test_data import get_unengaged_managers_data
from tests.test_data.sample_test_data import get_update_managers_data

# from tests.test_data.sample_test_data import get_sample_data


QUERY_ORG_UNITS = gql(
    """
    query ($uuid: [UUID!]!){
        org_units (filter: { parent: {uuids: $uuid} }){
            objects {
                validities {
                    uuid
                    name
                    parent_uuid
                    has_children
                }
            }
        }
    }
"""
)


@pytest.fixture()
def gql_client() -> Generator[AsyncMock, None, None]:
    """Fixture to mock GraphQLClient."""
    yield AsyncMock()


# FIX: Not sure how to test with recursive=True and mocks. It seems to run infinitely

# @patch("sd_managerscript.holstebro_managers.query_org_unit")
# async def test_get_manager_org_units(mock_query_org_unit: AsyncMock) -> None:
#     """Test the "get_manager_org_units" method returns correct '_leder' org-units."""
#
#     uuid = UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c")
#     sample_data = get_sample_data()
#     mock_query_org_unit.return_value = sample_data
#
#     returned_managers = await get_manager_org_units(
#         mock_query_org_unit, org_unit_uuid=uuid
#     )
#
#     assert returned_managers == [
#         OrgUnitManagers(
#             uuid=UUID("72d8e92f-9481-43af-8cb0-a83823c9f35e"),
#             name="Almind skole_leder",
#             has_children=False,
#             associations=[
#                 Association(
#                     uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
#                     org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
#                     employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
#                     association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
#                     validity=Validity(
#                         from_date=datetime(
#                             2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
#                         ),
#                         to_date=None,
#                     ),
#                 )
#             ],
#             parent=Parent(
#                 uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
#                 name="Skoler",
#                 parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
#                 org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
#             ),
#         ),
#         OrgUnitManagers(
#             uuid=UUID("60370b40-a143-40c5-aaa1-638b3b74d119"),
#             name="Social Indsats_LEDER",
#             has_children=True,
#             associations=[
#                 Association(
#                     uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
#                     org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
#                     employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
#                     association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
#                     validity=Validity(
#                         from_date=datetime(
#                             2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
#                         ),
#                         to_date=None,
#                     ),
#                 )
#             ],
#             parent=Parent(
#                 uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
#                 name="Skoler",
#                 parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
#                 org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
#             ),
#         ),
#         OrgUnitManagers(
#             uuid=UUID("23f3cebf-2625-564a-bcfc-31272eb9bce2"),
#             name="Social og sundhed_leder",
#             has_children=False,
#             associations=[
#                 Association(
#                     uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
#                     org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
#                     employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
#                     association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
#                     validity=Validity(
#                         from_date=datetime(
#                             2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
#                         ),
#                         to_date=None,
#                     ),
#                 )
#             ],
#             parent=Parent(
#                 uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
#                 name="Skoler",
#                 parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
#                 org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
#             ),
#         ),
#     ]


@patch("sd_managerscript.holstebro_managers.query_org_unit")
async def test_get_manager_org_units_recursion_disabled(
    mock_query_graphql: AsyncMock,
) -> None:
    parent_uuid = uuid4()
    mock_query_graphql.return_value = [
        OrgUnitManagers(
            uuid=UUID("72d8e92f-9481-43af-8cb0-a83823c9f35e"),
            name="Almind skole_leder",
            has_children=False,
            parent=Parent(
                uuid=parent_uuid,
                name="Almind skole",
                parent_uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        OrgUnitManagers(
            uuid=parent_uuid,
            name="Almind skole",
            has_children=True,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[],
        ),
    ]

    manager_org_units = await get_manager_org_units(
        mock_query_graphql, parent_uuid, False
    )

    # Assert
    assert manager_org_units == [
        OrgUnitManagers(
            uuid=UUID("72d8e92f-9481-43af-8cb0-a83823c9f35e"),
            name="Almind skole_leder",
            has_children=False,
            parent=Parent(
                uuid=parent_uuid,
                name="Almind skole",
                parent_uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
    ]


@pytest.mark.parametrize(
    "org_unit_uuid, root_uuid",
    [
        (
            UUID("1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"),
            UUID("1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"),
        ),
        (
            UUID("96a4715c-f4df-422f-a4b0-9dcc686753f7"),
            UUID("1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"),
        ),
    ],
)
@patch("sd_managerscript.holstebro_managers.query_graphql")
async def test_check_manager_engagement(
    mock_query_graphql: AsyncMock,
    gql_client: AsyncMock,
    org_unit_uuid: UUID,
    root_uuid: UUID,
) -> None:
    """
    Test check_manager_engagement can check if managers are engaged
    and if not, will terminate the manager role.
    """

    sample_data = get_manager_engagement_data()
    mock_query_graphql.side_effect = sample_data

    managers_list = await check_manager_engagement(gql_client, org_unit_uuid, root_uuid)

    assert managers_list == [
        OrgUnitManager(
            org_unit_uuid=UUID("1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"),
            manager_uuid=UUID("a7d51c1d-bcb2-4650-80f3-3b2ab630bc5e"),
        ),
        OrgUnitManager(
            org_unit_uuid=UUID("96a4715c-f4df-422f-a4b0-9dcc686753f7"),
            manager_uuid=UUID("37dbbd86-1e4f-4292-a9a7-f92be4b7371e"),
        ),
        OrgUnitManager(
            org_unit_uuid=UUID("e054559b-bc15-4203-bced-44375aed1555"),
            manager_uuid=UUID("f000416d-193d-45da-a405-bf95fe4f65d1"),
        ),
        OrgUnitManager(
            org_unit_uuid=UUID("0c655440-867d-561e-8c28-2aa0ac8d1e20"),
            manager_uuid=UUID("d0d0ab19-f69d-425e-a089-76610e8329dc"),
        ),
    ]


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
@patch("sd_managerscript.mo.query_graphql")
async def test_get_active_engagements(
    mock_query_gql: AsyncMock,
    gql_client: AsyncMock,
    employee_uuid: UUID,
    engagement: dict,
    expected: dict,
) -> None:
    """Test the "get_active_engagements" method returns correct Manager objects."""
    # Arrange
    mock_query_gql.return_value = engagement

    # Act
    returned_managers = await get_active_engagements(gql_client, employee_uuid)

    # Assert
    assert returned_managers == EngagementFrom.parse_obj(expected)


@pytest.mark.parametrize("org_unit, engagements, expected", get_filter_managers_data())
@patch("sd_managerscript.terminate.terminate_association")
@patch("sd_managerscript.filters.get_active_engagements")
async def test_filter_managers(
    mock_get_active_engagements: MagicMock,
    gql_client: AsyncMock,
    org_unit: OrgUnitManagers,
    engagements: list[dict],
    expected: OrgUnitManagers,
) -> None:
    """Test "filter_managers" returns the correct OrgUnitManagers object"""

    mock_get_active_engagements.side_effect = engagements

    returned_org_unit = await filter_managers(gql_client, org_unit)

    assert returned_org_unit == expected


@patch("sd_managerscript.filters.get_active_engagements")
async def test_filter_managers_error_raised(
    mock_get_active_engagements: MagicMock, gql_client: AsyncMock
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
@patch("sd_managerscript.filters.terminate_association")
@patch("sd_managerscript.filters.get_active_engagements")
async def test_filter_managers_calls_terminate(
    mock_get_active_engagements: MagicMock,
    mock_terminate_association: MagicMock,
    gql_client: AsyncMock,
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
@patch("sd_managerscript.terminate.execute_mutator", new_callable=AsyncMock)
async def test_terminate_association(
    mock_execute_mutator: AsyncMock,
    gql_client: AsyncMock,
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

    input_ = {
        "input": {
            "uuid": association_uuid,
            "to": (datetime.today() - timedelta(days=0)).date().isoformat(),
        }
    }

    await terminate_association(gql_client, UUID(association_uuid))

    mock_execute_mutator.assert_called_once_with(gql_client, mut_query, input_)


@pytest.mark.parametrize(
    "manager_uuid",
    [
        "36b5be05-7323-418f-bbd4-7be23c9ca150",
        "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
    ],
)
@patch("sd_managerscript.terminate.execute_mutator", new_callable=AsyncMock)
async def test_terminate_manager(
    mock_execute_mutator: AsyncMock,
    gql_client: AsyncMock,
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
    gql_client: AsyncMock,
) -> None:
    """Test "get_current_manager" returns correct values"""

    ou_uuid = uuid4()
    manager_uuid = uuid4()
    employee_uuid = uuid4()
    manager_level_uuid = uuid4()
    manager_type_uuid = uuid4()

    from_ = datetime.now()

    return_dict: dict = {
        "org_units": {
            "objects": [
                {
                    "validities": [
                        {
                            "managers": [
                                {
                                    "uuid": str(manager_uuid),
                                    "employee_uuid": str(employee_uuid),
                                    "manager_level_uuid": str(manager_level_uuid),
                                    "manager_type_uuid": str(manager_type_uuid),
                                    "org_unit_uuid": str(ou_uuid),
                                    "validity": {
                                        "from": from_.isoformat(),
                                        "to": None,
                                    },
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

    mock_query_graphql.return_value = return_dict
    manager = await get_current_manager(gql_client, ou_uuid)

    assert manager == Manager(
        employee=employee_uuid,
        manager_level=ManagerLevel(uuid=manager_level_uuid),
        manager_type=ManagerType(uuid=manager_type_uuid),
        validity=Validity(from_date=from_),
        org_unit=ou_uuid,
        uuid=manager_uuid,
    )


@patch("sd_managerscript.holstebro_managers.query_graphql")
async def test_get_current_manager_none(
    mock_query_graphql: MagicMock,
    gql_client: AsyncMock,
) -> None:
    """Test "get_current_manager" returns correct values"""

    ou_uuid = "27935dbb-c173-4116-a4b5-75022315749d"

    return_dict: dict = {"org_units": {"objects": [{"validities": [{"managers": []}]}]}}

    mock_query_graphql.return_value = return_dict
    returned_uuid = await get_current_manager(gql_client, UUID(ou_uuid))

    assert returned_uuid is None


@pytest.mark.parametrize(
    "manager, org_unit_uuid, query, current_manager, variables",
    get_update_managers_data(),
)
@patch("sd_managerscript.holstebro_managers.execute_mutator")
@patch("sd_managerscript.holstebro_managers.get_current_manager")
async def test_update_manager_object(
    mock_get_current_manager: MagicMock,
    mock_execute_mutator: AsyncMock,
    gql_client: AsyncMock,
    manager: Manager,
    org_unit_uuid: UUID,
    query: str,
    current_manager: str,
    variables: dict,
) -> None:
    """Test update_manager can update and create new manager object"""

    mock_get_current_manager.return_value = current_manager

    await update_manager(gql_client, org_unit_uuid, manager)

    mock_execute_mutator.assert_called_once_with(gql_client, query, variables)


@patch("sd_managerscript.holstebro_managers.execute_mutator")
@patch("sd_managerscript.holstebro_managers.get_current_manager")
async def test_manager_not_updated_when_already_correct(
    mock_get_current_manager: AsyncMock,
    mock_execute_mutator: AsyncMock,
    gql_client: AsyncMock,
) -> None:
    """
    This test ensures that we do not try to update a manager (and hence
    create a new registration in the LoRa DB) when the manager data in MO
    is already set correctly.
    """

    # Arrange

    employee = uuid4()
    manager_level = ManagerLevel(uuid=uuid4())
    manager_type = ManagerType(uuid=uuid4())
    org_unit = uuid4()

    current_manager = Manager(
        uuid=uuid4(),
        manager_level=manager_level,
        manager_type=manager_type,
        employee=employee,
        org_unit=org_unit,
        validity=Validity(
            from_date=datetime(2022, 8, 1, 0, 0),
            to_date=None,
        ),
    )
    potential_new_manager = Manager(
        employee=employee,
        org_unit=org_unit,
        manager_level=manager_level,
        manager_type=manager_type,
        validity=Validity(
            from_date=datetime.today().date().isoformat(),
            to_date=None,
        ),
    )

    mock_get_current_manager.return_value = current_manager

    # Act
    await update_manager(gql_client, org_unit, potential_new_manager)

    # Assert
    mock_execute_mutator.assert_not_awaited()


def test_is_manager_correct() -> None:
    org_unit = uuid4()
    current_manager = Manager(
        uuid=uuid4(),
        manager_level=ManagerLevel(uuid=uuid4()),
        manager_type=ManagerType(uuid=uuid4()),
        employee=uuid4(),
        org_unit=org_unit,
        validity=Validity(
            from_date=datetime(2022, 8, 1, 0, 0),
            to_date=None,
        ),
    )

    # Test that False is returned if there is a mismatch in one of
    # the properties

    new_manager = deepcopy(current_manager)
    new_manager.manager_type = ManagerType(uuid=uuid4())
    assert not is_manager_correct(current_manager, new_manager, org_unit)

    new_manager = deepcopy(current_manager)
    new_manager.manager_level = ManagerLevel(uuid=uuid4())
    assert not is_manager_correct(current_manager, new_manager, org_unit)

    new_manager = deepcopy(current_manager)
    assert not is_manager_correct(current_manager, new_manager, uuid4())

    new_manager = deepcopy(current_manager)
    new_manager.employee = uuid4()
    assert not is_manager_correct(current_manager, new_manager, org_unit)

    # Ensure that True is returned if everything match
    assert is_manager_correct(current_manager, current_manager, org_unit)


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


async def test_get_manager_level(gql_client: AsyncMock) -> None:
    """
    Test get_manager_level in the case where the OU is a "normal"
    unit, i.e. a unit where the name is not suffixed with _led-adm
    """

    # Arrange
    org_unit_manager = OrgUnitManagers(
        uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
        name="SomeUnit_leder",
        has_children=False,
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
        has_children=False,
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
            "org_units": {
                "objects": [
                    {
                        "validities": [
                            {
                                "org_unit_level_uuid": "891603db-cc28-6ed2-6d48-25e14d3f142f"
                            }
                        ]
                    }
                ]
            }
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
