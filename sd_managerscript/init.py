# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from gql import gql
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient

from .queries import QUERY_ORG, MANAGERLEVEL_QUERY
from .util import query_graphql

QUERY_FACET = gql(
    """
    query ($user_key: [String!]){
        facets (user_keys: $user_key) {
            uuid
        }
    }
    """
)


async def get_organisation(gql_client: PersistentGraphQLClient) -> UUID:
    r = await gql_client.execute(QUERY_ORG)
    return UUID(r["org"]["uuid"])


async def get_facet_uuid(
    gql_client: PersistentGraphQLClient, user_key: str
) -> UUID:
    r = await gql_client.execute(
        QUERY_FACET, variable_values={"user_key": user_key}
    )
    return UUID(one(r["facets"])["uuid"])


async def get_missing_manager_level_classes(
    gql_client: PersistentGraphQLClient, manager_level_uuids: list[UUID]
) -> list[UUID]:
    """
    Check if all manager level classes exist and return a list of the potentially
    missing manager level classes.

    Args:
        gql_client: GraphQL client
        manager_level_uuids: list of manager_level class UUIDs we need to verify exist.
    Returns:
        List of UUIDs of the classes we need to create, hence they didn't exist in system
    """
    manager_levels = list(map(str, manager_level_uuids))

    r = await gql_client.execute(MANAGERLEVEL_QUERY, variable_values={"uuids": manager_levels})

    existing_class_uuids = map(lambda _class: _class["uuid"], r.get("classes", []))
    missing_class_uuids_strings = filter(lambda uuid: uuid not in existing_class_uuids, manager_levels)
    missing_class_uuids = map(UUID, missing_class_uuids_strings)

    return list(missing_class_uuids)
