# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from uuid import uuid4

from ramodels.mo import Validity  # type: ignore

from sd_managerscript.filters import remove_org_units_without_associations
from sd_managerscript.models import Association
from sd_managerscript.models import OrgUnitManagers
from sd_managerscript.models import Parent


def test_remove_org_unit_without_associations() -> None:
    # Arrange
    parent = Parent(
        uuid=uuid4(),
        name="Parent OU name",
        parent_uuid=uuid4(),
        org_unit_level_uuid=uuid4(),
    )
    manager_org_units = [
        OrgUnitManagers(
            uuid=uuid4(),
            name="OU name",
            child_count=0,
            associations=[
                Association(
                    uuid=uuid4(),
                    org_unit_uuid=uuid4(),
                    employee_uuid=uuid4(),
                    association_type_uuid=uuid4(),
                    validity=Validity(from_date=datetime.now()),
                )
            ],
            parent=parent,
        ),
        OrgUnitManagers(
            uuid=uuid4(), name="OU name", child_count=0, associations=[], parent=parent
        ),
    ]

    # Act
    filtered_manager_org_units = remove_org_units_without_associations(
        manager_org_units
    )

    # Assert
    expected_filtered_manager_org_units = manager_org_units[:1]
    assert filtered_manager_org_units == expected_filtered_manager_org_units
