import asyncio
from fastapi.encoders import jsonable_encoder
from structlog import get_logger

from adobe_config_mgmt_lib.core.config import settings
from adobe_config_mgmt_lib.core.cron.config_change_listener import start
from adobe_config_mgmt_lib.dal import dynamodb_dal_instance
from adobe_config_mgmt_lib.models.configs.service_config import ServiceConfigPayload
from adobe_config_mgmt_lib.resources.constants import (
    CONFIG_KEY,
    CONFIG_NAME_KEY,
    SERVICE_ID_KEY,
)

logger = get_logger()


def add_service_config(
    service_id: str, config_name: str, config_data: ServiceConfigPayload
):
    """
    Method to add the configs of the given service
    :param service_id:
    :param config_name:
    :param config_data:
    :return:
    """
    payload_json = jsonable_encoder(config_data)
    res = dynamodb_dal_instance.add_configs(
        data={
            SERVICE_ID_KEY: service_id,
            CONFIG_NAME_KEY: config_name,
            CONFIG_KEY: payload_json,
        },
        execution_context=None,
    )
    if res:
        logger.info(
            "Added the configs successfully",
            service_id=service_id,
            config_name=config_name,
        )
    else:
        logger.info(
            "Failed to add the configs",
            service_id=service_id,
            config_name=config_name,
            status=res,
        )
    return res


def get_all_service_config(service_id: str):
    """
    Method to get all the configs for a given service
    :param service_id:
    :return:
    """
    # if not settings.is_cron_running:
    #     logger.info("Starting the cron to check for any updates in the service config.")
    #     asyncio.create_task(start(service_id=service_id))
    #     settings.is_cron_running = True

    return dynamodb_dal_instance.get_configs(
        data={SERVICE_ID_KEY: service_id}, execution_context=None
    )


def get_service_config_by_name(service_id: str, config_name: str):
    """
    Method to get the specific configs for a given service
    :param service_id:
    :param config_name:
    :return:
    """
    # if not settings.is_cron_running:
    #     logger.info("Starting the cron to check for any updates in the service config.")
    #     asyncio.create_task(start(service_id=service_id))
    #     settings.is_cron_running = True

    return dynamodb_dal_instance.get_configs(
        data={SERVICE_ID_KEY: service_id, CONFIG_NAME_KEY: config_name},
        execution_context=None,
    )


def update_service_config(service_id: str, config_name: str, config: dict):
    """

    :param service_id:
    :param config_name:
    :param config:
    :return:
    """
    return dynamodb_dal_instance.update_configs(
        data={"service_id": service_id, "config_name": config_name, "config": config},
        execution_context=None,
    )
