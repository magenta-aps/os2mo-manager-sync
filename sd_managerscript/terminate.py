# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from datetime import timedelta
from uuid import UUID

import structlog
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from sd_managerscript.queries import ASSOCIATION_TERMINATE
from sd_managerscript.queries import MANAGER_TERMINATE
from sd_managerscript.util import execute_mutator


logger = structlog.get_logger()


async def terminate_association(
    gql_client: PersistentGraphQLClient, association_uuid: UUID
) -> None:
    """
    Terminates association with "_leder" org_unit (updates end date).

    Args:
        gql_client: GraphQL client
        association_uuid: UUID of the association to terminate
    Returns:
        Nothing
    """

    input_ = {
        "input": {
            "uuid": str(association_uuid),
            "to": datetime.today().date().isoformat(),
        }
    }

    await execute_mutator(gql_client, ASSOCIATION_TERMINATE, input_)
    logger.info("Association terminated!", input=input_)


async def terminate_manager(
    gql_client: PersistentGraphQLClient, manager_uuid: UUID, dry_run: bool = False
) -> None:
    """
    Terminates manager role in parent org-unit (updates end date).

    Args:
        gql_client: GraphQL client
        manager_uuid: UUID of the association to terminate
        dry_run: If true, do not actually perform write operations to MO
    Returns:
        Nothing
    """

    # TODO: unit test for dry run

    input_ = {
        "input": {
            "uuid": str(manager_uuid),
            "to": (datetime.today() - timedelta(days=0)).date().isoformat(),
        }
    }

    if not dry_run:
        await execute_mutator(gql_client, MANAGER_TERMINATE, input_)
    logger.info("Manager terminated!", input=input_)
