# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import asyncio
from datetime import datetime
from typing import Any
from uuid import UUID

import structlog
from fastapi.encoders import jsonable_encoder
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore
from ramodels.mo._shared import Validity  # type: ignore

from .config import get_settings
from .filters import filter_manager_org_units
from .models import Manager
from .models import ManagerLevel
from .models import ManagerType
from .models import OrgUnitManager
from .models import OrgUnitManagers
from .queries import CREATE_MANAGER
from .queries import CURRENT_MANAGER
from .queries import QUERY_MANAGER_ENGAGEMENTS_ANCESTOR
from .queries import QUERY_ORG_UNIT_LEVEL
from .queries import QUERY_ORG_UNITS
from .queries import UPDATE_MANAGER
from .terminate import terminate_manager
from .util import execute_mutator
from .util import query_graphql
from .util import query_org_unit

try:
    import zoneinfo
except ImportError:  # pragma: no cover
    from backports import zoneinfo  # type: ignore

DEFAULT_TZ = zoneinfo.ZoneInfo("Europe/Copenhagen")

logger = structlog.get_logger()


def is_engagement_active(engagement: dict[str, Any], org_unit_uuid: str) -> bool:
    """Return True if engagement is in the org_unit and still active."""
    if engagement["org_unit_uuid"] != org_unit_uuid:
        return False

    to_date = engagement["validity"]["to"]
    if to_date is None:
        return True  # No to_date = still active
    return datetime.fromisoformat(to_date) > datetime.now(tz=DEFAULT_TZ)


def has_valid_led_adm_child(org_unit: dict) -> bool:
    """
    Returns True if any of the children follow the naming pattern:
    child.name == parent.name + '_led-adm'
    """
    parent_name = org_unit.get("name", "").lower().strip()
    expected_child_name = f"{parent_name}_led-adm"
    children = org_unit.get("children", [])
    return any(
        child.get("name", "").lower().strip() == expected_child_name
        for child in children
    )


async def get_unengaged_managers(query_dict: dict[str, Any]) -> list[OrgUnitManager]:
    """
    Return OrgUnitManager if the manager has no active engagements in the given org-unit.
    """
    unengaged_managers: list[OrgUnitManager] = []

    try:
        org_unit = one(query_dict["validities"])
    except Exception as e:
        logger.error(f"Invalid query_dict: {query_dict}. Exception: {e}", exc_info=True)
        return unengaged_managers

    if has_valid_led_adm_child(org_unit):
        return unengaged_managers

    org_unit_uuid = org_unit.get("uuid")

    for manager in org_unit.get("managers", []):
        try:
            manager_uuid = manager["uuid"]
            employee = one(manager.get("employee", []))
            engagements = employee.get("engagements", [])

            if not any(is_engagement_active(e, org_unit_uuid) for e in engagements):
                unengaged_managers.append(
                    OrgUnitManager(
                        org_unit_uuid=UUID(org_unit_uuid),
                        manager_uuid=UUID(manager_uuid),
                    )
                )
        except Exception as e:
            logger.warning(
                f"Skipping manager: {query_dict}. Exception: {e}", exc_info=True
            )

    return unengaged_managers


async def check_manager_engagement(
    gql_client: PersistentGraphQLClient,
    org_unit_uuid: UUID,
) -> list[OrgUnitManager]:
    """
    Fetches all descendant org-units (including self) and checks whether managers
    have active engagements. Returns a list of OrgUnitManager instances that should
    be terminated.

    Args:
        gql_client: GraphQL client
        org_unit_uuid: The UUID of the org-unit to check from (inclusive)

    Returns:
        List of OrgUnitManager instances to be terminated.
    """
    variables = {"uuid": str(org_unit_uuid)}
    data = await query_graphql(
        gql_client, QUERY_MANAGER_ENGAGEMENTS_ANCESTOR, variables
    )

    org_units = data["org_units"]["objects"]
    logger.debug("Checking manager engagements in org units", count=len(org_units))

    managers_to_terminate = []

    check_tasks = [get_unengaged_managers(org_unit) for org_unit in org_units]
    results = await asyncio.gather(*check_tasks)
    results = [res for res in results if res is not None]

    for res in results:
        managers_to_terminate.extend(res)

    return managers_to_terminate


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

    # TODO: This whole recursive thing, could possibly be simplyfied by just
    # fetching all units (potentially with pagination).
    # It seems redundant, compared to the state GraphQL is in now.
    variables = {"uuid": str(org_unit_uuid)}
    data = await query_org_unit(gql_client, QUERY_ORG_UNITS, variables)
    logger.debug("Org-units returned from query", response=data)

    # Select _leder units that are not prefixed with 'Ø_'
    leder_units = [
        ou
        for ou in data
        if ou.name.lower().strip().endswith("_leder")
        and not ou.name.strip().startswith("Ø_")
    ]

    if recursive:
        child_org_units = [ou for ou in data if ou.has_children]
        recursive_results = await asyncio.gather(
            *[
                get_manager_org_units(gql_client, ou.uuid, recursive=True)
                for ou in child_org_units
            ]
        )
        for result in recursive_results:
            leder_units.extend(result)

    return leder_units


async def get_current_manager(
    gql_client: PersistentGraphQLClient, org_unit_uuid: UUID
) -> Manager | None:
    """
    Get the current manager or None, if the manager does not exist

    Args:
        gql_client: GraphQL client
        org_unit_uuid: UUID of the org-unit we want to fetch the manager from.
    Returns:
        The manager or None, if the manager does not exist
    """
    variables = {"uuid": str(org_unit_uuid)}
    ou_manager = await query_graphql(gql_client, CURRENT_MANAGER, variables)
    managers = one(one(ou_manager["org_units"]["objects"])["validities"])["managers"]
    if managers:
        logger.debug("Manager found", manager=managers, org_unit=str(org_unit_uuid))
        manager = one(managers)
        return Manager(
            employee=UUID(manager["employee_uuid"]),
            manager_level=ManagerLevel(uuid=UUID(manager["manager_level_uuid"])),
            manager_type=ManagerType(uuid=UUID(manager["manager_type_uuid"])),
            validity=Validity(
                from_date=datetime.fromisoformat(manager["validity"]["from"])
            ),
            org_unit=UUID(manager["org_unit_uuid"]),
            uuid=UUID(manager["uuid"]),
        )
    logger.debug("Manager not found", org_unit=str(org_unit_uuid))
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
    # Not sure that's true ^
    # TODO: add missing fields
    manager = Manager(
        employee=org_unit.associations[0].employee_uuid,
        org_unit=org_unit.uuid,
        manager_level=manager_level,
        manager_type=ManagerType(uuid=manager_type_uuid),
        validity=Validity(
            from_date=datetime.today().date().isoformat(),
            to_date=None,
        ),
    )

    logger.info(f"Manager object created: {manager}")
    return manager


def is_manager_correct(
    current_manager: Manager,
    new_manager: Manager,
    org_unit: UUID,
) -> bool:
    logger.debug(
        "Comparing managers",
        current_manager=current_manager,
        new_manager=new_manager,
        org_unit=org_unit,
    )
    return (
        current_manager.manager_type == new_manager.manager_type
        and current_manager.manager_level == new_manager.manager_level
        and current_manager.org_unit == org_unit
        and current_manager.employee == new_manager.employee
    )


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

    current_manager = await get_current_manager(gql_client, org_unit_uuid)

    if current_manager is None:
        variables = {"input": manager_dict}
        await execute_mutator(gql_client, CREATE_MANAGER, variables)
        logger.info(f"Manager created: {manager_dict}")
        return

    manager_correct = is_manager_correct(current_manager, manager_obj, org_unit_uuid)
    logger.debug("Check if manager correct", correct=manager_correct)

    if not manager_correct:
        manager_dict["uuid"] = str(current_manager.uuid)
        variables = {"input": manager_dict}
        await execute_mutator(gql_client, UPDATE_MANAGER, variables)
        logger.info(f"Manager updated: {manager_dict}")


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
    manager_level_dict = get_settings().manager_level_mapping
    org_unit_level_uuid = org_unit.parent.org_unit_level_uuid

    # If parent org-unit name is ending with "led-adm"
    # we fetch org_unit_level_uuid from org-unit two levels up
    if org_unit.parent.name.strip().endswith("led-adm"):
        variables = {"uuids": str(org_unit.parent.parent_uuid)}
        data = await gql_client.execute(QUERY_ORG_UNIT_LEVEL, variable_values=variables)

        org_unit_level_uuid = one(one(data["org_units"]["objects"])["validities"])[
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
    recursive: bool = True,
    dry_run: bool = False,
) -> None:
    """Main function for selecting and updating managers"""

    logger.info("Check for unengaged managers...")
    managers_to_terminate = await check_manager_engagement(gql_client, org_unit_uuid)
    logger.debug("Managers to terminate", managers_to_terminate=managers_to_terminate)

    logger.info("Terminate unengaged managers", manager=managers_to_terminate)
    for org_unit_manager in managers_to_terminate:
        await terminate_manager(
            gql_client, org_unit_manager.manager_uuid, dry_run=dry_run
        )

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

    logger.debug("hurra")
    logger.info("Updating managers complete!")
