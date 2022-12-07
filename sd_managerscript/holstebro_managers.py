# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from asyncio import gather
from datetime import datetime
from datetime import timedelta
from uuid import UUID

import structlog
from fastapi.encoders import jsonable_encoder
from more_itertools import collapse
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore
from ramodels.mo._shared import Validity  # type: ignore

from .config import get_settings
from .exceptions import ConflictingManagers
from .models import EngagementFrom
from .models import Manager
from .models import ManagerLevel
from .models import ManagerType
from .models import OrgUnitManagers
from .util import execute_mutator
from .util import query_graphql
from .util import query_org_unit
from sd_managerscript.queries import ASSOCIATION_TERMINATE
from sd_managerscript.queries import CREATE_MANAGER
from sd_managerscript.queries import CURRENT_MANAGER
from sd_managerscript.queries import MANAGER_TERMINATE
from sd_managerscript.queries import QUERY_ENGAGEMENTS
from sd_managerscript.queries import QUERY_ORG_UNIT_LEVEL
from sd_managerscript.queries import QUERY_ORG_UNITS
from sd_managerscript.queries import QUERY_ROOT_ORG_UNIT
from sd_managerscript.queries import UPDATE_MANAGER

logger = structlog.get_logger()


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

    # Selecting org_unit with names ending in "_leder" but NOT starting with "Ø_"
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
            "to": datetime.today().date().isoformat(),
        }
    }

    await execute_mutator(gql_client, ASSOCIATION_TERMINATE, input)
    logger.info("Association terminated!", input=input)


# TODO: terminate_manager isn't utilized at the moment, but they might
# want to have the option to terminate managers...somehow
async def terminate_manager(
    gql_client: PersistentGraphQLClient, manager_uuid: UUID
) -> None:
    """
    Terminates manager role in parent org-unit (updates end date).

    Args:
        gql_client: GraphQL client
        manager_uuid: UUID of the association to terminate
    Returns:
        Nothing
    """

    input = {
        "input": {
            "uuid": str(manager_uuid),
            "to": (datetime.today() - timedelta(days=0)).date().isoformat(),
        }
    }

    await execute_mutator(gql_client, MANAGER_TERMINATE, input)
    logger.info("Manager terminated!", input=input)


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
                gql_client, association["employee_uuid"]
            ),
            org_unit_dict["associations"],
        )
    )
    active_engagements = list(map(jsonable_encoder, active_engagements))

    # Filter away non-active engagements.
    filtered_engagements = list(
        filter(lambda eng: bool(eng["engagement_from"]), active_engagements)
    )

    # If any managers with engagements. -Get manager with latests engagement from date.
    if any(filtered_engagements):
        # We check there's max one employee with the latest from date or we raise an exception
        date_list = [
            datetime.fromisoformat(eng_dict["engagement_from"])
            for eng_dict in filtered_engagements
        ]
        selected_employees = []
        filtered_managers = []
        for engagement in filtered_engagements:
            if (
                datetime.fromisoformat(engagement["engagement_from"]) == max(date_list)
                and engagement["employee_uuid"] not in selected_employees
            ):
                filtered_managers.append(engagement)
                selected_employees.append(engagement["employee_uuid"])

        if len(filtered_managers) > 1:
            raise ConflictingManagers(
                "Two or more employees have same engagement from"
                f"date, in org-unit with uuid: {org_unit_dict['uuid']}"
            )

        associations = list(
            filter(
                lambda association: association["employee_uuid"]
                == one(filtered_managers)["employee_uuid"],
                org_unit_dict["associations"],
            )
        )

        redundant_associations = [
            UUID(association["uuid"])
            for association in org_unit_dict["associations"]
            if association not in associations
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

    for association_uuid in redundant_associations:
        await terminate_association(gql_client, association_uuid)

    org_unit_dict["associations"] = associations

    return OrgUnitManagers.parse_obj(org_unit_dict)


async def get_current_manager(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID
) -> UUID | None:
    """
    Checks if org-unit has an existing manager object. If so, returns UUID
    of that Manager object. Otherwise returns None.

    Args:
        gql_client: GraphQL client
        org_unit_uuid: UUID of the org-unit we want to fetch the manager from.
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
    org_unit: OrgUnitManagers, manager_level: ManagerLevel
) -> Manager:
    """
    Create Manager object for updating and creating managers

    Args:
        org_unit: OrgUnitManagers object
        manager_level_uuid: UUID for manager level
    Returns:
        Manager object
    """

    # UUID for managertype "Leder" which is the same for every manager
    # Fetched from envirometal variable
    manager_type_uuid = get_settings().manager_type_uuid

    # We need to fetch the first element in associations as there could be
    # more than one association. But they would all refer to the same employee
    manager = Manager(
        employee=org_unit.associations[0].employee_uuid,
        org_unit=org_unit.uuid,
        manager_level=manager_level,
        manager_type=ManagerType(uuid=manager_type_uuid),
        validity=Validity(
            from_date=datetime.today().date().isoformat(),
            to_date=None,
        ),
    )  # type: ignore

    logger.info(f"Manager object created: {manager}")
    return manager


async def update_manager(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID, manager_obj: Manager
) -> None:
    """
    Checks if there exists a manager posistion at parent org-unit.
    If so. Update the manager position with employee
    If not: Creates new manager position with employee

    Assign manager to parent org_unit

    Args:
        gql_client: GraphQL client
        org_unit_uuid: uuid of the org-unit we want to assign the manager to
    Returns:
        Nothing
    """
    manager_dict = jsonable_encoder(manager_obj)
    manager_dict["manager_type"] = manager_dict["manager_type"]["uuid"]
    manager_dict["manager_level"] = manager_dict["manager_level"]["uuid"]
    manager_dict["person"] = manager_dict.pop("employee")
    manager_dict["org_unit"] = str(org_unit_uuid)

    current_manager_uuid = await get_current_manager(gql_client, org_unit_uuid)

    if current_manager_uuid:
        manager_dict["uuid"] = str(current_manager_uuid)
        variables = {"input": manager_dict}
        await execute_mutator(gql_client, UPDATE_MANAGER, variables)
        logger.info(f"Manager updated: {manager_dict}")
    else:
        variables = {"input": manager_dict}
        await execute_mutator(gql_client, CREATE_MANAGER, variables)
        logger.info(f"Manager created: {manager_dict}")


async def get_manager_level(
    gql_client: PersistentGraphQLClient, org_unit: OrgUnitManagers
) -> ManagerLevel:
    """
    Checks if parent org-unit is "led-adm" org-unit and returns
    managerlevel based on org-unit level.

    Args:
        gql_client: GraphQL client
        org_unit: OrgUnitManagers object
    Returns
        manager_level_uuid: UUID of managerlevel
    """

    # Assign manager level based on "NYx" org_unit_level_uuid
    managerlevel_dict = one(get_settings().manager_level_mapping)
    org_unit_dict = jsonable_encoder(org_unit)
    org_unit_level_uuid = org_unit_dict["parent"]["org_unit_level_uuid"]

    # If parent org-unit name is ending with "led-adm"
    # we fetch org_unit_level_uuid from org-unit two levels up
    if org_unit_dict["parent"]["name"].strip()[-7:] == "led-adm":
        variables = {"uuids": str(org_unit_dict["parent"]["uuid"])}
        data = await query_graphql(gql_client, QUERY_ORG_UNIT_LEVEL, variables)

        org_unit_level_uuid = one(one(data["org_units"])["objects"])[
            "org_unit_level_uuid"
        ]

    return ManagerLevel(uuid=UUID(managerlevel_dict[org_unit_level_uuid]))


async def create_update_manager(
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
    logger.debug("Creating manager object.", org_unit=org_unit)
    manager_level = await get_manager_level(gql_client, org_unit)

    if any(org_unit.associations):
        manager: Manager = await create_manager_object(
            org_unit,
            manager_level,
        )
        logger.debug("Update manager role.", manager=manager)
        await update_manager(gql_client, org_unit.parent.uuid, manager)

        # If parent org-unit has "led-adm" in name,
        # it's parent org-unit will also have the manager assigned
        if org_unit.parent.name.strip()[-7:] == "led-adm":
            await update_manager(gql_client, org_unit.parent.parent_uuid, manager)


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
    for org_unit in org_units:
        await create_update_manager(gql_client, org_unit)

    logger.info("Updating managers complete!")
