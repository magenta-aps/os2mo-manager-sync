# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextlib import AsyncExitStack
from typing import Any

import structlog
from fastapi import FastAPI
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .config import get_settings
from .config import Settings
from .holstebro_managers import update_mo_managers  # type: ignore
from .init import get_organisation, get_facet_uuid, \
    get_manager_level_facet_and_classes

logger = structlog.get_logger()


def construct_context() -> dict[str, Any]:
    """Construct request context."""
    return {}


def construct_client(
    settings: Settings,
) -> PersistentGraphQLClient:
    """Construct clients froms settings.

    Args:
        settings: Integration settings module.

    Returns:
        PersistentGraphQLClient.
    """
    gql_client = PersistentGraphQLClient(
        url=settings.mo_url + "/graphql/v2",
        client_id=settings.client_id,
        client_secret=settings.client_secret.get_secret_value(),
        auth_server=settings.auth_server,
        auth_realm=settings.auth_realm,
        execute_timeout=settings.graphql_timeout,
        httpx_client_kwargs={"timeout": settings.graphql_timeout},
    )
    logger.info("Created graphql client")

    return gql_client


def create_app(*args: Any, **kwargs: Any) -> FastAPI:

    settings = get_settings(*args, **kwargs)
    app = FastAPI()

    context = construct_context()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        async with AsyncExitStack() as stack:

            gql_client = construct_client(settings)
            context["gql_client"] = await stack.enter_async_context(gql_client)
            context["root_uuid"] = settings.root_uuid

            print(await get_organisation(gql_client))
            print(await get_facet_uuid(gql_client, "manager_level"))
            print(await get_manager_level_facet_and_classes(
                gql_client,
                ["Niveau 1", "Niveau 2", "Niveau 3", "Niveau 4", "Niveau 5"]
            ))

            yield

    app.router.lifespan_context = lifespan

    @app.get("/")
    async def index() -> dict[str, str]:
        return {"Integration": "SD Managersync"}

    @app.post("/trigger/all", status_code=202)
    async def run_update() -> None:
        """Starts update process of managers"""
        gql_client = context["gql_client"]
        root_uuid = context["root_uuid"]
        await update_mo_managers(gql_client=gql_client, root_uuid=root_uuid)

    return app
