# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Collection
from collections.abc import Iterable
from datetime import datetime
from uuid import UUID

from dateutil.tz import tzoffset  # type: ignore
from gql import gql  # type: ignore
from ramodels.mo._shared import Validity  # type: ignore

from sd_managerscript.models import Association
from sd_managerscript.models import Manager
from sd_managerscript.models import ManagerLevel
from sd_managerscript.models import ManagerType
from sd_managerscript.models import OrgUnitManagers
from sd_managerscript.models import Parent


org_unit_samples = [
    [
        OrgUnitManagers(
            uuid=UUID("08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"),
            name="Viuf skole",
            child_count=1,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            uuid=UUID("1e28b010-67a9-5e0b-b6b5-432a00e9be35"),
            name="Tjerre skole",
            child_count=2,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[],
        ),
        OrgUnitManagers(
            uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
            name="Sønder Stenderup skole",
            child_count=-2,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[],
        ),
        OrgUnitManagers(
            uuid=UUID("1caba8d9-6b9f-506b-b845-9a8c4f5b8a03"),
            name="Jordrup børnehus",
            child_count=1,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            child_count=3,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            1977, 3, 2, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        OrgUnitManagers(
            uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
            name="Social og sundhed_leder",
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
            name="Ø_Social og sundhed 666_leder",
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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

graphql_payload = {
    "org_units": [
        {
            "objects": [
                {
                    "uuid": "7133da92-e624-56c9-8e23-bac319a537e1",
                    "name": "Administration",
                    "child_count": 2,
                    "parent": {
                        "uuid": "ab1adf81-1c56-46ce-bd81-8cc536212c12",
                        "name": "Skoler",
                        "parent_uuid": "1caba8d9-6b9f-506b-b845-9a8c4f5b8a03",
                        "org_unit_level_uuid": "09c347ef-451f-5919-8d41-02cc989a6d8b",
                    },
                    "associations": [
                        {
                            "uuid": "36b5be05-7323-418f-bbd4-7be23c9ca150",
                            "employee": "4c88d5a3-199f-454b-9349-a24ab218ca54",
                            "org_unit": "7133da92-e624-56c9-8e23-bac319a537e1",
                            "association_type": "2665d8e0-435b-5bb6-a550-f275692984ef",
                            "validity": {
                                "to": None,
                                "from": "1977-03-02T00:00:00+02:00",
                            },
                        }
                    ],
                }
            ]
        },
        {
            "objects": [
                {
                    "uuid": "100b9d19-3190-490f-94f9-759b6b24172a",
                    "name": "Teknisk Support",
                    "child_count": 0,
                    "parent": {
                        "uuid": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
                        "name": "Skoler",
                        "parent_uuid": "1caba8d9-6b9f-506b-b845-9a8c4f5b8a03",
                        "org_unit_level_uuid": "09c347ef-451f-5919-8d41-02cc989a6d8b",
                    },
                    "associations": [
                        {
                            "uuid": "ab1adf81-1c56-46ce-bd81-8cc536212c12",
                            "employee": "8315443f-a918-4eea-9605-150472418101",
                            "org_unit": "100b9d19-3190-490f-94f9-759b6b24172a",
                            "association_type": "2665d8e0-435b-5bb6-a550-f275692984ef",
                            "validity": {
                                "to": None,
                                "from": "2022-08-01T00:00:00+02:00",
                            },
                        }
                    ],
                }
            ]
        },
    ]
}

org_unit_models = [
    OrgUnitManagers(
        uuid=UUID("7133da92-e624-56c9-8e23-bac319a537e1"),
        name="Administration",
        child_count=2,
        parent=Parent(
            uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
            name="Skoler",
            parent_uuid=UUID("1caba8d9-6b9f-506b-b845-9a8c4f5b8a03"),
            org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
        ),
        associations=[
            Association(
                uuid=UUID("36b5be05-7323-418f-bbd4-7be23c9ca150"),
                employee=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                org_unit=UUID("7133da92-e624-56c9-8e23-bac319a537e1"),
                association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date=datetime(1977, 3, 2, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
    OrgUnitManagers(
        uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
        name="Teknisk Support",
        child_count=0,
        parent=Parent(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="Skoler",
            parent_uuid=UUID("1caba8d9-6b9f-506b-b845-9a8c4f5b8a03"),
            org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
        ),
        associations=[
            Association(
                uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
                association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
]

expected_managers = [
    OrgUnitManagers(
        uuid=UUID("72d8e92f-9481-43af-8cb0-a83823c9f35e"),
        name="Almind skole_leder ",
        child_count=0,
        parent=Parent(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="Skoler",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
        ),
        associations=[
            Association(
                uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
        child_count=3,
        parent=Parent(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="Skoler",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
        ),
        associations=[
            Association(
                uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
    OrgUnitManagers(
        uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
        name="Social og sundhed_leder",
        child_count=0,
        parent=Parent(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="Skoler",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
        ),
        associations=[
            Association(
                uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
]


data_get_active_engagements = [
    (  # Test "normal" case
        "0b5936f2-328d-448e-bfb9-d655e6d3d849",
        {
            "engagements": [
                {
                    "objects": [
                        {
                            "validity": {
                                "from": "1982-12-31T00:00:00+01:00",
                                "to": None,
                            }
                        }
                    ]
                }
            ]
        },
        {
            "employee_uuid": "0b5936f2-328d-448e-bfb9-d655e6d3d849",
            "engagement_from": "1982-12-31T00:00:00+01:00",
        },
    ),
    (  # Test Engagement with from date in future
        "0790ca9c-f3ae-4e4b-b936-03b8aedf5314",
        {
            "engagements": [
                {
                    "objects": [
                        {
                            "validity": {
                                "from": "2050-12-31T00:00:00+01:00",
                                "to": None,
                            }
                        }
                    ]
                }
            ]
        },
        {
            "employee_uuid": "0790ca9c-f3ae-4e4b-b936-03b8aedf5314",
            "engagement_from": "2050-12-31T00:00:00+01:00",
        },
    ),
    (  # Test with multiple engagements
        "05d2415b-a9e7-4b8a-bdd4-0d5ea74a457e",
        {
            "engagements": [
                {
                    "objects": [
                        {
                            "validity": {
                                "from": "1982-12-31T00:00:00+01:00",
                                "to": None,
                            }
                        }
                    ]
                },
                {
                    "objects": [
                        {
                            "validity": {
                                "from": "2022-09-30T00:00:00+01:00",
                                "to": None,
                            }
                        }
                    ]
                },
            ]
        },
        {
            "employee_uuid": "05d2415b-a9e7-4b8a-bdd4-0d5ea74a457e",
            "engagement_from": "2022-09-30T00:00:00+01:00",
        },
    ),
    (  # Test with no engagements
        "07d2415b-a9e7-4b8a-bdd4-0d5ea74a457e",
        {"engagements": []},
        {
            "employee_uuid": "07d2415b-a9e7-4b8a-bdd4-0d5ea74a457e",
            "engagement_from": None,
        },
    ),
]

filter_managers_data = [
    (  # Test with two potential managers
        OrgUnitManagers(
            uuid=UUID("7133da92-e624-56c9-8e23-bac319a537e1"),
            name="Administration",
            child_count=2,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Some Unit",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("36b5be05-7323-418f-bbd4-7be23c9ca150"),
                    employee=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date="1978-01-01T00:00:00+01:00",
                        to_date=None,
                    ),
                ),
                Association(
                    uuid=UUID("a8ff5cb0-8a59-4614-a41c-453df25007cc"),
                    employee=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date="1978-01-01T00:00:00+01:00",
                        to_date=None,
                    ),
                ),
            ],
        ),
        [
            {
                "employee_uuid": "4c88d5a3-199f-454b-9349-a24ab218ca54",
                "engagement_from": "1989-04-01T00:00:00+01:00",
            },
            {
                "employee_uuid": "03ff3b1a-a16b-4ea6-b372-065a77f849cb",
                "engagement_from": "1996-04-01T00:00:00+01:00",
            },
        ],
        OrgUnitManagers(
            uuid=UUID("7133da92-e624-56c9-8e23-bac319a537e1"),
            name="Administration",
            child_count=2,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Some Unit",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("a8ff5cb0-8a59-4614-a41c-453df25007cc"),
                    employee=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date="1978-01-01T00:00:00+01:00",
                        to_date=None,
                    ),
                ),
            ],
        ),
    ),
    (  # Test with one potential manager
        OrgUnitManagers(
            uuid=UUID("6e629aef-4e5a-537a-8320-5e05015685f6"),
            name="Teknisk Support",
            child_count=0,
            parent=Parent(
                uuid=UUID("316358a3-6007-5802-af99-656a19999f0c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("a9409fb0-a00e-490e-a429-c153385fb880"),
                    employee=UUID("d9c71751-8afa-40c7-8b89-498db8c775d2"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date="1978-01-01",
                        to_date=None,
                    ),
                )
            ],
        ),
        [
            {
                "employee_uuid": "d9c71751-8afa-40c7-8b89-498db8c775d2",
                "engagement_from": "1998-07-01T00:00:00+01:00",
            }
        ],
        OrgUnitManagers(
            uuid=UUID("6e629aef-4e5a-537a-8320-5e05015685f6"),
            name="Teknisk Support",
            child_count=0,
            parent=Parent(
                uuid=UUID("316358a3-6007-5802-af99-656a19999f0c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("a9409fb0-a00e-490e-a429-c153385fb880"),
                    employee=UUID("d9c71751-8afa-40c7-8b89-498db8c775d2"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date="1978-01-01",
                        to_date=None,
                    ),
                )
            ],
        ),
    ),
]

# Test with two potential managers and same engagement date raises error
filter_managers_data_fail = (
    OrgUnitManagers(
        uuid=UUID("7133da92-e624-56c9-8e23-bac319a537e1"),
        name="Administration",
        child_count=2,
        parent=Parent(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="Some Unit",
            parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
        ),
        associations=[
            Association(
                uuid=UUID("a8ff5cb0-8a59-4614-a41c-453df25007cc"),
                employee=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date="1998-01-01T00:00:00+01:00",
                    to_date=None,
                ),
            ),
            Association(
                uuid=UUID("1caba8d9-6b9f-506b-b845-9a8c4f5b8a03"),
                employee=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date="1998-01-01T00:00:00+01:00",
                    to_date=None,
                ),
            ),
        ],
    ),
    [
        {
            "employee_uuid": "4c88d5a3-199f-454b-9349-a24ab218ca54",
            "engagement_from": "1988-10-12T00:00:00+01:00",
        },
        {
            "employee_uuid": "03ff3b1a-a16b-4ea6-b372-065a77f849cb",
            "engagement_from": "1988-10-12T00:00:00+01:00",
        },
    ],
)

filter_managers_terminate = [
    (
        OrgUnitManagers(
            uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
            name="Social og sundhed_leder",
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        [
            {
                "employee_uuid": "4c88d5a3-199f-454b-9349-a24ab218ca54",
                "engagement_from": None,
            },
        ],
        [UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12")],
    ),
    (
        OrgUnitManagers(
            uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
            name="Social og sundhed_leder",
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("09c347ef-451f-5919-8d41-02cc989a6d8b"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                ),
                Association(
                    uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    employee=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                ),
                Association(
                    uuid=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                    employee=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                    org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                ),
            ],
        ),
        [
            {
                "employee_uuid": "4c88d5a3-199f-454b-9349-a24ab218ca54",
                "engagement_from": "2002-10-12T00:00:00+01:00",
            },
            {
                "employee_uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2",
                "engagement_from": "1978-10-12T00:00:00+01:00",
            },
            {
                "employee_uuid": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
                "engagement_from": "1988-10-12T00:00:00+01:00",
            },
        ],
        [
            UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
            UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
        ],
    ),
]

updata_manager_data = [
    (  # Test update manager
        Manager(
            uuid=UUID("585675fe-8e2a-43a1-b0d9-7879a669c347"),
            manager_level=ManagerLevel(
                uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38")
            ),
            manager_type=ManagerType(uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8")),
            employee=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
            responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
            validity=Validity(
                from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                to_date=None,
            ),
        ),
        gql(
            """
        mutation UpdateManager($input: ManagerUpdateInput!) {
            manager_update(input: $input) {
                uuid
            }
        }
    """
        ),
        "585675fe-8e2a-43a1-b0d9-7879a669c347",
        {
            "input": {
                "uuid": "585675fe-8e2a-43a1-b0d9-7879a669c347",
                "manager_level": {"uuid": "d09ba017-f838-4742-b57e-44c2f5437e38"},
                "manager_type": {"uuid": "54d6ad15-d966-4523-8728-37718e3c46a8"},
                "validity": {"from": "2022-08-01T00:00:00+02:00", "to": None},
                "employee": "03ff3b1a-a16b-4ea6-b372-065a77f849cb",
                "responsibility": "d82039a5-f2d5-48e4-8eab-8c9f7694e16f",
            }
        },
    ),
    (  # Test create manager
        Manager(
            uuid=UUID("585675fe-8e2a-43a1-b0d9-7879a669c347"),
            manager_level=ManagerLevel(
                uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38")
            ),
            manager_type=ManagerType(uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8")),
            employee=UUID("0790ca9c-f3ae-4e4b-b936-03b8aedf5314"),
            responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
            validity=Validity(
                from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                to_date=None,
            ),
        ),
        gql(
            """
        mutation CreateManager($input: ManagerCreateInput!) {
            manager_create(input: $input) {
                uuid
            }
        }
    """
        ),
        None,
        {
            "input": {
                "uuid": "585675fe-8e2a-43a1-b0d9-7879a669c347",
                "manager_level": {"uuid": "d09ba017-f838-4742-b57e-44c2f5437e38"},
                "manager_type": {"uuid": "54d6ad15-d966-4523-8728-37718e3c46a8"},
                "validity": {"from": "2022-08-01T00:00:00+02:00", "to": None},
                "employee": "0790ca9c-f3ae-4e4b-b936-03b8aedf5314",
                "responsibility": "d82039a5-f2d5-48e4-8eab-8c9f7694e16f",
            }
        },
    ),
]

create_manager_sample = [
    (
        UUID("8315443f-a918-4eea-9605-150472418101"),
        datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
        ManagerLevel(
            uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
        ),
        Manager(
            uuid=None,
            employee=UUID("8315443f-a918-4eea-9605-150472418101"),
            responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
            manager_level=ManagerLevel(
                uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
            ),
            manager_type=ManagerType(
                uuid=UUID("75fee2b6-f405-4c77-b62e-32421c2e43d5"),
            ),
            validity=Validity(
                to_date=None,
                from_date="2022-08-01T00:00:00+02:00",
            ),
        ),
    ),
    (
        UUID("8315443f-a918-4eea-9605-150472418101"),
        datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
        ManagerLevel(
            uuid=UUID("e226821b-4af3-1e91-c53f-ea5c57c6d8d0"),
        ),
        Manager(
            uuid=None,
            employee=UUID("8315443f-a918-4eea-9605-150472418101"),
            responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
            manager_level=ManagerLevel(
                uuid=UUID("e226821b-4af3-1e91-c53f-ea5c57c6d8d0"),
            ),
            manager_type=ManagerType(
                uuid=UUID("75fee2b6-f405-4c77-b62e-32421c2e43d5"),
            ),
            validity=Validity(
                to_date=None,
                from_date="2022-08-01T00:00:00+02:00",
            ),
        ),
    ),
]

get_manager_lvl_sample = [
    (
        OrgUnitManagers(
            uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
            name="Social og sundhed_leder",
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("0263522a-2c1e-9c80-1880-92c1b97cfead"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        None,
        ManagerLevel(
            uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
        ),
    ),
    (
        OrgUnitManagers(
            uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
            name="Hjemmeskolen",
            child_count=0,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Skoler_led-adm",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("0263522a-2c1e-9c80-1880-92c1b97cfead"),
            ),
            associations=[
                Association(
                    uuid=UUID("ab1adf81-1c56-46ce-bd81-8cc536212c12"),
                    employee=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                ),
            ],
        ),
        OrgUnitManagers(
            uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
            name="Skoler_led-adm",
            child_count=2,
            parent=Parent(
                uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                name="Some Unit",
                parent_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                org_unit_level_uuid=UUID("891603db-cc28-6ed2-6d48-25e14d3f142f"),
            ),
            associations=[
                Association(
                    uuid=UUID("a8ff5cb0-8a59-4614-a41c-453df25007cc"),
                    employee=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    org_unit=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type=UUID("891603db-cc28-6ed2-6d48-25e14d3f142f"),
                    validity=Validity(
                        from_date="1998-01-01T00:00:00+01:00",
                        to_date=None,
                    ),
                )
            ],
        ),
        ManagerLevel(
            uuid=UUID("e226821b-4af3-1e91-c53f-ea5c57c6d8d0"),
        ),
    ),
]


def get_sample_data() -> tuple[list[list[OrgUnitManagers]], list[OrgUnitManagers]]:
    """Sample data for unit test of fetching '_leder' org-units."""
    return org_unit_samples, expected_managers


def get_org_unit_models_sample() -> tuple[dict, list]:
    """Sample data for test_util.test_get_manager_org_units"""
    return graphql_payload, org_unit_models


def get_active_engagements_data() -> Iterable[tuple[str, object, object]]:
    yield from data_get_active_engagements


def get_filter_managers_data() -> Iterable[
    tuple[OrgUnitManagers, list[dict[str, str]], OrgUnitManagers]
]:
    yield from filter_managers_data


def get_filter_managers_error_data() -> tuple[OrgUnitManagers, list[dict]]:
    return filter_managers_data_fail


def get_filter_managers_terminate() -> list[tuple[OrgUnitManagers, object, list[UUID]]]:
    return filter_managers_terminate


def get_update_managers_data() -> list[
    tuple[Manager, gql, str | None, dict[str, dict[str, Collection[str]]]]
]:
    return updata_manager_data


def get_create_manager_data() -> list[tuple[UUID, datetime, ManagerLevel, Manager]]:
    return create_manager_sample


def get_manager_level_data() -> list[
    tuple[OrgUnitManagers, OrgUnitManagers | None, ManagerLevel]
]:
    return get_manager_lvl_sample
