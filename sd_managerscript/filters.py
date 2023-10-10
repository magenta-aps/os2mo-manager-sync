# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from sd_managerscript.models import OrgUnitManagers


def remove_org_units_without_associations(
    manager_org_units: list[OrgUnitManagers],
) -> list[OrgUnitManagers]:
    return [org_unit for org_unit in manager_org_units if org_unit.associations]
