# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from asyncio import gather
from datetime import datetime
from datetime import timedelta
from functools import partial
from uuid import UUID
from uuid import uuid4

import structlog
from fastapi.encoders import jsonable_encoder
from gql import gql  # type: ignore
from more_itertools import collapse
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .exceptions import ConflictingManagers
from .models import EngagementFrom
from .models import Manager
from .models import OrgUnitManagers
from .util import execute_mutator
from .util import query_graphql
from .util import query_org_unit
from sd_managerscript.managerlevel import get_managerlevel_mapping

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
                child_count
                associations {
                    uuid
                    employee_uuid
                    validity{
                        from
                        to
                    }
                }
                parent{
                    uuid
                    name
                    parent_uuid
                    org_unit_level_uuid
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
    logger.debug("Org-units returned from query", response=data)
    child_org_units = filter(lambda ou: jsonable_encoder(ou)["child_count"] > 0, data)

    manager_list = list(
        filter(
            lambda ou: (jsonable_encoder(ou)["name"].lower().strip()[-6:] == "_leder")
            and (jsonable_encoder(ou)["name"].strip()[:2] != "Ø_"),
            data,
        )
    )
    logger.debug("Manager list up until now...", org_units=manager_list)
    manager_list += [
        await get_manager_org_units(  # type: ignore
            gql_client, UUID(jsonable_encoder(org_unit)["uuid"])
        )
        for org_unit in child_org_units
    ]
    managers = list(collapse(manager_list, base_type=OrgUnitManagers))
    return managers


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

    input = {
        "input": {
            "uuid": str(association_uuid),
            "to": (datetime.today() - timedelta(days=1)).date().isoformat(),
        }
    }

    await execute_mutator(gql_client, ASSOCIATION_TERMINATE, input)
    logger.info("Association terminated!", input=input)


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

    if engagements["engagements"]:
        latest_engagement = max(
            engagements["engagements"],
            key=lambda eng: datetime.fromisoformat(
                one(eng["objects"])["validity"]["from"]
            ),
        )

        # We add "from date" for lateste engagement to compare with other potential managers
        engagement_from = one(latest_engagement["objects"])["validity"]["from"]
        return EngagementFrom.parse_obj(
            {"employee_uuid": employee_uuid, "engagement_from": engagement_from}
        )

    return EngagementFrom.parse_obj(
        {"employee_uuid": employee_uuid, "engagement_from": None}
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
            lambda association: get_active_engagements(
                gql_client, association["employee"]
            ),
            org_unit_dict["associations"],
        )
    )

    # Filter away non-active engagements.
    filtered_engagements = [
        engagement for engagement in active_engagements if engagement["engagement_from"]
    ]

    # If any managers with engagements. -Get manager with latests engagement from date.
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
        associations = list(
            filter(
                lambda association: association["employee"]
                == filtered_manager["employee_uuid"],
                org_unit_dict["associations"],
            )
        )

        redundant_associations = [
            UUID(asso["uuid"])
            for asso in org_unit_dict["associations"]
            if asso["uuid"] != one(associations)["uuid"]
        ]
        logger.debug(
            "Associations collected.",
            associations=associations,
            redundant_associations=redundant_associations,
        )
    else:
        associations = []
        redundant_associations = [
            UUID(asso["uuid"]) for asso in org_unit_dict["associations"]
        ]
        logger.debug(
            "No associations collected.", redundant_associations=redundant_associations
        )
    # Terminate associations for all other employees in the
    # "_leder" org-unit, apart from the selected manager.
    [
        await terminate_association(gql_client, association_uuid)  # type: ignore
        for association_uuid in redundant_associations
    ]

    org_unit_dict["associations"] = associations

    return OrgUnitManagers.parse_obj(org_unit_dict)


async def get_current_manager(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID
) -> UUID | None:
    """
    Checks if org-unit has a manager and returns UUID of that manager posistion,
    otherwise returns new uuid.

    Args:
        gql_client: GraphQL client
        org_unit_uuid: UUID - uuid og the org-unit we want to fetch the manager from.
    Retuns:
        UUID or None - UUID if manager position is present otherwise None
    """
    variables = {"uuid": str(org_unit_uuid)}
    ou_manager = await query_graphql(gql_client, CURRENT_MANAGER, variables)
    managers = one(one(ou_manager["org_units"])["objects"])["managers"]
    if managers:
        logger.debug("Manager found", manager=managers)
        return UUID(one(managers)["uuid"])

    return None


async def create_manager_object(
    gql_client: PersistentGraphQLClient, org_unit: OrgUnitManagers
) -> Manager:
    """
    Create Manager object for updating and creating managers

    Args:
        gql_client: GraphQL client
        org_unit: OrgUnitManagers object
    Returns:
        Manager object
    """

    managertype_dict = get_managerlevel_mapping()

    org_unit_dict = jsonable_encoder(org_unit)

    manager_dict: dict[str, str | UUID | dict] = {}
    manager_dict["uuid"] = uuid4()
    manager_dict["employee"] = one(org_unit_dict["associations"])["employee"]

    # UUID for managertype "Leder" which is the same for every manager
    manager_dict["manager_type"] = {
        "uuid": UUID("75fee2b6-f405-4c77-b62e-32421c2e43d5")
    }
    manager_dict["validity"] = {
        "from": one(org_unit_dict["associations"])["validity"]["from"],
        "to": None,
    }

    # Assign manager level accordingly to "NYx" org_unit_level_uuid
    # If parent org-unit name is ending with "led-adm"
    # we fetch org_unit_level_uuid form parent org-unit
    if org_unit_dict["parent"]["name"].strip()[-7:] == "led-adm":
        variables = {"uuid": str(org_unit_dict["uuid"])}
        data = await query_org_unit(gql_client, QUERY_ORG_UNITS, variables)

        manager_dict["manager_level"] = {
            "uuid": UUID(
                managertype_dict[
                    jsonable_encoder(data)["parent"]["org_unit_level_uuid"]
                ]
            )
        }

    else:
        manager_dict["manager_level"] = {
            "uuid": UUID(
                managertype_dict[org_unit_dict["parent"]["org_unit_level_uuid"]]
            )
        }
    logger.info(f"Manager object created: {manager_dict}")
    return Manager.parse_obj(manager_dict)


async def update_manager_object(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID, manager_obj: Manager
) -> None:
    """
    Checks if there exists a manager posistion at parent org-unit.
    If theres does. Updates the manager posistion with employee
    If there doesn't: Creates new manager position with employee

    Assign manager to parent org_unit

    Args:
        gql_client: GraphQL client
        org_unit_uuid: uuid of the org-unit we want to assign the manager to
    Returns:
        Nothing
    """
    manager_dict = jsonable_encoder(manager_obj)

    current_manager_uuid = await get_current_manager(gql_client, org_unit_uuid)

    if current_manager_uuid:
        manager_dict["uuid"] = current_manager_uuid
        variables = {"input": manager_dict}
        await execute_mutator(gql_client, UPDATE_MANAGER, variables)
        logger.info(f"Manager updated: {manager_dict}")
    else:
        variables = {"input": manager_dict}
        await execute_mutator(gql_client, CREATE_MANAGER, variables)
        logger.info(f"Manager created: {manager_dict}")


async def update_manager(
    gql_client: PersistentGraphQLClient, org_unit: OrgUnitManagers
) -> None:
    """
    Create manager payload and send request to update manager in relevant org-units

    Args:
        gql_client: GraphQL client
        org_unit: OrgUnitManagers object
    Returns:
        Nothing
    """
    manager: Manager = await create_manager_object(gql_client, org_unit)
    await update_manager_object(gql_client, org_unit.parent.uuid, manager)

    # If parent org-unit has "led-adm" in name,
    # it's parent org-unit will also have the manager assigned
    if org_unit.parent.name.strip()[-7:] == "led-adm":
        await update_manager_object(gql_client, org_unit.parent.parent_uuid, manager)


async def update_mo_managers(
    gql_client: PersistentGraphQLClient, root_uuid: UUID
) -> None:
    """Main function for selecting and updating managers"""

    logger.msg("Getting root-org...")
    variables = {"uuids": str(root_uuid)}
    root_org_unit = await query_graphql(gql_client, QUERY_ROOT_ORG_UNIT, variables)
    root_org_unit_uuid = UUID(one(root_org_unit["org_units"])["uuid"])

    logger.msg("Getting org-units...")
    manager_org_units = await get_manager_org_units(gql_client, root_org_unit_uuid)

    logger.info("Filter Managers")
    org_units = [
        await filter_managers(gql_client, org_unit) for org_unit in manager_org_units
    ]
    logger.info("Updating Managers")
    map(partial(update_manager, gql_client), org_units)
    logger.info("Updating managers complete!")
