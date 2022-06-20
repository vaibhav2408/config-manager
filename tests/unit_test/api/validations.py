from starlette import status


class ExpectedResponse:
    status_code: int
    response: dict

    def __init__(self, status_code, response):
        self.status_code = status_code
        self.response = response


def get_expected_response(test_name):
    """
    Method to fetch the expected response instance
    Args:
        test_name: test for which response is to be fetched
    """
    if test_name not in expected_responses:
        return None
    return ExpectedResponse(**expected_responses.get(test_name))


expected_responses = {
    "get_all_configs": {
        "status_code": status.HTTP_200_OK,
        "response": [
            {
                "updated_at": 1655715652,
                "service_id": "abc",
                "created_at": 1655715315,
                "config_name": "emails",
                "config": {
                    "domains": "gmail.com, yahoo.com, hotmail.com",
                    "enabled": True,
                },
            },
            {
                "updated_at": 1655715284,
                "service_id": "abc",
                "created_at": 1655715284,
                "config_name": "message",
                "config": {
                    "config": {"domains": "gmail.com, yahoo.com", "enabled": True}
                },
            },
        ],
    },
    "get_configs": {
        "status_code": status.HTTP_200_OK,
        "response": {
            "updated_at": 1655715652,
            "service_id": "abc",
            "created_at": 1655715315,
            "config_name": "emails",
            "config": {"domains": "gmail.com, yahoo.com, hotmail.com", "enabled": True},
        },
    },
}
