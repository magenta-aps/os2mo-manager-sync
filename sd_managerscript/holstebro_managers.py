# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from asyncio import gather
from datetime import datetime
from datetime import timedelta
from uuid import UUID

import structlog
from fastapi.encoders import jsonable_encoder
from gql import gql  # type: ignore
from more_itertools import collapse
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .exceptions import ConflictingManagers
from .models import EngagementFrom
from .models import OrgUnitManagers
from .util import ConflictingManagers
from .util import execute_mutator
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

QUERY_ENGAGEMENTS = gql(
    """
        query ($uuid: [UUID!]!){
            engagements (employees: $uuid){
                objects{
                    validity{
                        from
                        to
                    }
                }
            }
        }
    """
)

CURRENT_MANAGER = gql(
    """
    query ($uuid: [UUID!]!){
  org_units(uuids: $uuid) {
    objects {
      managers {
        uuid
      }
    }
  }
}
"""
)

UPDATE_MANAGER = gql(
    """
        mutation UpdateManager($input: ManagerUpdateInput!) {
            manager_update(input: $input) {
                uuid
            }
        }
    """
)

CREATE_MANAGER = gql(
    """
        mutation CreateManager($input: ManagerCreateInput!) {
            manager_create(input: $input) {
                uuid
            }
        }
    """
)

MANAGER_TERMINATE = gql(
    """
        mutation ($input: ManagerTerminateInput!){
            manager_terminate(input: $input){
                uuid
            }
        }
    """
)

ASSOCIATION_QUERY = gql(
    """
        query ($employees: [UUID!]!, $org_units: [UUID!]!){
            associations(employees: $employees, org_units: $org_units) {
                uuid
            }
        }
    """
)

ASSOCIATION_TERMINATE = gql(
    """
        mutation($input: AssociationTerminateInput!){
            association_terminate(input: $input){
                uuid
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

    manager_list += [
        await get_manager_org_units(  # type: ignore
            gql_client, UUID(jsonable_encoder(org_unit)["uuid"])
        )
        for org_unit in child_org_units
    ]
    managers = list(collapse(manager_list, base_type=OrgUnitManagers))
    return managers


async def terminate_association(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID, employee_uuid: UUID
) -> None:
    """
    Terminates association with "_leder" org_unit (updates end date).

    Args:
        gql_client: GraphQL client
        org_unit_uuid: UUID of the org_unit related to the association
        employee_uuid: UUID of the employee related to the association
    Returns:
        Nothing
    """

    query_input = {"input": {"employees": employee_uuid, "org_units": org_unit_uuid}}

    association_uuid = await query_graphql(gql_client, ASSOCIATION_QUERY, query_input)

    input = {
        "input": {
            "uuid": str(association_uuid),
            "to": (datetime.today() - timedelta(days=1)).date().isoformat(),
        }
    }

    await execute_mutator(gql_client, ASSOCIATION_TERMINATE, input)


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

    if engagements["engagements"]:
        latest_engagement = max(
            engagements["engagements"],
            key=lambda eng: datetime.fromisoformat(
                one(eng["objects"])["validity"]["from"]
            ),
        )

        # We add from date for lateste engagement to compare with other potential managers
        engagement_from = one(latest_engagement["objects"])["validity"]["from"]
        return EngagementFrom.parse_obj(
            {"employee_uuid": employee_uuid, "engagement_from": engagement_from}
        )

    return EngagementFrom.parse_obj(
        {"employee_uuid": employee_uuid, "engagement_from": None}
    )

    if any(managers):
        print(f"++++++++++++++++++ managers {managers}")
        # We check there's max one employee with the latest from date or we raise an exception
        date_list = [datetime.fromisoformat(man["eng_from"]) for man in managers]
        if date_list.count(max(date_list)) > 1:
            raise Exception(
                "Two or more employees have same engagement from"
                f"date, in org-unit with uuid: {org_unit_dict['uuid']}"
            )

async def filter_managers(
    gql_client: PersistentGraphQLClient, org_unit: OrgUnitManagers
) -> OrgUnitManagers:
    """
    Checks potential managers are actually employeed.
    The manager with latest hiring date is returned inside org-unit object.
    If more than one employee has the latest engagement date we raise an exception.
    If none of the potential managers have an engagement, Managers list will be returned empty.

    Args:
        gql_client: GraphQL client
        org_unit: OrgUnitManager object
    Returns:
        OrgUnitManager object
    """

    # get active engagements for each manager
    org_unit_dict = jsonable_encoder(org_unit)

    active_engagements = await gather(
        *map(
            lambda manager: get_active_engagements(
                gql_client, manager["employee_uuid"]
            ),
            org_unit_dict["managers"],
        )
    )

    # If manager doesn't have an engagement: associations with org-unit gets terminated.
    filtered_engagements = []
    for engagement in active_engagements:
        if not engagement["engagement_from"]:
            await terminate_association(
                gql_client, org_unit_dict["uuid"], engagement["employee_uuid"]
            )
        else:
            filtered_engagements.append(engagement)

    # Get manager with latests engagement from date.
    if filtered_engagements:
        # We check there's max one employee with the latest from date or we raise an exception
        date_list = [
            datetime.fromisoformat(eng_dict["engagement_from"])
            for eng_dict in filtered_engagements
        ]
        if date_list.count(max(date_list)) > 1:
            raise ConflictingManagers(
                "Two or more employees have same engagement from"
                f"date, in org-unit with uuid: {org_unit_dict['uuid']}"
            )

        filtered_manager = max(
            filtered_engagements,
            key=lambda eng_dict: datetime.fromisoformat(eng_dict["engagement_from"]),
        )
        managers = list(
            filter(
                lambda manager: manager["employee_uuid"]
                == filtered_manager["employee_uuid"],
                org_unit_dict["managers"],
            )
        )

    else:
        managers = []

    org_unit_dict["managers"] = managers

    return OrgUnitManagers.parse_obj(org_unit_dict)


async def update_mo_managers(
    gql_client: PersistentGraphQLClient, root_uuid: UUID
) -> None:
    """Main function for finding and updating managers"""

    logger.msg("Getting org-units...")
    variables = {"uuids": str(root_uuid)}
    root_org_unit = await query_graphql(gql_client, QUERY_ROOT_ORG_UNIT, variables)
    root_org_unit_uuid = UUID(one(root_org_unit["org_units"])["uuid"])
    manager_org_units = await get_manager_org_units(gql_client, root_org_unit_uuid)

    org_units = [
        await filter_managers(gql_client, org_unit) for org_unit in manager_org_units
    ]

    print(
        org_units
    )  # just to avoid MyPy errors. Will be replaced with call to function in next MR
