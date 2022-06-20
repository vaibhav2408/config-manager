from typing import List, Union

from fastapi import APIRouter, Body, Path, status
from starlette.responses import JSONResponse, Response
from structlog import get_logger

from adobe_config_mgmt_lib.core.service_config import service_config_mgmt
from adobe_config_mgmt_lib.models.configs.service_config import (
    ServiceConfigPayload,
    ServiceConfigResponse,
)
from adobe_config_mgmt_lib.models.generic.empty_response import EmptyResponse

app = APIRouter()

logger = get_logger(__name__)


"""
NOTE:

These API are valid only if we're going to run this service as 
a separate microservice. 
If this will only be imported as a library, we can skip the APIs
"""


@app.post(
    "/{service_id}/configs/{config_name}",
    status_code=status.HTTP_200_OK,
    summary="Add a config for the given service",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": EmptyResponse},
        status.HTTP_403_FORBIDDEN: {"model": EmptyResponse},
    },
)
# @auth_check
def add_service_configs(
    response: Response,
    service_id: str = Path(
        ...,
        title="Service ID",
        description="The unique ID associated with the service",
    ),
    config_name: str = Path(
        title="The config name",
        description="The specific config name of the given service",
    ),
    config: ServiceConfigPayload = Body(..., title="The config payload"),
):
    result = service_config_mgmt.add_service_config(
        service_id=service_id, config_name=config_name, config_data=config
    )
    if not result:
        logger.info(
            "Could not create the config for the service.",
            service_id=service_id,
            config_name=config_name,
        )
        response.status_code = 400
        return EmptyResponse()
    return JSONResponse(status_code=201, content={"status": True})


@app.get(
    "/{service_id}/configs",
    status_code=status.HTTP_200_OK,
    summary="Get all the configs of the service",
    response_model=Union[List[ServiceConfigResponse], EmptyResponse],
    responses={
        status.HTTP_200_OK: {
            "model": Union[List[ServiceConfigResponse], EmptyResponse]
        },
        status.HTTP_404_NOT_FOUND: {"model": EmptyResponse},
        status.HTTP_403_FORBIDDEN: {"model": EmptyResponse},
    },
)
# @auth_check
async def get_service_config_all(
    response: Response,
    service_id: str = Path(
        ...,
        title="Service ID",
        description="The unique ID associated with the service",
    ),
):
    result = service_config_mgmt.get_all_service_config(service_id=service_id)
    if not result:
        logger.info(
            "No config entries found for the given service.", service_id=service_id,
        )
        response.status_code = 404
        return EmptyResponse()
    return result


@app.get(
    "/{service_id}/configs/{config_name}",
    status_code=status.HTTP_200_OK,
    summary="Fetch the specific config for the given service",
    response_model=Union[ServiceConfigResponse, EmptyResponse],
    responses={
        status.HTTP_200_OK: {"model": ServiceConfigResponse},
        status.HTTP_404_NOT_FOUND: {"model": EmptyResponse},
        status.HTTP_403_FORBIDDEN: {"model": EmptyResponse},
    },
)
# @auth_check
def get_service_config(
    response: Response,
    service_id: str = Path(
        ...,
        title="Service ID",
        description="The unique ID associated with the service",
    ),
    config_name: str = Path(
        title="The config name",
        description="The specific config name of the given service",
    ),
):
    result = service_config_mgmt.get_service_config_by_name(
        service_id=service_id, config_name=config_name
    )
    if not result:
        logger.info(
            "No config entries found for the given service.",
            service_id=service_id,
            config_name=config_name,
        )
        response.status_code = 404
        return EmptyResponse()
    return result[0]


@app.put(
    "/{service_id}/configs/{config_name}",
    status_code=status.HTTP_200_OK,
    summary="Update config for the given service",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": EmptyResponse},
        status.HTTP_403_FORBIDDEN: {"model": EmptyResponse},
    },
)
# @auth_check
def update_service_configs(
    response: Response,
    service_id: str = Path(
        ...,
        title="Service ID",
        description="The unique ID associated with the service",
    ),
    config_name: str = Path(
        title="The config name",
        description="The specific config name of the given service",
    ),
    config: ServiceConfigPayload = Body(..., title="The config payload"),
):
    result = service_config_mgmt.update_service_config(
        service_id=service_id, config_name=config_name, config=config.config
    )
    if not result:
        logger.info(
            "Could not create the config for the service.",
            service_id=service_id,
            config_name=config_name,
        )
        response.status_code = 400
        return EmptyResponse()
    return JSONResponse(status_code=201, content={"status": True})
