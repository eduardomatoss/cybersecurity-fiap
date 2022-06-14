from logging import getLogger

from fastapi import FastAPI
from dynaconf import settings
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.routers import root
from app.routers import health_check

logger = getLogger()

app = FastAPI(
    title=settings.get("application_name"),
    description=settings.get("application_description"),
    version="v1.0.0",
)

app.add_middleware(PrometheusMiddleware, app_name=settings.get("application_name"))
app.add_route("/metrics", handle_metrics)

app.include_router(root.router, include_in_schema=False)
app.include_router(health_check.router, include_in_schema=False)
