# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from gql import gql
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient

from .queries import QUERY_ORG, MANAGER_LEVEL_QUERY


async def get_organisation(gql_client: PersistentGraphQLClient) -> UUID:
    r = await gql_client.execute(QUERY_ORG)
    return UUID(r["org"]["uuid"])


async def get_facet_uuid(
    gql_client: PersistentGraphQLClient, user_key: str
) -> UUID:
    QUERY_FACET = gql(
        """
        query ($user_key: [String!]){
            facets (user_keys: $user_key) {
                uuid
            }
        }
        """
    )

    r = await gql_client.execute(
        QUERY_FACET, variable_values={"user_key": user_key}
    )

    return UUID(one(r["facets"])["uuid"])


QUERY_MANAGER_CLASSES = gql(
    """
    query Facet {
      facets(user_keys: "manager_level") {
        classes {
          name
        }
        uuid
      }
    }
    """
)


async def get_missing_manager_level_classes_and_facet_uuid(
    gql_client: PersistentGraphQLClient, manager_levels: list[str]
) -> (list[str], UUID):
    """
    Check if all manager level classes exist and return a list of the potentially
    missing manager level classes.

    Args:
        gql_client: GraphQL client
        manager_level_uuids: list of manager_level class UUIDs we need to verify exist.
    Returns:
        List of UUIDs of the classes we need to create, hence they didn't exist in system
    """

    r = await gql_client.execute(QUERY_MANAGER_CLASSES)

    facet = one(r["facets"])
    classes = facet.get("classes", [])
    existing_class_names = tuple(map(lambda _class: _class["name"], classes))
    missing_class_names = list(filter(lambda name: name not in existing_class_names, manager_levels))

    return missing_class_names, UUID(facet["uuid"])
