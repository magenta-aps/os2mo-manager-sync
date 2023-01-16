# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from uuid import uuid4, UUID

from sd_managerscript.init import get_organisation, \
    get_manager_level_facet_and_classes, QUERY_MANAGER_CLASSES, \
    create_manager_level, ManagerLevel, create_missing_manager_levels
from sd_managerscript.queries import MANAGERLEVEL_CREATE

from tests.test_holstebro_managers import gql_client


async def test_get_organisation():
    # Arrange
    org_uuid = uuid4()
    mock_gql_client = AsyncMock()
    mock_gql_client.execute.return_value = {"org": {"uuid": str(org_uuid)}}

    # Act
    _uuid = await get_organisation(mock_gql_client)

    # Assert
    assert _uuid == org_uuid


async def test_get_manager_level_facet_and_classes() -> None:
    # Arrange
    mock_gql_client = AsyncMock()
    mock_execute = AsyncMock(return_value={
        "facets": [
            {
                "classes": [
                    {"name": "Niveau 1"},
                    {"name": "Niveau 2"},
                    {"name": "Niveau 3"}
                ],
                "uuid": "35d5d061-5d19-4584-8c5e-796309b87dfb"
            }
        ]
    })
    mock_gql_client.execute = mock_execute

    # Act
    returned_data = await get_manager_level_facet_and_classes(mock_gql_client)

    # Assert
    assert returned_data == (UUID("35d5d061-5d19-4584-8c5e-796309b87dfb"), ["Niveau 1", "Niveau 2", "Niveau 3"])
    mock_execute.assert_awaited_once_with(QUERY_MANAGER_CLASSES)


async def test_create_manager_level(gql_client) -> None:
    # Arrange
    org_uuid = uuid4()
    facet_uuid = uuid4()
    class_uuid = uuid4()

    mock_execute = AsyncMock(return_value={"class_create": {"uuid": str(class_uuid)}})
    gql_client.execute = mock_execute

    # Act
    create_manager_level_uuid = await create_manager_level(gql_client, facet_uuid, "Name", org_uuid, "name")

    # Assert
    assert class_uuid == create_manager_level_uuid
    mock_execute.assert_awaited_once_with(
        MANAGERLEVEL_CREATE, variable_values={
            "input": {
                "facet_uuid": str(facet_uuid),
                "name": "Name",
                "org_uuid": str(org_uuid),
                "user_key": "name"
            }
        })


async def test_create_manager_level_with_uuid(gql_client) -> None:
    # Arrange
    org_uuid = uuid4()
    facet_uuid = uuid4()
    class_uuid = uuid4()

    mock_execute = AsyncMock(return_value={"class_create": {"uuid": str(class_uuid)}})
    gql_client.execute = mock_execute

    # Act
    create_manager_level_uuid = await create_manager_level(gql_client, facet_uuid, "Name", org_uuid, "name", class_uuid)

    # Assert
    assert class_uuid == create_manager_level_uuid
    mock_execute.assert_awaited_once_with(
        MANAGERLEVEL_CREATE, variable_values={
            "input": {
                "facet_uuid": str(facet_uuid),
                "name": "Name",
                "org_uuid": str(org_uuid),
                "user_key": "name",
                "uuid": str(class_uuid)
            }
        })


async def test_create_missing_manager_levels() -> None:
    # Arrange
    org_uuid = uuid4()
    facet_uuid = uuid4()
    manager_level_1_uuid = uuid4()
    manager_level_3_uuid = uuid4()

    mock_execute = AsyncMock(side_effect=[
        {"org": {"uuid": str(org_uuid)}},
        {
            "facets": [
                {
                    "classes": [
                        {"name": "Niveau 1"},
                        {"name": "Niveau 2"},
                    ],
                    "uuid": str(facet_uuid)
                }
            ]
        },
        {"class_create": {"uuid": str(uuid4())}},
        {"class_create": {"uuid": str(uuid4())}}
    ])
    gql_client = AsyncMock()
    gql_client.execute = mock_execute

    mandatory_manager_levels = [
        ManagerLevel(name="Niveau 1", user_key="niveau 1", uuid=manager_level_1_uuid),
        ManagerLevel(name="Niveau 2", user_key="niveau 2"),
        ManagerLevel(name="Niveau 3", user_key="niveau 3", uuid=manager_level_3_uuid),
        ManagerLevel(name="Niveau 4", user_key="niveau 4"),
    ]

    # Act
    await create_missing_manager_levels(gql_client, mandatory_manager_levels)

    # Assert

    # One for getting the org UUID + one for getting existing facet and classes +
    # two for creating the two missing manager levels = 4
    assert 4 == mock_execute.await_count

    mock_execute.assert_any_await(MANAGERLEVEL_CREATE, variable_values={
        "input": {
            "facet_uuid": str(facet_uuid),
            "name": "Niveau 3",
            "org_uuid": str(org_uuid),
            "user_key": "niveau 3",
            "uuid": str(manager_level_3_uuid)
        }
    })
    mock_execute.assert_any_await(MANAGERLEVEL_CREATE, variable_values={
        "input": {
            "facet_uuid": str(facet_uuid),
            "name": "Niveau 4",
            "org_uuid": str(org_uuid),
            "user_key": "niveau 4"
        }
    })
