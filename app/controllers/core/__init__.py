from .health_controller import router as health_router_core
from .swagger_controller import router as swagger_router_core

core_routes = [
    health_router_core,  # type: ignore
    swagger_router_core,  # type: ignore
]
