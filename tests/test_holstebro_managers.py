# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import Callable
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from gql import gql  # type: ignore
from graphql import DocumentNode
from more_itertools import one

from sd_managerscript.holstebro_managers import query_graphql
from sd_managerscript.main import create_app


@pytest.fixture
def fastapi_app_builder() -> Generator[Callable[..., FastAPI], None, None]:
    """Fixture for the FastAPI app builder."""

    def builder(*args: Any, default_args: bool = True, **kwargs: Any) -> FastAPI:
        if default_args:
            kwargs["client_secret"] = "hunter2"
        return create_app(*args, **kwargs)

    yield builder


@pytest.fixture
def test_client_builder(
    fastapi_app_builder: Callable[..., FastAPI]
) -> Generator[Callable[..., TestClient], None, None]:
    """Fixture for the FastAPI test client builder."""

    def builder(*args: Any, **kwargs: Any) -> TestClient:
        return TestClient(fastapi_app_builder(*args, **kwargs))

    yield builder


@pytest.fixture
def test_client(
    test_client_builder: Callable[..., TestClient]
) -> Generator[TestClient, None, None]:
    """Fixture for the FastAPI test client."""
    yield test_client_builder(client_secret="hunter2")


QUERY_ORG_UNITS = gql(
    """
    query ($uuid: [UUID!]!){
        org_units (uuids: $uuid){
            objects {
                uuid
                name
                parent_uuid
                child_count
                managers {
                    uuid
                    employee_uuid
                    manager_level {
                        name
                        uuid
                    }
                    manager_type {
                        name
                        uuid
                    }
                }
            }
        }
    }
"""
)


async def test_query_graphql() -> None:
    """Test we get the correct response from query_graphql."""
    input = {"uuid": "08eaf849-e9f9-53e0-b6b9-3cd45763ecbb"}
    params: dict[str, Any] = {}

    async def execute(*args: Any, **kwargs: Any) -> dict[str, Any]:
        params["args"] = args
        params["kwargs"] = kwargs

        return {
            "org_units": [
                {
                    "objects": [
                        {
                            "uuid": "08eaf849-e9f9-53e0-b6b9-3cd45763ecbb",
                            "name": "Viuf skole",
                            "parent_uuid": "2665d8e0-435b-5bb6-a550-f275692984ef",
                            "child_count": 0,
                            "managers": [
                                {
                                    "uuid": "ab1adf81-1c56-46ce-bd81-8cc536212c12",
                                    "employee_uuid": "8315443f-a918-4eea-9605-150472418101",
                                    "manager_level": {
                                        "name": "Niveau 4",
                                        "uuid": "9a2bbe63-b7b4-4b3d-9b47-9d7dd391b42c",
                                    },
                                    "manager_type": {
                                        "name": "Direktør",
                                        "uuid": "267e5e49-3abd-49df-9bd9-38d41d2294ff",
                                    },
                                }
                            ],
                        }
                    ]
                }
            ]
        }

    session = MagicMock()
    session.execute = execute
    result = await query_graphql(session, QUERY_ORG_UNITS, input)
    assert len(params["args"]) == 1
    assert len(params["kwargs"]) == 1
    assert isinstance(params["args"][0], DocumentNode)
    assert params["kwargs"]["variable_values"]["uuid"] == input["uuid"]
    assert one(one(result["org_units"])["objects"])["uuid"] == input["uuid"]
