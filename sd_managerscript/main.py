# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextlib import AsyncExitStack
from typing import Any
from uuid import UUID

import structlog
from fastapi import FastAPI
from raclients.graph.client import PersistentGraphQLClient  # type: ignore

from .config import get_settings
from .config import Settings
from .holstebro_managers import update_mo_managers  # type: ignore
from .init import create_missing_manager_levels
from .log import setup_logging

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

    setup_logging(settings.log_level)
    context = construct_context()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        async with AsyncExitStack() as stack:

            gql_client = construct_client(settings)
            context["gql_client"] = await stack.enter_async_context(gql_client)
            context["root_uuid"] = settings.root_uuid

            await create_missing_manager_levels(
                gql_client, settings.manager_level_create
            )

            yield

    app.router.lifespan_context = lifespan

    @app.get("/")
    async def index() -> dict[str, str]:
        return {"Integration": "SD Managersync"}

    @app.post("/trigger/{ou_uuid}")
    async def update_single_org_unit(ou_uuid: UUID, dry_run: bool = False) -> None:
        logger.info("Updating org unit", uuid=ou_uuid)
        gql_client = context["gql_client"]
        root_uuid = context["root_uuid"]
        await update_mo_managers(
            gql_client=gql_client,
            org_unit_uuid=ou_uuid,
            root_uuid=root_uuid,
            recursive=False,
        )

    @app.post("/trigger/all", status_code=202)
    async def run_update() -> None:
        """Starts update process of managers"""
        gql_client = context["gql_client"]
        root_uuid = context["root_uuid"]
        await update_mo_managers(
            gql_client=gql_client, org_unit_uuid=root_uuid, root_uuid=root_uuid
        )

    return app
