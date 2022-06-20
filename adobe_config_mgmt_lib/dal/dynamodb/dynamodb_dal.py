import time

from botocore.exceptions import ClientError, NoCredentialsError
from structlog import get_logger  # type: ignore

from adobe_config_mgmt_lib.core.config import settings
from adobe_config_mgmt_lib.dal.abstract_db_handler import AbstractDBHandler
from adobe_config_mgmt_lib.dal.dynamodb import SERVICES_CONFIG_TABLE, dynamodb
from adobe_config_mgmt_lib.resources.constants import (  # Services-configs keys
    CONFIG_KEY,
    CONFIG_NAME_KEY,
    CREATED_AT_KEY,
    SERVICE_ID_KEY,
    UPDATED_AT_KEY,
)

"""
Data access layer for the services_configs dynamodb table.

This module contains basic Write/Read operations.
It has functions to add a new config and 
fetch config based on service ID & config type 

"""

logger = get_logger()

INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error."
DYNAMODB_CLIENT_NOT_INITIALIZED_MESSAGE = "Dynamodb client is not initialized."


class DynamodbDAL(AbstractDBHandler):
    # dynamodb internal keys
    DYNAMO_DB_ITEMS_KEY = "Items"
    DYNAMO_DB_RESPONSE_META_KEY = "ResponseMetadata"
    DYNAMO_DB_HTTP_STATUS_CODE_KEY = "HTTPStatusCode"

    def __init__(self):
        self.table = dynamodb.Table(SERVICES_CONFIG_TABLE)

    def add_configs(self, data: dict, execution_context: dict):
        """
         Method to add configs into the services_config dynamodb table.

        Args:
            data: contains all the required fields/attributes for inserting
            execution_context: any additional info needed for completing the operation.
        Returns:
            The status True if 200 response, otherwise False
        """
        service_id = data.get(SERVICE_ID_KEY)
        config_name = data.get(CONFIG_NAME_KEY)
        config = data.get(CONFIG_KEY)
        response = self._add_service_config(service_id, config_name, config)
        logger.info(f"dynamo db add config completed. response code: {response}")
        return response == 200

    def get_configs(self, data: dict, execution_context: dict):
        """
         Method to fetch the specified config from the table.

        Args:
            data: contains all the required fields for inserting
            execution_context: any additional info needed for completing the operation.

        Returns:
            The status code obtained from the operation
        """
        if SERVICE_ID_KEY not in data and CONFIG_NAME_KEY not in data:
            logger.error(
                f"Mandatory query fields are missing. Mandatory fields are: {SERVICE_ID_KEY}, {CONFIG_NAME_KEY}"
            )
            return None
        if SERVICE_ID_KEY in data and CONFIG_NAME_KEY not in data:
            return self._get_all_service_config(data[SERVICE_ID_KEY])
        return self._get_service_config(data[SERVICE_ID_KEY], data[CONFIG_NAME_KEY])

    def _add_service_config(
        self, service_id: str, config_name: str, config: str,
    ):
        """
        Create a event and post to config table.

        Args:
            service_id: Application/Service id.
            config_name: Name of the config
            config: The config
        Returns:
            The status code obtained from the operation
                200: Success else failure
        """
        try:
            if settings.dynamodb_init_complete:
                logger.info(
                    "Inserting entry into the dynamodb",
                    service_id=service_id,
                    config_name=config_name,
                    dynmodb_status=settings.dynamodb_init_complete,
                    table=SERVICES_CONFIG_TABLE,
                )
                created_at = int(time.time())
                updated_at = int(time.time())
                response = self.table.put_item(
                    Item={
                        SERVICE_ID_KEY: service_id,
                        CREATED_AT_KEY: str(created_at),
                        UPDATED_AT_KEY: str(updated_at),
                        CONFIG_KEY: config,
                        CONFIG_NAME_KEY: config_name,
                    }
                )
                result = response[self.DYNAMO_DB_RESPONSE_META_KEY][
                    self.DYNAMO_DB_HTTP_STATUS_CODE_KEY
                ]
                logger.info("Done writing data to dynamodb", result=result)
                return result
            else:
                logger.exception(
                    DYNAMODB_CLIENT_NOT_INITIALIZED_MESSAGE,
                    dynmodb_status=settings.dynamodb_init_complete,
                )
                raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)
        except (ClientError, NoCredentialsError) as ce:
            logger.exception(
                f"Error while inserting entry into the dynamodb for the "
                f"service: {service_id}, config-type: {config_name}",
                error=str(ce),
            )
            raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)
        except Exception as ex:
            logger.exception(
                f"Exception occurred while inserting entry into the dynamodb for the "
                f"service: {service_id}, config-type: {config_name}",
                error=str(ex),
            )
            raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)

    def _get_service_config(self, service_id: str, config_name: int):
        """
        Gets all the entries from dynamodb
        Args:
            service_id: The ID of the service.
            config_name: The name of the config
        Returns:
            All the entries matching the search criteria
        """
        try:
            if settings.dynamodb_init_complete:
                logger.info(
                    "Reading entry from the dynamodb",
                    dynmodb_status=settings.dynamodb_init_complete,
                    table=SERVICES_CONFIG_TABLE,
                )
                response = self.table.query(
                    ConsistentRead=True,  # Takes care of consistency in Dynamodb
                    TableName=SERVICES_CONFIG_TABLE,
                    KeyConditionExpression="service_id = :service_id AND config_name = :config_name",
                    ExpressionAttributeValues={
                        ":service_id": service_id,
                        ":config_name": config_name,
                    },
                )
                return response[self.DYNAMO_DB_ITEMS_KEY]
            else:
                logger.error(
                    DYNAMODB_CLIENT_NOT_INITIALIZED_MESSAGE,
                    dynmodb_status=settings.dynamodb_init_complete,
                )
                raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)
        except (ClientError, NoCredentialsError) as nce:
            logger.exception(
                f"Error while reading entry from the configs from dynamodb for "
                f"service: {service_id}, config: {config_name}",
                error=str(nce),
            )
            raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)

    def _get_all_service_config(self, service_id: str):
        """
        Gets all the entries from dynamodb
        Args:
            service_id: The ID of the service.
        Returns:
            All the entries matching the search criteria
        """
        try:
            if settings.dynamodb_init_complete:
                logger.info(
                    "Reading entry from the dynamodb",
                    dynmodb_status=settings.dynamodb_init_complete,
                    table=SERVICES_CONFIG_TABLE,
                )
                response = self.table.query(
                    ConsistentRead=True,  # Takes care of consistency in Dynamodb
                    TableName=SERVICES_CONFIG_TABLE,
                    KeyConditionExpression="service_id = :service_id",
                    ExpressionAttributeValues={":service_id": service_id},
                )
                return response[self.DYNAMO_DB_ITEMS_KEY]
            else:
                logger.error(
                    DYNAMODB_CLIENT_NOT_INITIALIZED_MESSAGE,
                    dynmodb_status=settings.dynamodb_init_complete,
                )
                raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)
        except (ClientError, NoCredentialsError) as nce:
            logger.exception(
                f"Error while reading entry from the configs from dynamodb for service: {service_id}",
                error=str(nce),
            )
            raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)

    def update_configs(self, data: dict, execution_context: dict):
        """
        :param data:
        :param execution_context:
        :return:
        """
        service_id = (data[SERVICE_ID_KEY],)
        config_name = data[CONFIG_NAME_KEY]
        try:
            if settings.dynamodb_init_complete:
                logger.info(
                    "Updating config for service: {service_id}, config: {config_name}",
                    status="in-progress",
                )

                response = self.get_configs(
                    data=data, execution_context=execution_context
                )
                item = response[0]

                item[CONFIG_KEY] = data["config"]
                item[UPDATED_AT_KEY] = str(int(time.time()))
                self.table.put_item(Item=item)
                logger.info(
                    f"Done updating the config for service: {service_id}, config: {config_name}",
                    result=True,
                )
                return True
            else:
                logger.exception(
                    DYNAMODB_CLIENT_NOT_INITIALIZED_MESSAGE,
                    dynmodb_status=settings.dynamodb_init_complete,
                )
                raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)

        except (ClientError, NoCredentialsError) as ce:
            logger.exception(
                f"Error while updating config entry in dynamodb for the "
                f"service: {service_id}, config-type: {config_name}",
                error=str(ce),
            )
            raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)
        except Exception as ex:
            logger.exception(
                f"Exception occurred while updating entry in dynamodb for the "
                f"service: {service_id}, config-type: {config_name}",
                error=str(ex),
            )
            raise RuntimeError(500, INTERNAL_SERVER_ERROR_MESSAGE)

    def delete_configs(self, data: dict, execution_context: dict):
        """
        TODO implement this logic if needed
        """
        pass
