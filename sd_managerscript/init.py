# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from gql import gql
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient

from .queries import QUERY_ORG

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
