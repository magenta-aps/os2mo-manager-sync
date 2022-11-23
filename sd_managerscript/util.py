# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import no_type_check

from more_itertools import one  # type: ignore
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .models import OrgUnitManagers  # type: ignore


class ConflictingManagers(Exception):
    pass


@no_type_check
async def query_graphql(
    gql_client: PersistentGraphQLClient, query: str, variables: dict
) -> dict[str, list]:
    """Graphql query. Returns List[Dict]

    Args:
        gql_client: GraphQL client
        query: String for grapqhql query.
        variables: Values to query over.

    Returns:
        dict[str, list[dict[str, Any]]]
    """
    return await gql_client.execute(query, variable_values=variables)


async def query_org_unit(
    gql_client: PersistentGraphQLClient, query: str, variables: dict
) -> list[OrgUnitManagers]:
    """
    Calling graphql function and turn payload into list of org-unit objects

    Args:
        gql_client: GraphQL client
        query: String for grapqhql query.
        variables: Values to query over.
    Returns:
        list[OrgUnitManagers]
    """

    org_unit_dicts = await query_graphql(gql_client, query, variables)

    ou_model_list = [
        OrgUnitManagers.parse_obj(one(org_unit["objects"]))
        for org_unit in org_unit_dicts["org_units"]
    ]
    return ou_model_list


async def execute_mutator(
    gql_client: PersistentGraphQLClient, mutate_param: str, variables: dict
) -> None:
    """Generic graphql mutation.

    Args:
        mutate_param: The object you want to change. Eg. "org-units"
        variables: Dict of parameters to input to mutator.
    Returns:
        uuid: uuid of the modified object
    """

    _ = await gql_client.execute(mutate_param, variables)
