from app.services.paypal_gateway.paypal_client import PayPalClient
from app.config.structlog import get_struct_logger
from app.tasks import create_order_task

logger = get_struct_logger(__name__)


class PaymentService:

    def __init__(self, paypal_client: PayPalClient):
        self.paypal_client = paypal_client

    def get_order(self, order_id: str) -> dict:
        """capture payment."""
        try:

            order = self.paypal_client.capture_order(order_id)

            return order

        except Exception as ex:
            logger.error(f"Error while processing payment: {ex}")
            raise

    def create_payment(self, data: dict) -> dict:
        """Create an order"""
        try:
            amount = data.get("amount")
            currency = data.get("currency")
            description = data.get("description")

            # Create the order
            order = self.paypal_client.create_order(amount, currency, description)

            return order

        except Exception as ex:
            logger.error(f"Error while processing payment: {ex}")
            raise

    def create_payout(self, data: dict) -> dict:
        """Cria um novo pagamento com base nos dados fornecidos."""
        try:
            amount = data.get("amount")
            currency = data.get("currency")
            description = data.get("description")
            recipient_email = data.get("recipient_email")

            payout_response = self.paypal_client.create_payout(
                recipient_email, amount, currency, description
            )

            return payout_response

        except Exception as ex:
            logger.error(f"Erro ao criar pagamento: {ex}")
            raise
