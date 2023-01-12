# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from raclients.graph.client import PersistentGraphQLClient

from .queries import QUERY_ORG


async def get_organisation(gql_client: PersistentGraphQLClient) -> UUID:
    r = await gql_client.execute(QUERY_ORG)
    return UUID(r["org"]["uuid"])
