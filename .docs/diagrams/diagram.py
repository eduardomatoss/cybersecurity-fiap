from diagrams import Diagram

from diagrams.onprem.monitoring import Prometheus
from diagrams.programming.framework import FastAPI
from diagrams.aws.database import RDS
from diagrams.onprem.client import Client

with Diagram(
    "Architecture",
    ".docs/diagrams/architecture",
    direction="LR",
    show=False,
    graph_attr={
        "pad": "0.5",
    },
):

    frontend = Client("Frontend")
    api = FastAPI("API")
    rds = RDS("Database")
    metrics = Prometheus("Metrics")

    frontend >> api >> rds
    api >> metrics
