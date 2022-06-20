from fastapi import FastAPI
from starlette.responses import JSONResponse
from structlog import get_logger

from adobe_config_mgmt_lib.apis.internal_apis import app as config_app
from adobe_config_mgmt_lib.core.config import settings

logger = get_logger(__name__)

complete_description = (
    " This Document outlines the API contracts"
)

app = FastAPI(title=settings.APP_NAME, description=complete_description)
app.include_router(config_app, prefix="/adobe/v1")

"""
Using FastAPI framework
Reasons:
- FastAPI is the best choice when speed and performance are of primary importance
- Inbuilt data validation
- Inbuilt Async I/O support
- Inbuilt Swagger UI GUI
- 
"""


@app.get("/healthz")
def healthz():
    """
    To check the readiness of the service
    :return:
    """
    return JSONResponse(status_code=200, content={"ready": True})
