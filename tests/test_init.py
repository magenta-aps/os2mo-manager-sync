# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from uuid import uuid4, UUID

from gql import gql

from sd_managerscript.init import get_organisation, get_facet_uuid, \
    get_manager_level_facet_and_classes, QUERY_MANAGER_CLASSES
from sd_managerscript.queries import MANAGER_LEVEL_QUERY


async def test_get_organisation():
    # Arrange
    org_uuid = uuid4()
    mock_gql_client = AsyncMock()
    mock_gql_client.execute.return_value = {"org": {"uuid": str(org_uuid)}}

    # Act
    _uuid = await get_organisation(mock_gql_client)

    # Assert
    assert _uuid == org_uuid


async def test_get_facet_uuid():
    # Arrange
    facet_uuid = uuid4()
    mock_gql_client = AsyncMock()
    mock_gql_client.execute.return_value = {
        "facets": [{"uuid": str(facet_uuid)}]
    }
    # Act
    _uuid = await get_facet_uuid(mock_gql_client, "manager_level")

    # Assert
    assert _uuid == facet_uuid


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
