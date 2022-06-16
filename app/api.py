from logging import getLogger

from fastapi import FastAPI
from dynaconf import settings
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.routers import root
from app.routers import health_check
from app.routers import delivery
from app.routers import product
from app.routers import buyer
from app.routers import deliveryman


logger = getLogger()

app = FastAPI(
    title=settings.get("application_name"),
    description=settings.get("application_description"),
    version="v1.0.0",
)

app_v1 = FastAPI(
    title=settings.get("application_name"),
    description=settings.get("application_description"),
    version="v1.0.0",
)

app.mount("/v1", app_v1)

app.add_middleware(PrometheusMiddleware, app_name=settings.get("application_name"))
app.add_route("/metrics", handle_metrics)
app.include_router(root.router)
app.include_router(health_check.router)


app_v1.include_router(root.router, include_in_schema=False)
app_v1.include_router(health_check.router, include_in_schema=False)
app_v1.include_router(delivery.router, prefix="/delivery", tags=["delivery"])
app_v1.include_router(product.router, prefix="/product", tags=["product"])
app_v1.include_router(buyer.router, prefix="/buyer", tags=["buyer"])
app_v1.include_router(deliveryman.router, prefix="/deliveryman", tags=["deliveryman"])
