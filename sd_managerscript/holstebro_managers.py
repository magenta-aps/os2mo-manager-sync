# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

import structlog
from fastapi.encoders import jsonable_encoder
from gql import gql  # type: ignore
from more_itertools import collapse
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .models import OrgUnitManagers
from .util import query_graphql
from .util import query_org_unit

logger = structlog.get_logger()

ORG_UNITS = "org_units"

QUERY_ORG = gql("query {org { uuid }}")

QUERY_ROOT_ORG_UNIT = gql(
    """query ($uuids: [UUID!]!) {org_units (uuids: $uuids) {uuid}}"""
)

QUERY_ORG_UNITS = gql(
    """
    query ($uuid: [UUID!]!){
        org_units (parents: $uuid){
            objects {
                uuid
                name
                parent_uuid
                child_count
                managers {
                    uuid
                    employee_uuid
                    manager_level {
                        name
                        uuid
                    }
                    manager_type {
                        name
                        uuid
                    }
                    validity{
                        to
                        from
                    }
                }
            }
        }
    }
"""
)


async def get_manager_org_units(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID
) -> list[OrgUnitManagers]:
    """
    Recursive function, traverse through all org_units and return '_leder' org-units

    Args:
        Graphql client
        org_unit_uuid: UUID
    Returns:
        managers: list of '_leder' OrgUnitManagers

    """

    variables = {"uuid": str(org_unit_uuid)}

    data = await query_org_unit(gql_client, QUERY_ORG_UNITS, variables)

    child_org_units = filter(lambda ou: jsonable_encoder(ou)["child_count"] > 0, data)

    manager_list = list(
        filter(
            lambda ou: jsonable_encoder(ou)["name"].lower().strip()[-6:] == "_leder",
            data,
        )
    )
    # TODO: Fix MyPy error:
    # "List comprehension has incompatible type List[List[OrgUnitManagers]];
    # expected List[OrgUnitManagers]"
    manager_list += [
        await get_manager_org_units(  # type: ignore
            gql_client, UUID(jsonable_encoder(org_unit)["uuid"])
        )
        for org_unit in child_org_units
    ]

    managers = list(collapse(manager_list, base_type=OrgUnitManagers))

    return managers


async def update_mo_managers(
    gql_client: PersistentGraphQLClient, root_uuid: UUID
) -> None:
    """Main function for finding and updating managers"""

    logger.msg("Getting org-units...")
    variables = {"uuids": str(root_uuid)}
    root_org_unit = await query_graphql(gql_client, QUERY_ROOT_ORG_UNIT, variables)
    root_org_unit_uuid = UUID(one(root_org_unit["org_units"])["uuid"])

    managers = await get_manager_org_units(gql_client, root_org_unit_uuid)
    print(f"**************************** MANAGERS {managers}")
