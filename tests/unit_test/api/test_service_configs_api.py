import uuid

from fastapi.testclient import TestClient
from mock import patch
from structlog import get_logger

from tests.unit_test.api.validations import get_expected_response

logger = get_logger()

url_prefix = "/adobe/v1"


@patch(
    "adobe_config_mgmt_lib.core.service_config.service_config_mgmt.add_service_config",
    return_value=True,
)
@patch(
    "adobe_config_mgmt_lib.dal.dynamodb.dynamodb_dal.DynamodbDAL._add_service_config",
    return_value=201,
)
@patch(
    "adobe_config_mgmt_lib.dal.dynamodb.dynamodb_dal.DynamodbDAL.add_configs",
    return_value=True,
)
def test_add_service_configs(
    mock_add_service_config,
    mock__add_service_config,
    mock_add_configs,
    client: TestClient,
):
    service_id = str(uuid.uuid4())
    config_name = "emails"
    api_endpoint = f"{url_prefix}/{service_id}/configs/{config_name}"

    response = client.post(api_endpoint, allow_redirects=True, json={"config": {}})

    expected_response = {"status": True}

    assert response.status_code == 201
    assert response.json() == expected_response


@patch(
    "adobe_config_mgmt_lib.core.service_config.service_config_mgmt.get_service_config_by_name",
    return_value=get_expected_response("get_all_configs").response,
)
@patch(
    "adobe_config_mgmt_lib.dal.dynamodb.dynamodb_dal.DynamodbDAL.get_configs",
    return_value=get_expected_response("get_all_configs").response,
)
@patch(
    "adobe_config_mgmt_lib.dal.dynamodb.dynamodb_dal.DynamodbDAL._get_all_service_config",
    return_value=get_expected_response("get_all_configs").response,
)
def test_get_service_configs_all(
    mock_get_service_config_by_name,
    mock_get_configs,
    mock__get_all_service_config,
    client: TestClient,
):
    service_id = str(uuid.uuid4())
    api_endpoint = f"{url_prefix}/{service_id}/configs"

    response = client.get(api_endpoint, allow_redirects=True)

    assert response.status_code == get_expected_response("get_all_configs").status_code
    assert response.json() == get_expected_response("get_all_configs").response


@patch(
    "adobe_config_mgmt_lib.core.service_config.service_config_mgmt.get_service_config_by_name",
    return_value=[get_expected_response("get_configs").response],
)
@patch(
    "adobe_config_mgmt_lib.dal.dynamodb.dynamodb_dal.DynamodbDAL.get_configs",
    return_value=[get_expected_response("get_configs").response],
)
@patch(
    "adobe_config_mgmt_lib.dal.dynamodb.dynamodb_dal.DynamodbDAL._get_service_config",
    return_value=[get_expected_response("get_configs").response],
)
def test_get_service_config(
    mock_get_service_config_by_name,
    mock_get_configs,
    mock__get_service_config,
    client: TestClient,
):
    service_id = str(uuid.uuid4())
    config_name = "emails"
    api_endpoint = f"{url_prefix}/{service_id}/configs/{config_name}"

    response = client.get(api_endpoint, allow_redirects=True)

    assert response.status_code == get_expected_response("get_configs").status_code
    assert response.json() == get_expected_response("get_configs").response
