from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK


class TestServiceHealth:
    def test_health_ep(self, client: TestClient):
        """
        Test to check the /healthz endpoint
        :param client:
        :return:
        """
        response = client.get(f"/healthz", allow_redirects=False,)

        assert response.status_code == HTTP_200_OK
