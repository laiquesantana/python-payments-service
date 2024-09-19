# Endpoint version: v1
API_VERSION = "v1"  # pylint: disable=C0413

from .payment_controller.paypal_controller import router as payments_router_v1

routes_v1 = [
    payments_router_v1,  # type: ignore
]
