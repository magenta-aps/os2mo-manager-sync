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

            yield

    app.router.lifespan_context = lifespan

    @app.get("/")
    async def index() -> dict[str, str]:
        return {"Integration": "SD Managersync"}

    return app
