# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from functools import cache
from typing import Any
from uuid import UUID

from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import Field
from pydantic import parse_obj_as
from pydantic import SecretStr

from .init import ManagerLevel


class Settings(BaseSettings):
    graphql_timeout: int = 120
    client_id: str = Field("SD-Managerscript", description="Client ID for OIDC client.")
    client_secret: SecretStr = Field(..., description="Client Secret for OIDC client.")
    mo_url: AnyHttpUrl = Field(
        parse_obj_as(AnyHttpUrl, "http://mo-service:5000"),
        description="Base URL for OS2mo.",
    )
    auth_server: AnyHttpUrl = Field(
        parse_obj_as(AnyHttpUrl, "http://keycloak-service:8080/auth"),
        description="Base URL for OIDC server (Keycloak).",
    )
    auth_realm: str = Field("mo", description="Realm to authenticate against")
    root_uuid: UUID = Field(description="UUID of the root org-unit")
    manager_type_uuid: UUID = Field(
        description="UUID defining manager type. Same for all managers"
    )
    responsibility_uuid: UUID = Field(
        description="UUID defining responsibility. Same for all managers"
    )
    # manager_level_mapping: list of dict used as Pydantic doesn't accept dict types
    manager_level_mapping: dict[str, str] = Field(
        description="Mapping dict from org-unit level to manager level"
    )
    manager_level_create: list[ManagerLevel]

    log_level: str = "INFO"


@cache
def get_settings(*args: Any, **kwargs: Any) -> Settings:
    """Fetch settings object.

    Args:
        args: overrides
        kwargs: overrides

    Return:
        Cached settings object.
    """
    return Settings(*args, **kwargs)
