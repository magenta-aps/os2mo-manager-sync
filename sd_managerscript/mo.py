# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from uuid import UUID

import structlog
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .models import EngagementFrom
from .queries import QUERY_ENGAGEMENTS
from .util import query_graphql

logger = structlog.get_logger()


async def get_active_engagements(
    gql_client: PersistentGraphQLClient, employee_uuid: UUID
) -> EngagementFrom:
    """
    Checks the manager has an active engagement and returns the latest, if any.

    Args:
        gql_client: GraphQL client
        employee_uuid: UUID for the employee we want to fetch engagements for.
    Returns:
        dict: dict with employee uuid and engagement from date.

    """

    variables = {"uuid": employee_uuid}
    engagements = await query_graphql(gql_client, QUERY_ENGAGEMENTS, variables)
    logger.debug("Engagements fetched.", response=engagements)
    engagement_from = None

    if engagements["engagements"]:
        latest_engagement = max(
            engagements["engagements"],
            key=lambda eng: datetime.fromisoformat(
                one(eng["objects"])["validity"]["from"]
            ),
        )

        # We add "from date" for lateste engagement to compare with other potential managers
        engagement_from = one(latest_engagement["objects"])["validity"]["from"]

    return EngagementFrom(employee_uuid=employee_uuid, engagement_from=engagement_from)
