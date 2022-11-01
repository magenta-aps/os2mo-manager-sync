# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# from typing import Any
from typing import Any

import structlog
from gql import gql  # type: ignore
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

logger = structlog.get_logger()

KOMMUNE = "Kolding Kommune"
ORG_UNITS = "org_units"

QUERY_ORG = gql("query {org { uuid }}")

QUERY_ROOT_ORG_UNIT = gql(
    """query ($user_keys: [String!]!) {org_units (user_keys: $user_keys) {uuid}}"""
)

# QUERY_ORG_UNITS = gql("query($uuid: [UUID!]!){org_units (uuids: $uuid){uuid}}")

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
                }
            }
        }
    }
"""
)


async def query_graphql(
    gql_client: PersistentGraphQLClient, query: str, variables: dict
) -> Any:
    """Graphql query. Returns List[Dict]"""

    """
    query: str - String for grapqhql query.
    variables: str - Input formatted as json.

    Returns: List[Dict] - List of alle the objects returned by the query.
    """
    return await gql_client.execute(query, variable_values=variables)


async def traverse_org_units(
    gql_client: PersistentGraphQLClient, input_org_unit: dict
) -> list[dict] | None:
    """Traverse through all org_units under passed UUID"""

    root_uuid = {"uuid": one(input_org_unit["objects"])["uuid"]}

    data = await query_graphql(gql_client, QUERY_ORG_UNITS, root_uuid)
    leder_org_units = []
    next_org_units = list(
        filter(lambda ou: one(ou["objects"])["child_count"] > 0, data["org_units"])
    )
    leder_org_units += list(
        filter(
            lambda ou: one(ou["objects"])["name"].lower().strip()[-6:] == "_leder",
            data["org_units"],
        )
    )
    leder_org_units += [
        await traverse_org_units(gql_client, org_unit) for org_unit in next_org_units
    ]
    return leder_org_units


async def update_mo_managers(gql_client: PersistentGraphQLClient) -> None:

    logger.msg("Getting org-units...")
    variables = {"user_keys": KOMMUNE}
    root_org_unit = await query_graphql(gql_client, QUERY_ROOT_ORG_UNIT, variables)
    root_org_unit["objects"] = list(root_org_unit.pop("org_units"))

    # Return value removed to avoid MyPy and Flake8 error
    _ = await traverse_org_units(gql_client, root_org_unit)
