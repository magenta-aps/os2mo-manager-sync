# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Collection
from collections.abc import Iterable
from collections.abc import Sequence
from datetime import datetime
from typing import Any
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                            "employee_uuid": "4c88d5a3-199f-454b-9349-a24ab218ca54",
                            "org_unit_uuid": "7133da92-e624-56c9-8e23-bac319a537e1",
                            "association_type_uuid": "2665d8e0-435b-5bb6-a550-f275692984ef",
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
                            "employee_uuid": "8315443f-a918-4eea-9605-150472418101",
                            "org_unit_uuid": "100b9d19-3190-490f-94f9-759b6b24172a",
                            "association_type_uuid": "2665d8e0-435b-5bb6-a550-f275692984ef",
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

unengaged_managers_sample = [
    (  # Test with two different engagements (can it match by org_unit_uuid?)
        {
            "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
            "objects": [
                {
                    "child_count": 2,
                    "managers": [
                        {
                            "uuid": "5a988dee-109a-4353-95f2-fb414ea8d605",
                            "employee": [
                                {
                                    "engagements": [
                                        {
                                            "org_unit_uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
                                            "validity": {
                                                "from": "2019-02-20T00:00:00+01:00",
                                                "to": None,
                                            },
                                        },
                                        {
                                            "org_unit_uuid": "09c347ef-451f-5919-8d41-02cc989a6d8b",
                                            "validity": {
                                                "from": "2022-11-20T00:00:00+01:00",
                                                "to": None,
                                            },
                                        },
                                    ]
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        None,
    ),
    (  # Test no engagements
        {
            "uuid": "96a4715c-f4df-422f-a4b0-9dcc686753f7",
            "objects": [
                {
                    "child_count": 0,
                    "managers": [
                        {
                            "uuid": "37dbbd86-1e4f-4292-a9a7-f92be4b7371e",
                            "employee": [{"engagements": []}],
                        }
                    ],
                }
            ],
        },
        UUID("37dbbd86-1e4f-4292-a9a7-f92be4b7371e"),
    ),
    (  # Test to-date before today (no active engagement)
        {
            "uuid": "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",
            "objects": [
                {
                    "child_count": 0,
                    "managers": [
                        {
                            "uuid": "a8d51c1d-bcb2-4650-80f3-3b2ab630bc5e",
                            "employee": [
                                {
                                    "engagements": [
                                        {
                                            "org_unit_uuid": "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",
                                            "validity": {
                                                "from": "2021-02-09T00:00:00+01:00",
                                                "to": "2022-07-26T00:00:00+02:00",
                                            },
                                        }
                                    ]
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        UUID("a8d51c1d-bcb2-4650-80f3-3b2ab630bc5e"),
    ),
    (  # Test NO managers
        {
            "uuid": "18443c6b-dbd4-58eb-984e-25b6350d9f50",
            "objects": [
                {
                    "child_count": 0,
                    "managers": [],
                }
            ],
        },
        None,
    ),
]

engagement_samples = [
    {
        "org_units": [
            {
                "uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",
                "objects": [
                    {
                        "child_count": 2,
                        "managers": [
                            {
                                "uuid": "5a988dee-109a-4353-95f2-fb414ea8d605",
                                "employee": [
                                    {
                                        "engagements": [
                                            {
                                                "org_unit_uuid": "1f06ed67-aa6e-4bbc-96d9-2f262b9202b5",  # noqa: E501
                                                "validity": {
                                                    "from": "2019-02-20T00:00:00+01:00",
                                                    "to": None,
                                                },
                                            },
                                            {
                                                "org_unit_uuid": "09c347ef-451f-5919-8d41-02cc989a6d8b",  # noqa: E501
                                                "validity": {
                                                    "from": "2022-11-20T00:00:00+01:00",
                                                    "to": None,
                                                },
                                            },
                                        ]
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "uuid": "25e39a21-caef-4e96-ac90-7cc27173082e",
                "objects": [
                    {
                        "child_count": 0,
                        "managers": [
                            {
                                "uuid": "a9894c2b-8eaa-4487-97c9-9644fb22f93e",
                                "employee": [
                                    {
                                        "engagements": [
                                            {
                                                "org_unit_uuid": "25e39a21-caef-4e96-ac90-7cc27173082e",  # noqa: E501
                                                "validity": {
                                                    "from": "1979-04-21T00:00:00+01:00",
                                                    "to": None,
                                                },
                                            }
                                        ]
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "uuid": "96a4715c-f4df-422f-a4b0-9dcc686753f7",
                "objects": [
                    {
                        "child_count": 0,
                        "managers": [
                            {
                                "uuid": "37dbbd86-1e4f-4292-a9a7-f92be4b7371e",
                                "employee": [{"engagements": []}],
                            }
                        ],
                    }
                ],
            },
            {
                "uuid": "e054559b-bc15-4203-bced-44375aed1555",
                "objects": [
                    {
                        "child_count": 0,
                        "managers": [
                            {
                                "uuid": "f000416d-193d-45da-a405-bf95fe4f65d1",
                                "employee": [
                                    {
                                        "engagements": [
                                            {
                                                "org_unit_uuid": "96a4715c-f4df-422f-a4b0-9dcc686753f7",  # noqa: E501
                                                "validity": {
                                                    "from": "1987-12-05T00:00:00+01:00",
                                                    "to": None,
                                                },
                                            }
                                        ]
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                "uuid": "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",
                "objects": [
                    {
                        "child_count": 0,
                        "managers": [
                            {
                                "uuid": "a8d51c1d-bcb2-4650-80f3-3b2ab630bc5e",
                                "employee": [
                                    {
                                        "engagements": [
                                            {
                                                "org_unit_uuid": "f1c20ee2-ecbb-4b74-b91c-66ef9831c5cd",  # noqa: E501
                                                "validity": {
                                                    "from": "2021-02-09T00:00:00+01:00",
                                                    "to": "2022-07-26T00:00:00+02:00",
                                                },
                                            }
                                        ]
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
        ]
    },
    {
        "org_units": [
            {
                "uuid": "0c655440-867d-561e-8c28-2aa0ac8d1e20",
                "objects": [
                    {
                        "child_count": 0,
                        "managers": [
                            {
                                "uuid": "d0d0ab19-f69d-425e-a089-76610e8329dc",
                                "employee": [{"engagements": []}],
                            }
                        ],
                    }
                ],
            },
            {
                "uuid": "18443c6b-dbd4-58eb-984e-25b6350d9f50",
                "objects": [
                    {
                        "child_count": 0,
                        "managers": [],
                    }
                ],
            },
        ]
    },
]

expected_managers_list = [
    None,
    None,
    UUID("37dbbd86-1e4f-4292-a9a7-f92be4b7371e"),
    None,
    UUID("a8d51c1d-bcb2-4650-80f3-3b2ab630bc5e"),
    UUID("f000416d-193d-45da-a405-bf95fe4f65d1"),
    None,
]

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
                employee_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                org_unit_uuid=UUID("7133da92-e624-56c9-8e23-bac319a537e1"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit_uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date="1978-01-01T00:00:00+01:00",
                        to_date=None,
                    ),
                ),
                Association(
                    uuid=UUID("a8ff5cb0-8a59-4614-a41c-453df25007cc"),
                    employee_uuid=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("d9c71751-8afa-40c7-8b89-498db8c775d2"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("d9c71751-8afa-40c7-8b89-498db8c775d2"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                employee_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date="1998-01-01T00:00:00+01:00",
                    to_date=None,
                ),
            ),
            Association(
                uuid=UUID("1caba8d9-6b9f-506b-b845-9a8c4f5b8a03"),
                employee_uuid=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                ),
                Association(
                    uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    employee_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    org_unit_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                ),
                Association(
                    uuid=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
                    employee_uuid=UUID("9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c"),
                    org_unit_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
            uuid=None,
            manager_level=ManagerLevel(
                uuid=UUID("d09ba017-f838-4742-b57e-44c2f5437e38")
            ),
            manager_type=ManagerType(uuid=UUID("54d6ad15-d966-4523-8728-37718e3c46a8")),
            employee=UUID("03ff3b1a-a16b-4ea6-b372-065a77f849cb"),
            responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
            org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
            validity=Validity(
                from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                to_date=None,
            ),
        ),
        "08c85974-8929-456a-a166-efc7230ac5b7",
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
                "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
                "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
                "validity": {"from": "2022-08-01T00:00:00+02:00", "to": None},
                "person": "03ff3b1a-a16b-4ea6-b372-065a77f849cb",
                "responsibility": "d82039a5-f2d5-48e4-8eab-8c9f7694e16f",
                "org_unit": "08c85974-8929-456a-a166-efc7230ac5b7",
            }
        },
    ),
    (  # Test create manager
        Manager(
            uuid=None,
            org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
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
        "c935454a-e1ba-4bb4-bfca-853c0d69f35b",
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
                "uuid": None,
                "manager_level": "d09ba017-f838-4742-b57e-44c2f5437e38",
                "manager_type": "54d6ad15-d966-4523-8728-37718e3c46a8",
                "validity": {"from": "2022-08-01T00:00:00+02:00", "to": None},
                "person": "0790ca9c-f3ae-4e4b-b936-03b8aedf5314",
                "responsibility": "d82039a5-f2d5-48e4-8eab-8c9f7694e16f",
                "org_unit": "c935454a-e1ba-4bb4-bfca-853c0d69f35b",
            }
        },
    ),
]

create_manager_sample = [
    (
        OrgUnitManagers(
            uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        ManagerLevel(
            uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
        ),
        Manager(
            uuid=None,
            employee=UUID("8315443f-a918-4eea-9605-150472418101"),
            responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
            org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
            manager_level=ManagerLevel(
                uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
            ),
            manager_type=ManagerType(
                uuid=UUID("75fee2b6-f405-4c77-b62e-32421c2e43d5"),
            ),
            validity=Validity(
                to_date=None,
                from_date="2019-01-14",
            ),
        ),
    ),
    (
        OrgUnitManagers(
            uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                )
            ],
        ),
        ManagerLevel(
            uuid=UUID("e226821b-4af3-1e91-c53f-ea5c57c6d8d0"),
        ),
        Manager(
            uuid=None,
            employee=UUID("8315443f-a918-4eea-9605-150472418101"),
            responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
            org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
            manager_level=ManagerLevel(
                uuid=UUID("e226821b-4af3-1e91-c53f-ea5c57c6d8d0"),
            ),
            manager_type=ManagerType(
                uuid=UUID("75fee2b6-f405-4c77-b62e-32421c2e43d5"),
            ),
            validity=Validity(
                to_date=None,
                from_date="2019-01-14",
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
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
                    employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                    org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                    association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                    validity=Validity(
                        from_date=datetime(
                            2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)
                        ),
                        to_date=None,
                    ),
                ),
            ],
        ),
        {
            "org_units": [
                {
                    "objects": [
                        {"org_unit_level_uuid": "891603db-cc28-6ed2-6d48-25e14d3f142f"}
                    ]
                }
            ]
        },
        ManagerLevel(
            uuid=UUID("e226821b-4af3-1e91-c53f-ea5c57c6d8d0"),
        ),
    ),
]

get_create_update_manager_sample = (
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
                employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit_uuid=UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
    ManagerLevel(
        uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
    ),
    Manager(
        uuid=None,
        employee=UUID("8315443f-a918-4eea-9605-150472418101"),
        responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
        org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
        manager_level=ManagerLevel(
            uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
        ),
        manager_type=ManagerType(
            uuid=UUID("75fee2b6-f405-4c77-b62e-32421c2e43d5"),
        ),
        validity=Validity(
            to_date=None,
            from_date="2022-05-01T00:00:00+02:00",
        ),
    ),
)

get_create_update_manager_led_adm_sample = (
    OrgUnitManagers(
        uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
        name="Social og sundhed_leder",
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
                employee_uuid=UUID("8315443f-a918-4eea-9605-150472418101"),
                org_unit_uuid=UUID("100b9d19-3190-490f-94f9-759b6b24172a"),
                association_type_uuid=UUID("2665d8e0-435b-5bb6-a550-f275692984ef"),
                validity=Validity(
                    from_date=datetime(2022, 8, 1, 0, 0, tzinfo=tzoffset(None, 7200)),
                    to_date=None,
                ),
            )
        ],
    ),
    ManagerLevel(
        uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
    ),
    Manager(
        uuid=None,
        employee=UUID("8315443f-a918-4eea-9605-150472418101"),
        responsibility=UUID("d82039a5-f2d5-48e4-8eab-8c9f7694e16f"),
        org_unit=UUID("4c88d5a3-199f-454b-9349-a24ab218ca54"),
        manager_level=ManagerLevel(
            uuid=UUID("a8754726-a4b9-1715-6b41-769c6fe703c5"),
        ),
        manager_type=ManagerType(
            uuid=UUID("75fee2b6-f405-4c77-b62e-32421c2e43d5"),
        ),
        validity=Validity(
            to_date=None,
            from_date="2022-05-01T00:00:00+02:00",
        ),
    ),
)


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


def get_update_managers_data() -> list[tuple[Manager, str, Any, str | None, object]]:
    return updata_manager_data


def get_create_manager_data() -> list[tuple[OrgUnitManagers, ManagerLevel, Manager]]:
    return create_manager_sample


def get_manager_level_data() -> list[
    tuple[
        OrgUnitManagers,
        dict[str, list[dict[str, list[dict[str, str]]]]] | None,
        ManagerLevel,
    ]
]:
    return get_manager_lvl_sample


def get_create_update_manager_data() -> tuple[OrgUnitManagers, ManagerLevel, Manager]:
    return get_create_update_manager_sample


def get_create_update_manager_led_adm_data() -> tuple[
    OrgUnitManagers, ManagerLevel, Manager
]:
    return get_create_update_manager_led_adm_sample


def get_manager_engagement_data() -> tuple[
    list[dict[str, list[dict[str, Sequence[Collection[str]]]]]], list[UUID | None]
]:
    return engagement_samples, expected_managers_list


def get_unengaged_managers_data() -> list[
    tuple[dict[str, Sequence[Collection[str]]], UUID | None]
]:
    return unengaged_managers_sample
