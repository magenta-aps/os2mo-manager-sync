# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from asyncio import gather
from datetime import datetime
from uuid import UUID

import structlog
from fastapi.encoders import jsonable_encoder
from more_itertools import one
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .exceptions import ConflictingManagers
from .mo import get_active_engagements
from .models import OrgUnitManagers
from .terminate import terminate_association

logger = structlog.get_logger()


def remove_org_units_without_associations(
    manager_org_units: list[OrgUnitManagers],
) -> list[OrgUnitManagers]:
    return [org_unit for org_unit in manager_org_units if org_unit.associations]


# Moved to this module from holstebro_managers.py
# TODO: this coroutine has too many responsibilities
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


async def filter_manager_org_units(
    gql_client: PersistentGraphQLClient, manager_org_units: list[OrgUnitManagers]
) -> list[OrgUnitManagers]:
    manager_org_units = [
        await filter_managers(gql_client, org_unit) for org_unit in manager_org_units
    ]
    # Remove the _leder units without associations to the parent "main" unit
    manager_org_units = remove_org_units_without_associations(manager_org_units)

    return manager_org_units
