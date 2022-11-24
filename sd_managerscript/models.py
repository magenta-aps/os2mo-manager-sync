# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from ramodels.mo._shared import Validity  # type: ignore

"""
Genereally there seems to be some issues with consistency among the different OS2MO repos.
Eg.: In OS2MO (main) ManagerLevel and ManagerType objects has a name and UUID field, among others.
But in RAModels the ManagerLevel and ManagerType objects only consists of an UUID

Also there is some discrepancies in the naming conventions. In OS2MO (main) ManagerLevel can refer
to just an UUID while it also uses the name for details objects containing UUID, name, user_key etc.
"""


class ManagerLevel(BaseModel):
    """Managerlevel"""

    uuid: UUID = Field(description="UUID og the managerlevel.")
    name: str = Field(description="Name of the managerlevel.")


class ManagerType(BaseModel):
    """Managertype"""

    uuid: UUID = Field(description="UUID og the managertype.")
    name: str = Field(description="Name of the managertype.")


class Manager(BaseModel):
    """Manager model"""

    uuid: UUID = Field(description="UUID og the manager.")
    employee_uuid: UUID = Field(description="UUID of the related employee.")
    manager_level: ManagerLevel = Field(description="Manager level object.")
    manager_type: ManagerType = Field(description="Manager type object.")
    validity: Validity | None = Field(
        description="From date and to date for manager role."
    )


class OrgUnitManagers(BaseModel):
    """
    Organisation unit with managers

    We made our own Pydantic model as we combined the org-unit model
    with Manager model and also omitted some fields not neccessary for
    this integration.

    """

    uuid: UUID = Field(description="UUID og the org-unit.")
    name: str = Field(description="Name of the created organisation unit.")
    parent_uuid: UUID = Field(description="Reference to the parent organisation unit.")
    child_count: int = Field(description="Number of child org-units.")
    managers: list[Manager] = Field(description="Manager object.")


class EngagementFrom(BaseModel):
    employee_uuid: UUID = Field(description="UUID of the related employee.")
    engagement_from: datetime | None = Field(description="Engagement from date.")
