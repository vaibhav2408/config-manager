import json
import logging
import os
import sys

from pydantic.error_wrappers import ValidationError
from starlette.config import Config
from structlog import get_logger  # type: ignore

# Need to set log stream in addition to main since this executed before main.
# configure logging with filename, function name and line numbers

"""
Setting the date format for log message
"""
date_str = "%I:%M:%S %p %Z"

"""
Setting up the format of the log message.
"""
fmt_str = "%(asctime)s: %(levelname)s: [%(threadName)-2.12s - %(filename)s:%(funcName)s::%(lineno)s]- %(message)s"

logging.basicConfig(
    level=logging.INFO, datefmt=date_str, format=fmt_str, stream=sys.stdout,
)

logger = get_logger()

CLOUD_INFRA_BLOBS = ["dynamodb"]

# Config will be read from environment variables and/or ".env" files.
config = Config(".env")

CONFIG_PATH = config("CONFIGMAP_MOUNT_PATH", cast=str, default="/var/data")


class Settings:
    DB_INIT_SUCCESS: bool = True
    APP_NAME = "config-management"

    def __init__(self):
        self.config = {}
        self.is_cron_running = False

    def load_config(self) -> None:
        def set_from_file(f_path: str, blob_name: str):
            if os.path.isfile(f_path):
                logger.info(
                    f"Setting configuration from file {f_path} for configuration {blob_name}"
                )
                with open(f_path) as file:
                    print(f"*********************** CONFIG *********** \n {file}")
                    configs = json.load(file)
                    setattr(self, blob_name, configs.get(blob_name))
            else:
                if blob_name == "msk":
                    setattr(self, "kafka", {})
                setattr(self, blob_name, {})

        for infra_blob in CLOUD_INFRA_BLOBS:
            file_path = f"{CONFIG_PATH}/infra_{infra_blob}.json"
            set_from_file(f_path=file_path, blob_name=infra_blob)

    @property
    def dynamodb_url(self):
        host = self.dynamodb.get("host", "localstack")  # type: ignore
        if "localstack" in host:
            port = self.dynamodb.get("port", 4569)
            return f"http://{host}:{port}"
        else:
            return f"https://{host}"

    @property
    def dynamodb_user(self):
        return self.dynamodb.get("username", "")

    @property
    def dynamodb_password(self):
        return self.dynamodb.get("password", "")

    @property
    def dynamodb_table_prefix(self):
        return self.dynamodb.get("table_prefix", "services")

    @property
    def dynamodb_region(self):
        return self.dynamodb.get("region", "us-west-2")

    @property
    def dynamodb_init_complete(self):
        return self.DB_INIT_SUCCESS

    @property
    def log_level(self):
        levels = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
        }
        log_level = levels.get(os.environ.get("LOG_LEVEL", "").upper(), logging.INFO)
        return log_level


try:
    settings = Settings()
    settings.load_config()
except ValidationError as e:
    logger.exception(e)
    sys.exit(1)
