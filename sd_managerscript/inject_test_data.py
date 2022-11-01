# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Any

from fastapi.encoders import jsonable_encoder
from gql import gql  # type: ignore
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

"""org-unit name, uuid of org-unit."""
leder_org_units = [
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

"""Person_uuid, Resonsibility_uuid, manager_level_uuid, manager_type_uuid."""
employees = [
    {
        "person": "00973369-2d8f-4120-bbaf-75f0e0f38534",
        "responsibility": "2f4f5cbc-35bd-4ee1-a220-5778036a15cd",
        "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
        "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
    },
    {
        "person": "03ff3b1a-a16b-4ea6-b372-065a77f849cb",
        "responsibility": "36601c9a-561c-4372-a43f-2a15bf27ef0c",
        "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
        "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
    },
    {
        "person": "0790ca9c-f3ae-4e4b-b936-03b8aedf5314",
        "responsibility": "2f4f5cbc-35bd-4ee1-a220-5778036a15cd",
        "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
        "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
    },
    {
        "person": "07d2415b-a9e7-4b8a-bdd4-0d5ea74a457e",
        "responsibility": "2f4f5cbc-35bd-4ee1-a220-5778036a15cd",
        "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
        "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
    },
    {
        "person": "08c31328-17aa-48c2-8293-3fc6f59ebe9c",
        "responsibility": "36601c9a-561c-4372-a43f-2a15bf27ef0c",
        "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
        "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
    },
    {
        "person": "0b5936f2-328d-448e-bfb9-d655e6d3d849",
        "responsibility": "36601c9a-561c-4372-a43f-2a15bf27ef0c",
        "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
        "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
    },
]


CREATE_MANAGER = gql(
    """
    mutation (
        $person: UUID!,
        $responsibility: [UUID!]!
        $org_unit: UUID!
        $manager_level: UUID!
        $manager_type: UUID!
        $from: DateTime!
    )
    {
        manager_create (
            input: {
                person: $person
                responsibility: $responsibility
                org_unit: $org_unit
                manager_level: $manager_level
                manager_type: $manager_type
                validity: {from: $from}
            }
        )
        {
            uuid
        }
    }
"""
)

CREATE_LEDER_ORG_UNIT = gql(
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


async def create_leder_ou(input: tuple, gql_client: PersistentGraphQLClient) -> Any:
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
    org_unit_uuid: dict = await gql_client.execute(
        CREATE_LEDER_ORG_UNIT, variable_values=jsonable_encoder(data)
    )
    return org_unit_uuid


async def create_managers(input: tuple, gql_client: PersistentGraphQLClient) -> None:
    """Write managers to the newly created '_leder' org-units."""
    data = input[0]
    data["org_unit"] = input[1]["org_unit_create"]["uuid"]
    data["from"] = "2022-08-01"
    _ = await gql_client.execute(CREATE_MANAGER, variable_values=jsonable_encoder(data))


async def inject_data(gql_client: PersistentGraphQLClient) -> None:
    org_unit_uuids = [
        await create_leder_ou(input=ou, gql_client=gql_client) for ou in leder_org_units
    ]
    input = list(zip(employees, org_unit_uuids))
    for ou in input:
        await create_managers(ou, gql_client=gql_client)
