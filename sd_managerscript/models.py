# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from ramodels.mo._shared import Validity  # type: ignore

from .config import get_settings  # type: ignore


"""
Genereally there seems to be some issues with consistency among the different OS2MO repos.
Eg.: In OS2MO (main) ManagerLevel and ManagerType objects has a name and UUID field, among others.
But in RAModels the ManagerLevel and ManagerType objects only consists of an UUID

Also there is some discrepancies in the naming conventions. In OS2MO (main) ManagerLevel can refer
to just an UUID while it also uses the name for details objects containing UUID, name, user_key etc.
"""


class Association(BaseModel):
    """Model representing an association creation."""

    uuid: UUID = Field(description="UUID of association.")
    org_unit_uuid: UUID = Field(description="UUID of the org-unit.")
    employee_uuid: UUID = Field(description="UUID of the related employee.")
    association_type_uuid: UUID = Field(description="UUID of the association type.")
    validity: Validity = Field(description="Validity range for the org-unit.")


class ManagerLevel(BaseModel):
    """Managerlevel"""

    uuid: UUID = Field(description="UUID of the managerlevel.")


class ManagerType(BaseModel):
    """Managertype"""

    uuid: UUID = Field(description="UUID of the managertype.")


class Manager(BaseModel):
    """Manager model"""

    employee: UUID = Field(description="UUID of the related employee.")
    manager_level: ManagerLevel = Field(description="Manager level object.")
    manager_type: ManagerType = Field(
        description="Manager type object. Same for all managers"
    )
    validity: Validity = Field(description="From date and to date for manager role.")
    org_unit: UUID = Field(description="UUID of the org-unit.")
    uuid: UUID | None = Field(description="UUID of the manager.")
    responsibility: UUID | None = Field(
        get_settings().responsibility_uuid,
        description="Responsibilities. Uses default for all managers",
    )


class Parent(BaseModel):
    uuid: UUID = Field(description="UUID of the parent org-unit.")
    name: str = Field(description="Name of the parent organisation unit.")
    parent_uuid: UUID = Field(
        description="UUID of the parents-parent organisation unit."
    )
    org_unit_level_uuid: UUID = Field(description="UUID of the parent org-unit level.")


class OrgUnitManager(BaseModel):
    org_unit_uuid: UUID
    manager_uuid: UUID


class OrgUnitManagers(BaseModel):
    """
    Organisation unit with managers

    We made our own Pydantic model as we combined the org-unit model
    with Association model and also omitted some fields not neccessary for
    this integration.

    """

    uuid: UUID = Field(description="UUID of the org-unit.")
    name: str = Field(description="Name of the created organisation unit.")
    has_children: bool = Field(
        description="Returns whether the organisation unit has children."
    )
    associations: list[Association] = Field(description="Association object.")
    parent: Parent = Field(description="Details for parent org-unit.")


class EngagementFrom(BaseModel):
    employee_uuid: UUID = Field(description="UUID of the related employee.")
    engagement_from: datetime | None = Field(description="Engagement from date.")
