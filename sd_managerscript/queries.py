# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from gql import gql  # type: ignore

ORG_UNITS = "org_units"

QUERY_ORG = gql("query {org { uuid }}")

QUERY_ORG_UNIT_LEVEL = gql(
    """query ($uuids: [UUID!]!) {org_units (uuids: $uuids) {objects{org_unit_level_uuid}}}"""
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
                    org_unit_uuid
                    employee_uuid
                    association_type_uuid
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

MANAGER_TERMINATE = gql(
    """
        mutation($input: ManagerTerminateInput!){
            manager_terminate(input: $input){
                uuid
            }
        }
    """
)

QUERY_ROOT_MANAGER_ENGAGEMENTS = gql(
    """
        query ($uuid: [UUID!]!){
            org_units (uuids: $uuid){
                uuid
                objects{
                    child_count
                    managers{
                        uuid
                        employee {
                            engagements {
                                org_unit_uuid
                                validity{
                                    from
                                    to
                                }
                            }
                        }
                    }
                }
            }
        }
    """
)

QUERY_MANAGER_ENGAGEMENTS = gql(
    """
        query ($uuid: [UUID!]!){
            org_units (parents: $uuid){
                uuid
                objects{
                    child_count
                    managers{
                        uuid
                        employee {
                            engagements {
                                org_unit_uuid
                                validity{
                                    from
                                    to
                                }
                            }
                        }
                    }
                }
            }
        }
    """
)
