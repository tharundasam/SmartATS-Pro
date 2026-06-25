from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    app_name: str
    environment: str
    database: str  # "connected" | "unreachable"


class RootResponse(BaseModel):
    message: str
    docs_url: str
    api_version: str
