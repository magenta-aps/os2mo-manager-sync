# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from unittest.mock import AsyncMock
from unittest.mock import patch

from gql import gql  # type: ignore

from sd_managerscript.util import query_graphql
from sd_managerscript.util import query_org_unit
from tests.test_data.sample_test_data import get_org_unit_models_sample  # type: ignore

QUERY_ROOT_ORG_UNIT = gql(
    """query ($uuids: [UUID!]!) {org_units (uuids: $uuids) {uuid}}"""
)

MUTATOR_TERMINATE_MANAGER_BY_UUID = gql(
    """mutation ($input: ManagerTerminateInput!){
            manager_terminate(input: $input){
                uuid
            }
        }"""
)


async def test_query_graphql() -> None:
    gql_client = AsyncMock()
    query = QUERY_ROOT_ORG_UNIT
    variables = {"uuid": "08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"}

    await query_graphql(gql_client, query, variables)

    gql_client.execute.assert_called_once_with(query, variable_values=variables)


@patch("sd_managerscript.util.query_graphql")
async def test_query_org_unit(mock_query_gql: AsyncMock) -> None:
    """Test we can convert graphql payload to org_unit models in query_org_unit"""

    sample_data, expected_org_units = get_org_unit_models_sample()
    mock_query_gql.return_value = sample_data
    gql_client = AsyncMock()
    query = QUERY_ROOT_ORG_UNIT
    variables = {"uuid": "08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"}

    returned_org_units = await query_org_unit(gql_client, query, variables)

    assert returned_org_units == expected_org_units


async def test_execute_mutator() -> None:
    gql_client = AsyncMock()
    query = MUTATOR_TERMINATE_MANAGER_BY_UUID
    variables = {"uuid": "08eaf849-e9f9-53e0-b6b9-3cd45763ecbb", "to": "2022-10-12"}

    await query_graphql(gql_client, query, variables)

    gql_client.execute.assert_called_once_with(query, variable_values=variables)
