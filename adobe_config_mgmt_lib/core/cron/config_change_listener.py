import asyncio
from typing import List

from structlog import get_logger

from adobe_config_mgmt_lib.models.configs.service_config import ServiceConfigResponse

logger = get_logger(__name__)

prev_configs = None


def _is_config_changed(config1, config2):
    for config in config1:
        match = False
        for prev_config in config2:
            if config['updated_at'] == prev_config['updated_at']:
                match = True
        if not match:
            return True
    return False


def check_for_config_change(service_id: str):
    from adobe_config_mgmt_lib.core.service_config.service_config_mgmt import get_all_service_config
    global prev_configs
    curr_configs: List[ServiceConfigResponse] = get_all_service_config(service_id=service_id)
    config_change_res = _is_config_changed(config1=prev_configs, config2=curr_configs)
    prev_configs = curr_configs
    return config_change_res


def config_change_listener(service_id: str, config_file_destination: str, interval: int = 5):
    from adobe_config_mgmt_lib.core.service_config.service_config_mgmt import get_all_service_config
    global prev_configs
    if prev_configs is None:
        prev_configs = get_all_service_config(service_id=service_id)
    res = check_for_config_change(service_id=service_id)
    if res:
        logger.info("Config changed")
    else:
        logger.info("No changes to the config")


async def start(service_id="abc", config_file_destination="/var/data/test/"):
    """
    A background task which keeps checking
    for newly published youtube videos after a
    given interval of time
    """
    while True:
        config_change_listener(service_id, config_file_destination)
        await asyncio.sleep(20)
