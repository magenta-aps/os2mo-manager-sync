# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from gql import gql
from more_itertools import one
from pydantic import BaseModel
from raclients.graph.client import PersistentGraphQLClient

from .queries import QUERY_ORG, MANAGERLEVEL_CREATE


logger = structlog.get_logger()


class ManagerLevel(BaseModel):
    name: str
    user_key: str
    uuid: UUID | None = None


async def get_organisation(gql_client: PersistentGraphQLClient) -> UUID:
    r = await gql_client.execute(QUERY_ORG)
    uuid = UUID(r["org"]["uuid"])
    logger.info("Got org UUID", uuid=uuid)
    return uuid


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


async def get_manager_level_facet_and_classes(
    gql_client: PersistentGraphQLClient
) -> (UUID, list[str]):
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
    existing_class_names = list(map(lambda _class: _class["name"], classes))

    logger.info(
        "Manager level facet and classes",
        uuid=UUID(facet["uuid"]),
        existing_class_names=existing_class_names
    )

    return UUID(facet["uuid"]), existing_class_names


async def create_manager_level(
    gql_client: PersistentGraphQLClient,
    facet_uuid: UUID,
    name: str,
    org_uuid: UUID,
    user_key: str,
    uuid: UUID | None = None
) -> UUID:
    gql_input = {
        "facet_uuid": str(facet_uuid),
        "name": name,
        "org_uuid": str(org_uuid),
        "user_key": user_key
    }
    if uuid is not None:
        gql_input["uuid"] = str(uuid)

    r = await gql_client.execute(MANAGERLEVEL_CREATE, variable_values={
        "input": gql_input
    })
    uuid = UUID(r["class_create"]["uuid"])
    logger.info("Create manager level", name=name, user_key=user_key, uuid=uuid)

    return uuid


async def create_missing_manager_levels(
    gql_client, mandatory_manager_levels: list[ManagerLevel]
) -> None:
    logger.info("Creating missing manager levels...")

    org_uuid = await get_organisation(gql_client)
    facet_uuid, existing_manager_levels = await get_manager_level_facet_and_classes(gql_client)
    missing_manager_levels = list(filter(lambda ml: ml.name not in existing_manager_levels, mandatory_manager_levels))
    print(missing_manager_levels)
    for manager_level in missing_manager_levels:
        await create_manager_level(
            gql_client,
            facet_uuid,
            manager_level.name,
            org_uuid,
            manager_level.user_key,
            manager_level.uuid
        )

    logger.info("Finished creating manager levels")
