from structlog import get_logger

from adobe_config_mgmt_lib.core.config import settings

# Setting up logger
from adobe_config_mgmt_lib.dal.dynamodb.dynamodb_dal import DynamodbDAL

logger = get_logger(__name__)

try:
    logger.info("DynamoDB table init started.", status="In-progress")
    dynamodb_dal_instance = DynamodbDAL()
    logger.info("DynamoDB table init.", status=True)
except Exception as e:
    logger.exception(str(e))
