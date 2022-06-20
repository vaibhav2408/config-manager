from __future__ import annotations

from pydantic import BaseModel


class ServiceConfigPayload(BaseModel):
    config: dict = {}


class ServiceConfigResponse(BaseModel):
    updated_at: int
    service_id: str
    created_at: int
    config_name: str
    config: dict
