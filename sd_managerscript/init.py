# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from gql import gql  # type: ignore
from more_itertools import one
from pydantic import BaseModel
from raclients.graph.client import PersistentGraphQLClient  # type: ignore
from ramodels.mo import Validity  # type: ignore

from .queries import QUERY_ORG

QUERY_MANAGER_CLASSES = gql(
    """
    query Facet {
        facets(filter: { user_keys: "manager_level" }) {
            objects {
                validities {
                    classes {
                       name
                    }
                    uuid
                }
            }
        }
    }
    """
)

MANAGER_LEVEL_CREATE = gql(
    """
        mutation ($input: ClassCreateInput!){
            class_create (input: $input){
                uuid
            }
        }
    """
)

logger = structlog.get_logger()


class ManagerLevel(BaseModel):
    """
    Model used to load mandatory manager levels from the ENV
    """

    name: str
    user_key: str
    uuid: UUID | None = None


async def get_organisation(gql_client: PersistentGraphQLClient) -> UUID:
    """
    Get the MO organisation.

    Args:
        gql_client: GraphQL client used to call MO
    Returns:
         UUID of the MO organisation
    """

    r = await gql_client.execute(QUERY_ORG)
    uuid = UUID(r["org"]["uuid"])
    logger.info("Got org UUID", uuid=uuid)
    return uuid


async def get_manager_level_facet_and_classes(
    gql_client: PersistentGraphQLClient,
) -> tuple[UUID, list[str]]:
    """
    Get the UUID of the manager level facet and all the corresponding manager level
    classes already existing in MO.

    Args:
        gql_client: GraphQL client used to call MO
    Returns:
        Tuple containing the manager level facet UUID and a list of UUIDs of the
        manager level classes in MO.
    """

    r = await gql_client.execute(QUERY_MANAGER_CLASSES)
    facets = r.get("facets", {})
    facet = one(one(facets["objects"])["validities"])
    classes = facet.get("classes", [])
    existing_class_names = list(map(lambda _class: _class["name"], classes))  # type: ignore

    logger.info(
        "Manager level facet and classes",
        uuid=UUID(facet["uuid"]),
        existing_class_names=existing_class_names,
    )

    return UUID(facet["uuid"]), existing_class_names


async def create_manager_level(
    gql_client: PersistentGraphQLClient,
    facet_uuid: UUID,
    name: str,
    user_key: str,
    uuid: UUID | None = None,
    validity: Validity = {"from": "1900-01-01"},
) -> UUID:
    """
    Create a manager level class in MO.

    Args:
        gql_client: GraphQL client used to call MO
        facet_uuid: UUID of the manager level facet in MO
        name: Name of the manager level class
        user_key: User key of the manager level class
        uuid: UUID of the manager level class
    Returns:
        UUID of the created manager level class
    """

    gql_input = {
        "facet_uuid": str(facet_uuid),
        "name": name,
        "user_key": user_key,
        "validity": validity,
    }
    if uuid is not None:
        gql_input["uuid"] = str(uuid)

    r = await gql_client.execute(
        MANAGER_LEVEL_CREATE, variable_values={"input": gql_input}
    )
    uuid = UUID(r["class_create"]["uuid"])
    logger.info("Create manager level", name=name, user_key=user_key, uuid=uuid)

    return uuid


async def create_missing_manager_levels(
    gql_client: PersistentGraphQLClient, mandatory_manager_levels: list[ManagerLevel]
) -> None:
    """
    Create the missing manager level classes in MO, i.e. the manager
    levels specificed in the ENV that do not already exist in MO.

    Args:
         gql_client: GraphQL client used to call MO
         mandatory_manager_levels: The mandatory manager levels that
           should exist in MO
    """

    logger.info("Creating missing manager levels...")

    facet_uuid, existing_manager_levels = await get_manager_level_facet_and_classes(
        gql_client
    )
    missing_manager_levels = list(
        filter(
            lambda ml: ml.name not in existing_manager_levels, mandatory_manager_levels
        )
    )

    for manager_level in missing_manager_levels:
        await create_manager_level(
            gql_client,
            facet_uuid,
            manager_level.name,
            manager_level.user_key,
            manager_level.uuid,
        )

    logger.info("Finished creating manager levels")
