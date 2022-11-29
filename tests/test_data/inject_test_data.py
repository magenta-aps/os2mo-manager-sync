# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import argparse
from functools import partial

import structlog
from fastapi.encoders import jsonable_encoder
from gql import gql  # type: ignore
from raclients.graph.client import GraphQLClient  # type: ignore

logger = structlog.get_logger()


"""org-unit name, uuid of org-unit."""
manager_org_units = [
    (
        "Kloakering",
        "cf4daae1-4812-41f1-8c47-63a99e26aadf",
    ),
    (
        "Social og sundhed",
        "a6773531-6c0a-4c7b-b0e2-77992412b610",
    ),
    (
        "Social Indsats",
        "535ba446-d618-4e51-8dae-821d63e26560",
    ),
    (
        "Hejls skole",
        "48fa5e8a-5a47-5df3-a10b-292ed181e054",
    ),
    (
        "Almind skole",
        "bc876b6c-3682-5b60-804b-95ff759b5509",
    ),
    (
        "Byudvikling",
        "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",
    ),
]

"""org-unit name, uuid of org-unit."""
redundant_org_units = [
    (
        "Kloakering",
        "cf4daae1-4812-41f1-8c47-63a99e26aadf",
    ),
    (
        "Almind skole",
        "bc876b6c-3682-5b60-804b-95ff759b5509",
    ),
]

"""org-unit name, uuid of org-unit."""
led_adm_org_units = [
    (
        "Hejls skole",
        "48fa5e8a-5a47-5df3-a10b-292ed181e054",
    ),
    (
        "Byudvikling",
        "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",
    ),
]


"""Person_uuid, Resonsibility_uuid, manager_level_uuid, manager_type_uuid."""
employees = [
    (
        "00973369-2d8f-4120-bbaf-75f0e0f38534",
        "03ff3b1a-a16b-4ea6-b372-065a77f849cb",
    ),
    (
        "0790ca9c-f3ae-4e4b-b936-03b8aedf5314",
        "07d2415b-a9e7-4b8a-bdd4-0d5ea74a457e",
    ),
    (
        "08c31328-17aa-48c2-8293-3fc6f59ebe9c",
        "0b5936f2-328d-448e-bfb9-d655e6d3d849",
    ),
    (
        "1c571f8f-0e3e-4ffa-9ff0-d35505781924",
        "1caf4616-f22d-4989-8492-d3c5024ef4e8",
    ),
    (
        "1d64f753-5506-4de1-8125-87a2ec04ecc9",
        "1e96bf0b-bcfe-4703-a604-2e829b5a7663",
    ),
    ("bff25bde-a300-43b6-a070-778a60f59a7d", "c0814647-ae83-4c43-9ff2-ccc42dfd429c"),
]


CREATE_ASSOCIATION = gql(
    """
    mutation ($input: AssociationCreateInput!)
    {
        association_create (input: $input)
        {
            uuid
        }
    }
"""
)

CREATE_MANAGER_ORG_UNIT = gql(
    """
    mutation (
        $name: String!
        $parent: UUID!
        $from: DateTime!
        $org_unit_type: UUID!
    )
    {
        org_unit_create (
            input: {
                name: $name
                parent: $parent
                validity: {from: $from}
                org_unit_type: $org_unit_type
            }
        )
        {
            uuid
        }
    }

"""
)

UPDATE_ORG_UNIT = gql(
    """
    mutation (
        $name: String!
        $uuid: UUID!
        $from: DateTime!
    )
    {
        org_unit_update (
            input: {
                name: $name
                uuid: $uuid
                validity: {from: $from}
            }
        )
        {
            uuid
        }
    }
    """
)


def construct_client(client_secret: str) -> GraphQLClient:
    """Construct clients froms settings.

    Args:
        settings: Integration settings module.

    Returns:
        PersistentGraphQLClient.
    """
    gql_client = GraphQLClient(
        url="http://localhost:5000/graphql/v2",
        client_id="dipex",
        client_secret=client_secret,
        auth_server="http://localhost:5000/auth",
        auth_realm="mo",
        execute_timeout=120,
        httpx_client_kwargs={"timeout": 120},
    )
    logger.info("Created graphql client")

    return gql_client


def create_manager_ou(input: tuple, gql_client: GraphQLClient) -> str:
    """Create new sub org-units with name as parent + '_leder '"""
    name = input[0] + "_leder"
    parent = input[1]  # UUID
    org_unit_type = "9d2ac723-d5e5-4e7f-9c7f-b207bd223bc2"
    from_date = "2022-07-31"
    data = {
        "name": name,
        "parent": parent,
        "org_unit_type": org_unit_type,
        "from": from_date,
    }

    org_unit = gql_client.execute(
        CREATE_MANAGER_ORG_UNIT, variable_values=jsonable_encoder(data)
    )

    return org_unit["org_unit_create"]["uuid"]  # type: ignore


def create_led_adm_org_units(gql_client: GraphQLClient, input: tuple) -> None:
    """Update selected org-units name with '_led-adm'"""

    name = input[0] + "_led-adm"
    uuid = input[1]  # UUID
    org_unit_type = "9d2ac723-d5e5-4e7f-9c7f-b207bd223bc2"
    from_date = "2022-07-15"
    data = {
        "name": name,
        "uuid": uuid,
        "org_unit_type": org_unit_type,
        "from": from_date,
    }

    gql_client.execute(UPDATE_ORG_UNIT, variable_values=jsonable_encoder(data))


def create_redundant_ou(gql_client: GraphQLClient, input: tuple) -> None:
    """Create new sub org-units with name as parent + prepend "Ø_" and append '_leder '"""
    name = "Ø_" + input[0] + "_leder"
    parent = input[1]  # UUID
    org_unit_type = "9d2ac723-d5e5-4e7f-9c7f-b207bd223bc2"
    from_date = "2022-06-20"
    data = {
        "name": name,
        "parent": parent,
        "org_unit_type": org_unit_type,
        "from": from_date,
    }

    gql_client.execute(CREATE_MANAGER_ORG_UNIT, variable_values=jsonable_encoder(data))


def create_assocications(
    gql_client: GraphQLClient, org_unit_uuid: str, employee_uuid: str
) -> None:
    """Write associations to the newly created '_leder' org-units."""

    variables = {
        "input": {
            "org_unit": org_unit_uuid,
            "employee": employee_uuid,
            "association_type": "75fee2b6-f405-4c77-b62e-32421c2e43d5",
            "validity": {
                "from": "2022-08-05",
                "to": None,
            },
        }
    }

    gql_client.execute(CREATE_ASSOCIATION, variable_values=variables)


def inject_data(client_password: str) -> None:
    logger.info("Will probably inject test data now ...")
    gql_client = construct_client(client_password)

    org_unit_uuids = [
        create_manager_ou(input=ou, gql_client=gql_client) for ou in manager_org_units
    ]

    for org_unit_uuid, emp in zip(org_unit_uuids, employees):
        for employee in emp:
            create_assocications(gql_client, org_unit_uuid, employee)

    map(partial(create_led_adm_org_units, gql_client), led_adm_org_units)

    for org_unit_tuple in redundant_org_units:
        create_redundant_ou(gql_client, org_unit_tuple)

    logger.info("Test data injected!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("password", type=str)
    args = parser.parse_args()
    inject_data(args.password)
