import boto3
import botocore
from structlog import get_logger  # type: ignore

from adobe_config_mgmt_lib.core.config import settings
from adobe_config_mgmt_lib.resources.constants import (  # attributes
    CONFIG_KEY,
    CONFIG_NAME_KEY,
    CREATED_AT_KEY,
    SERVICE_ID_KEY,
    UPDATED_AT_KEY,
)

# setting up the logger
logger = get_logger()

# Creating dynamodb resource
dynamodb = boto3.resource("dynamodb")


logger.info(
    "Created boto3 client.", region_name=settings.dynamodb_region,
)

# Syntax <cluster_name>-configs table.
SERVICES_CONFIG_TABLE = settings.dynamodb_table_prefix + "_" + "configs"


def create_services_config_table() -> bool:
    """
    Try to get table first, if failed, create it.
    Returns:
        True if table is created/present, False in case of any error
    """
    table = dynamodb.Table(SERVICES_CONFIG_TABLE)
    table_exist = True
    try:
        table.creation_date_time
    except Exception:
        logger.info(
            "Table does not exist. Creating table.", TableName=SERVICES_CONFIG_TABLE
        )
        table_exist = False
    if not table_exist:
        try:
            services_config_table = dynamodb.create_table(
                AttributeDefinitions=[
                    {"AttributeName": SERVICE_ID_KEY, "AttributeType": "S"},
                    {"AttributeName": CONFIG_NAME_KEY, "AttributeType": "S"},
                ],
                KeySchema=[
                    {"KeyType": "HASH", "AttributeName": SERVICE_ID_KEY},
                    {"KeyType": "RANGE", "AttributeName": CONFIG_NAME_KEY},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 100,
                    "WriteCapacityUnits": 100,
                },
                TableName=SERVICES_CONFIG_TABLE,
            )
            services_config_table.meta.client.get_waiter("table_exists").wait(
                TableName=SERVICES_CONFIG_TABLE
            )
            logger.info("Created dynamodb table.", TableName=SERVICES_CONFIG_TABLE)
            return True
        except (
            botocore.exceptions.EndpointConnectionError,
            botocore.exceptions.ConnectionError,
            botocore.exceptions.ReadTimeoutError,
        ) as error:
            logger.error("Could not connect to Dynamodb endpoint URL", error=error)
            return False
        except botocore.exceptions.ClientError as e:
            logger.error("Unexpected error", error=str(e))
            return False
    else:
        logger.info("Table already exists.", TableName=SERVICES_CONFIG_TABLE)
        return True


create_services_config_table()
