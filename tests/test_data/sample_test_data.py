# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from uuid import UUID

from dateutil.tz import tzoffset  # type: ignore
from ramodels.mo._shared import Validity  # type: ignore

from sd_managerscript.models import Manager
from sd_managerscript.models import ManagerLevel
from sd_managerscript.models import ManagerType
from sd_managerscript.models import OrgUnitManagers

graphql_payload = {
    "org_units": [
        {
            "objects": [
                {
                    "uuid": "7133da92-e624-56c9-8e23-bac319a537e1",
                    "name": "Administration",
                    "parent_uuid": "1caba8d9-6b9f-506b-b845-9a8c4f5b8a03",
                    "child_count": 2,
                    "managers": [
                        {
                            "uuid": "36b5be05-7323-418f-bbd4-7be23c9ca150",
                            "employee_uuid": "4c88d5a3-199f-454b-9349-a24ab218ca54",
                            "manager_level": {
                                "name": "Niveau 4",
                                "uuid": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
                            },
                            "manager_type": {
                                "name": "Direktør",
                                "uuid": "267e5e49-3abd-49df-9bd9-38d41d2294ff",
                            },
                            "validity": {
                                "to": None,
                                "from": "1977-03-02T00:00:00+01:00",
                            },
                        }
                    ],
                }
            ]
        },
        {
            "objects": [
                {
                    "uuid": "6e629aef-4e5a-537a-8320-5e05015685f6",
                    "name": "Teknisk Support",
                    "parent_uuid": "316358a3-6007-5802-af99-656a19999f0c",
                    "child_count": 0,
                    "managers": [
                        {
                            "uuid": "a9409fb0-a00e-490e-a429-c153385fb880",
                            "employee_uuid": "d9c71751-8afa-40c7-8b89-498db8c775d2",
                            "manager_level": {
                                "name": "Niveau 4",
                                "uuid": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
                            },
                            "manager_type": {
                                "name": "Direktør",
                                "uuid": "267e5e49-3abd-49df-9bd9-38d41d2294ff",
                            },
                            "validity": {
                                "to": None,
                                "from": "2022-01-01T00:00:00+01:00",
                            },
                        }
                    ],
                }
            ]
        },
    ]
}

org_unit_samples = [
    [
        OrgUnitManagers(
            uuid=UUID("08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"),
            name="Viuf skole",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            child_count=1,
            managers=[
                Manager(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    manager_level=ManagerLevel(
                        uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                        name="Niveau 4",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("267e5e49-3abd-49df-9bd9-38d41d2294ff"),
                        name="Direktør",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        OrgUnitManagers(
            uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            name="Lunderskov skole",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            child_count=2,
            managers=[],
        ),
        OrgUnitManagers(
            uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
            name="Sønder Stenderup skole",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            child_count=-2,
            managers=[
                Manager(
                    uuid=UUID("0b51953c-537b-4bf9-a872-2710b0ddd9e3"),
                    employee_uuid=UUID("7deea6da-8892-4d93-ac8b-8d5b9c659d77"),
                    manager_level=ManagerLevel(
                        uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                        name="Niveau 4",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("267e5e49-3abd-49df-9bd9-38d41d2294ff"),
                        name="Direktør",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
    ],
    [
        OrgUnitManagers(
            uuid=UUID("1c690f27-35c5-5c02-975a-930e6b524805"),
            name="Haderslev skole",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            child_count=0,
            managers=[],
        ),
        OrgUnitManagers(
            uuid=UUID("1caba8d9-6b9f-506b-b845-9a8c4f5b8a03"),
            name="Jordrup børnehus",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            child_count=1,
            managers=[
                Manager(
                    uuid=UUID("c542df8b-ad33-4a1b-844a-b1ff0150e4d4"),
                    employee_uuid=UUID("539391a4-a12b-4f0b-8b79-440118e1522e"),
                    manager_level=ManagerLevel(
                        uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                        name="Niveau 4",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("267e5e49-3abd-49df-9bd9-38d41d2294ff"),
                        name="Direktør",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
    ],
    [
        OrgUnitManagers(
            uuid=UUID("72d8e92f-9481-43af-8cb0-a83823c9f35e"),
            name="Almind skole_leder ",
            parent_uuid=UUID("bc876b6c-3682-5b60-804b-95ff759b5509"),
            child_count=0,
            managers=[
                Manager(
                    uuid=UUID("649fc94c-4897-4421-a9f6-fb06c43e5f4e"),
                    employee_uuid=UUID("08c31328-17aa-48c2-8293-3fc6f59ebe9c"),
                    manager_level=ManagerLevel(
                        uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38"),
                        name="Niveau 2",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8"),
                        name="Områdeleder",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        OrgUnitManagers(
            uuid=UUID("60370b40-a143-40c5-aaa1-638b3b74d119"),
            name="Social Indsats_LEDER",
            parent_uuid=UUID("535ba446-d618-4e51-8dae-821d63e26560"),
            child_count=3,
            managers=[
                Manager(
                    uuid=UUID("8250d35b-fab6-4c9e-95ab-da52848f9df9"),
                    employee_uuid=UUID("0790ca9c-f3ae-4e4b-b936-03b8aedf5314"),
                    manager_level=ManagerLevel(
                        uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38"),
                        name="Niveau 2",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8"),
                        name="Områdeleder",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
    ],
    [
        OrgUnitManagers(
            uuid=UUID("1f06ed67-aa6e-4bbc-96d9-2f262b9202b5"),
            name="Budget og Planlægning",
            parent_uuid=UUID("b6c11152-0645-4712-a207-ba2c53b391ab"),
            child_count=0,
            managers=[
                Manager(
                    uuid=UUID("5a988dee-109a-4353-95f2-fb414ea8d605"),
                    employee_uuid=UUID("f16eee45-d96a-4efb-bd17-667d1795e13d"),
                    manager_level=ManagerLevel(
                        uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                        name="Niveau 4",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("267e5e49-3abd-49df-9bd9-38d41d2294ff"),
                        name="Direktør",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
    ],
    [
        OrgUnitManagers(
            uuid=UUID("25e39a21-caef-4e96-ac90-7cc27173082e"),
            name="IT-Support",
            parent_uuid=UUID("b6c11152-0645-4712-a207-ba2c53b391ab"),
            child_count=0,
            managers=[
                Manager(
                    uuid=UUID("a9894c2b-8eaa-4487-97c9-9644fb22f93e"),
                    employee_uuid=UUID("ade098f3-0a7a-476d-b0ff-055b15453efe"),
                    manager_level=ManagerLevel(
                        uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                        name="Niveau 4",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("267e5e49-3abd-49df-9bd9-38d41d2294ff"),
                        name="Direktør",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        OrgUnitManagers(
            uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
            name="Social og sundhed_leder",
            parent_uuid=UUID("a6773531-6c0a-4c7b-b0e2-77992412b610"),
            child_count=0,
            managers=[
                Manager(
                    uuid=UUID("a8ff5cb0-8a59-4614-a41c-453df25007cc"),
                    employee_uuid=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                    manager_level=ManagerLevel(
                        uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38"),
                        name="Niveau 2",
                    ),
                    manager_type=ManagerType(
                        uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8"),
                        name="Områdeleder",
                    ),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
    ],
]

expected_managers = [
    OrgUnitManagers(
        uuid=UUID("72d8e92f-9481-43af-8cb0-a83823c9f35e"),
        name="Almind skole_leder ",
        parent_uuid=UUID("bc876b6c-3682-5b60-804b-95ff759b5509"),
        child_count=0,
        managers=[
            Manager(
                uuid=UUID("649fc94c-4897-4421-a9f6-fb06c43e5f4e"),
                employee_uuid=UUID("08c31328-17aa-48c2-8293-3fc6f59ebe9c"),
                manager_level=ManagerLevel(
                    uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38"), name="Niveau 2"
                ),
                manager_type=ManagerType(
                    uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8"),
                    name="Områdeleder",
                ),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
    OrgUnitManagers(
        uuid=UUID("60370b40-a143-40c5-aaa1-638b3b74d119"),
        name="Social Indsats_LEDER",
        parent_uuid=UUID("535ba446-d618-4e51-8dae-821d63e26560"),
        child_count=3,
        managers=[
            Manager(
                uuid=UUID("8250d35b-fab6-4c9e-95ab-da52848f9df9"),
                employee_uuid=UUID("0790ca9c-f3ae-4e4b-b936-03b8aedf5314"),
                manager_level=ManagerLevel(
                    uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38"), name="Niveau 2"
                ),
                manager_type=ManagerType(
                    uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8"),
                    name="Områdeleder",
                ),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
    OrgUnitManagers(
        uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
        name="Social og sundhed_leder",
        parent_uuid=UUID("a6773531-6c0a-4c7b-b0e2-77992412b610"),
        child_count=0,
        managers=[
            Manager(
                uuid=UUID("a8ff5cb0-8a59-4614-a41c-453df25007cc"),
                employee_uuid=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                manager_level=ManagerLevel(
                    uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38"), name="Niveau 2"
                ),
                manager_type=ManagerType(
                    uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8"),
                    name="Områdeleder",
                ),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
]


org_unit_models = [
    OrgUnitManagers(
        uuid=UUID("7133da92-e624-56c9-8e23-bac319a537e1"),
        name="Administration",
        parent_uuid=UUID("1caba8d9-6b9f-506b-b845-9a8c4f5b8a03"),
        child_count=2,
        managers=[
            Manager(
                uuid=UUID("36b5be05-7323-418f-bbd4-7be23c9ca150"),
                employee_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                manager_level=ManagerLevel(
                    uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"), name="Niveau 4"
                ),
                manager_type=ManagerType(
                    uuid=UUID("267e5e49-3abd-49df-9bd9-38d41d2294ff"), name="Direktør"
                ),
                validity=Validity(
                    from_date=datetime(1977, 3, 2, 0, 0, tzinfo=tzoffset(None, 3600)),
                    to_date=None,
                ),
            )
        ],
    ),
    OrgUnitManagers(
        uuid=UUID("6e629aef-4e5a-537a-8320-5e05015685f6"),
        name="Teknisk Support",
        parent_uuid=UUID("316358a3-6007-5802-af99-656a19999f0c"),
        child_count=0,
        managers=[
            Manager(
                uuid=UUID("a9409fb0-a00e-490e-a429-c153385fb880"),
                employee_uuid=UUID("d9c71751-8afa-40c7-8b89-498db8c775d2"),
                manager_level=ManagerLevel(
                    uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"), name="Niveau 4"
                ),
                manager_type=ManagerType(
                    uuid=UUID("267e5e49-3abd-49df-9bd9-38d41d2294ff"), name="Direktør"
                ),
                validity=Validity(
                    from_date=datetime(2022, 1, 1, 0, 0, tzinfo=tzoffset(None, 3600)),
                    to_date=None,
                ),
            )
        ],
    ),
]


def get_sample_data() -> tuple[list, list]:
    """Sample data for unit test of fetching '_leder' org-units."""
    return org_unit_samples, expected_managers


def get_org_unit_models_sample() -> tuple[dict, list]:
    """Sample data for test_util.test_get_manager_org_units"""
    return graphql_payload, org_unit_models
