# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from uuid import uuid4, UUID

from sd_managerscript.init import get_organisation, get_facet_uuid, \
    get_missing_manager_level_classes
from sd_managerscript.queries import MANAGERLEVEL_QUERY


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


async def test_get_missing_manager_level_classes() -> None:
    # Arrange
    mock_gql_client = AsyncMock()
    mock_execute = AsyncMock(return_value={
        "classes": [{"uuid": "afc5077b-bea5-4873-806e-6129d48be765"}]
    })
    mock_gql_client.execute = mock_execute

    manager_level_uuids = [
        UUID("afc5077b-bea5-4873-806e-6129d48be765"),
        UUID("dcd3f94b-dff5-4729-86df-a9dfc037b078"),
    ]
    manager_level_str = list(map(str, manager_level_uuids))

    # Act
    returned_data = await get_missing_manager_level_classes(mock_gql_client, manager_level_uuids)

    # Assert
    assert returned_data == [UUID("dcd3f94b-dff5-4729-86df-a9dfc037b078")]
    mock_execute.assert_awaited_once_with(
        MANAGERLEVEL_QUERY, variable_values={"uuids": manager_level_str}
    )
