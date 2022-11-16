# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import no_type_check

from more_itertools import one  # type: ignore
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .models import OrgUnitManagers  # type: ignore


@no_type_check
async def query_graphql(
    gql_client: PersistentGraphQLClient, query: str, variables: dict
) -> dict[str, list]:
    """Graphql query. Returns List[Dict]"""

    """
    query: str - String for grapqhql query.
    variables: str - Input formatted as json.

    Returns: dict[str, list[dict[str, Any]]]
        -Dict with list of all the objects returned by the query.
    """
    return await gql_client.execute(query, variable_values=variables)


async def query_org_unit(
    gql_client: PersistentGraphQLClient, query: str, variables: dict
) -> list[OrgUnitManagers]:
    """Calling graphql function and turn payload into list of org-unit objects"""

    org_unit_dicts = await query_graphql(gql_client, query, variables)

    ou_model_list = [
        OrgUnitManagers.parse_obj(one(org_unit["objects"]))
        for org_unit in org_unit_dicts["org_units"]
    ]
    return ou_model_list
