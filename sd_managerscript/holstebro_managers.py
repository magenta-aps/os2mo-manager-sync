# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from datetime import timezone
from typing import Any
from uuid import UUID

import structlog
from fastapi.encoders import jsonable_encoder
from more_itertools import collapse
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore
from ramodels.mo._shared import Validity  # type: ignore

from .config import get_settings
from .filters import filter_manager_org_units
from .models import Manager
from .models import ManagerLevel
from .models import ManagerType
from .models import OrgUnitManagers
from .queries import CREATE_MANAGER
from .queries import CURRENT_MANAGER
from .queries import QUERY_MANAGER_ENGAGEMENTS
from .queries import QUERY_ORG_UNIT_LEVEL
from .queries import QUERY_ORG_UNITS
from .queries import QUERY_ROOT_MANAGER_ENGAGEMENTS
from .queries import UPDATE_MANAGER
from .terminate import terminate_manager
from .util import execute_mutator
from .util import query_graphql
from .util import query_org_unit

logger = structlog.get_logger()


async def get_unengaged_managers(query_dict: dict[str, Any]) -> UUID | None:
    """
    Check if manager has an active engagement in this org-unit
    if not, return manager_uuid.

    Args:
        query_dict: dict with info on manager details: employee, engagement to date
                    See example below, as well as query to generate the dict:
                        .queries: QUERY_MANAGER_ENGAGEMENTS
    Returns:
        UUID (manager uuid) if manager has no active engagement
        None if manager has an active engagement in this org-unit

    Example of query_dict:

    {
        "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
        "objects": [
            {
                "child_count": 2,
                "managers": [
                    {
                        "uuid": "5a988dee-109a-4353-95f2-fb414ea8d605",
                        "employee": [
                            {
                                "engagements": [
                                    {
                                        "org_unit_uuid": "09c347ef-451f-5919-8d41-02cc989a6d8b",
                                        "validity": {
                                            "from": "2022-11-20T00:00:00+01:00",
                                            "to": None,
                                        },
                                    },
                                ]
                            }
                        ],
                    }
                ],
            }
        ],
    }



    """
    # TODO: Replace nested if tree with filter?
    # (https://git.magenta.dk/rammearkitektur/os2mo-manager-sync/-/merge_requests/7#note_177686)

    # if org-unit has any managers
    if one(query_dict["objects"])["managers"]:
        manager_uuid = one(one(query_dict["objects"])["managers"])["uuid"]

        # if employee has any engagements, check it's still active
        engagements = one(one(one(query_dict["objects"])["managers"])["employee"])[
            "engagements"
        ]
        # Only get engagements relevant for this org_unit
        if engagements:
            relevant_engagements = list(
                filter(
                    lambda eng: eng["org_unit_uuid"] == query_dict["uuid"], engagements
                )
            )
            if relevant_engagements:
                to_dates = [
                    engagement["validity"]["to"] for engagement in relevant_engagements
                ]

                # Check if at least one of the engagements to_date is after
                # today or None in which case there is an active engagement
                for to_date in to_dates:
                    if not to_date or (
                        datetime.fromisoformat(to_date) > datetime.now(tz=timezone.utc)
                    ):
                        return None

        return UUID(manager_uuid)
    return None


async def check_manager_engagement(
    gql_client: PersistentGraphQLClient,
    org_unit_uuid: UUID,
    root_uuid: UUID,
    recursive: bool = True,
) -> list[UUID]:
    """
    Recursive function, traverse through all org_units and checks if manager has engagement
    If not: Managers uuid is added to managers_to_terminate for later termination


    Args:
        Graphql client
        org_unit_uuid: UUID of the parent org-unit we want to get child org-units from
        root_uuid: root_uuid of the Organisation tree.
                   (root_uuid is fetched from enviromental variable)
        recursive: If true, check manager engagement recursively
    Returns:
        list of manager UUID's

    Function flow:
        If pass org_unit_uuid is same as root_uuid:
            Check manager in root org-unit has active engagement.

        Query org_unit_uuid for child org_units

        For each child org-unit check the assigned manager has active engagement
        or return manager_uuid for termination

        for each child org_unit check if it has any child org_units.
        If an org_unit has children the org_units uuid is passed to this function recusively

        TODO: Might optimize this function to avoid checking for root_uuid:
        https://git.magenta.dk/rammearkitektur/os2mo-manager-sync/-/merge_requests/7#note_177689
    """

    # TODO: add unit test for recursive=False

    variables = {"uuid": str(org_unit_uuid)}
    managers_to_terminate = []

    # If this is root org-unit we have to query it separately
    # For info: the difference between QUERY_ROOT_MANAGER_ENGAGEMENTS and
    # QUERY_MANAGER_ENGAGEMENTS is that the latter uses org_units(parents: ...) where
    # the former uses org_units(uuids: ...)
    # TODO: investigate if this can be refactored
    if org_unit_uuid == root_uuid or not recursive:
        data = await query_graphql(
            gql_client, QUERY_ROOT_MANAGER_ENGAGEMENTS, variables
        )
        # Check if manager of root org-unit has active engagement
        managers_to_terminate = [
            out
            for org_unit in data["org_units"]
            if (out := await get_unengaged_managers(org_unit))
        ]
        if not recursive:
            return managers_to_terminate

    # Query for child org-units of org_unit_uuid
    data = await query_graphql(gql_client, QUERY_MANAGER_ENGAGEMENTS, variables)

    # For each child org_unit in data, check the assigned manager has active engagement
    # or else return managers uuid to terminate
    logger.debug("Org-units returned from query", response=data)
    managers_to_terminate += [
        out
        for org_unit in data["org_units"]
        if (out := await get_unengaged_managers(org_unit))
    ]

    # Fetch org-units with children
    child_org_units = filter(
        lambda org_unit: one(org_unit["objects"])["child_count"] > 0,
        data["org_units"],
    )
    # Pass org_units with children (uuid)to this function recusively
    managers_to_terminate += [
        await check_manager_engagement(gql_client, org_unit["uuid"], root_uuid)  # type: ignore
        for org_unit in child_org_units
    ]

    managers = list(collapse(managers_to_terminate, base_type=UUID))
    return managers


async def get_manager_org_units(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID, recursive: bool = True
) -> list[OrgUnitManagers]:
    """
    Recursive function, traverse through all org_units and return '_leder' org-units

    Args:
        Graphql client
        org_unit_uuid: UUID
        recursive: If true, all manager OUs will be fetched recursively. If false,
          only the '_leder' OUs directly below the org_unit_uuid will be fetched.
    Returns:
        managers: list of '_leder' OrgUnitManagers

    """

    variables = {"uuid": str(org_unit_uuid)}
    data = await query_org_unit(gql_client, QUERY_ORG_UNITS, variables)
    logger.debug("Org-units returned from query", response=data)
    child_org_units = filter(lambda ou: jsonable_encoder(ou)["child_count"] > 0, data)

    # Selecting org_unit with names ending in "_leder" but NOT starting
    # with "Ø_"
    # TODO: we should probably check that there is only one '_leder' in each
    #  org unit level in the OU-tree
    manager_list = list(
        filter(
            lambda ou: (jsonable_encoder(ou)["name"].lower().strip()[-6:] == "_leder")
            and (jsonable_encoder(ou)["name"].strip()[:2] != "Ø_"),
            data,
        )
    )
    logger.debug("Manager list up until now...", org_units=manager_list)
    if recursive:
        manager_list += [
            await get_manager_org_units(  # type: ignore
                gql_client, UUID(jsonable_encoder(org_unit)["uuid"])
            )
            for org_unit in child_org_units
        ]
    managers = list(collapse(manager_list, base_type=OrgUnitManagers))
    return managers


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
    manager level based on org-unit level.

    Args:
        gql_client: GraphQL client
        org_unit: OrgUnitManagers object
    Returns
        manager_level_uuid: UUID of manager level
    """

    # Assign manager level based on "NYx" org_unit_level_uuid
    # TODO: use Pydantic model instead of dict in the ENV
    manager_level_dict = one(get_settings().manager_level_mapping)
    org_unit_level_uuid = org_unit.parent.org_unit_level_uuid

    # If parent org-unit name is ending with "led-adm"
    # we fetch org_unit_level_uuid from org-unit two levels up
    if org_unit.parent.name.strip()[-7:] == "led-adm":
        variables = {"uuids": str(org_unit.parent.parent_uuid)}
        data = await gql_client.execute(QUERY_ORG_UNIT_LEVEL, variable_values=variables)

        org_unit_level_uuid = one(one(data["org_units"])["objects"])[
            "org_unit_level_uuid"
        ]

    return ManagerLevel(uuid=UUID(manager_level_dict[str(org_unit_level_uuid)]))


async def create_update_manager(
    gql_client: PersistentGraphQLClient,
    org_unit: OrgUnitManagers,
    dry_run: bool = False,
) -> None:
    """
    Create manager payload and send request to update manager in relevant org-units

    Args:
        gql_client: GraphQL client
        org_unit: OrgUnitManagers object
        dry_run: If true, do not actually perform write operations to MO
    Returns:
        Nothing
    """

    # TODO: unit test for dry run

    logger.debug("Creating manager object.", org_unit=org_unit)
    manager_level = await get_manager_level(gql_client, org_unit)

    manager: Manager = await create_manager_object(
        org_unit,
        manager_level,
    )
    logger.debug("Update manager role.", manager=manager)
    if not dry_run:
        await update_manager(gql_client, org_unit.parent.uuid, manager)

    # If parent org-unit has "led-adm" in name,
    # it's parent org-unit will also have the manager assigned
    if org_unit.parent.name.strip()[-7:] == "led-adm":
        logger.debug("Parent unit is 'led-adm' - manager will also be assigned here")
        if not dry_run:
            await update_manager(gql_client, org_unit.parent.parent_uuid, manager)


async def update_mo_managers(
    gql_client: PersistentGraphQLClient,
    org_unit_uuid: UUID,
    root_uuid: UUID,
    recursive: bool = True,
    dry_run: bool = False,
) -> None:
    """Main function for selecting and updating managers"""

    logger.info("Check for unengaged managers...")
    managers_to_terminate = await check_manager_engagement(
        gql_client, org_unit_uuid, root_uuid, recursive=recursive
    )
    logger.debug("Managers to terminate", managers_to_terminate=managers_to_terminate)

    logger.info("Terminate unengaged managers", manager=managers_to_terminate)
    for manager_uuid in managers_to_terminate:
        await terminate_manager(gql_client, manager_uuid, dry_run=dry_run)

    logger.info("Getting manager org units (units ending in _leder)...")
    manager_org_units = await get_manager_org_units(
        gql_client, org_unit_uuid, recursive=recursive
    )
    logger.debug("Manager org units", manager_org_units=manager_org_units)

    logger.info("Filter managers org units")
    manager_org_units = await filter_manager_org_units(gql_client, manager_org_units)

    logger.info("Updating Managers")
    for org_unit in manager_org_units:
        await create_update_manager(gql_client, org_unit, dry_run=dry_run)

    logger.info("Updating managers complete!")
