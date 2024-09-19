from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from app.config.env_adapter import EnvAdapter
from app.config.structlog import get_struct_logger

import uuid

logger = get_struct_logger(__name__)


class PayPalClient:
    """Classe para interagir com a API de Payouts do PayPal."""

    def __init__(self):
        """Configura o ambiente do PayPal para autenticação."""

        self.client_id = EnvAdapter.get_paypal_client_id()
        self.client_secret = EnvAdapter.get_paypal_client_secret()

        # Configura o ambiente de sandbox para teste (ou LiveEnvironment para produção)
        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret
        )
        self.client = PayPalHttpClient(self.environment)

    def create_order(self, amount, currency, description):
        """Create an order using PayPal Orders API."""
        request = OrdersCreateRequest()
        request.prefer("return=representation")
        request.request_body(
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency,
                            "value": amount,
                        },
                        "description": description,
                    }
                ],
            },
        )

        # Execute the order creation
        try:
            response = self.client.execute(request)
            logger.info(f"Order created successfully: {response.result}")
            return response.result
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise

    def capture_order(self, order_id: str):
        """Capture payment for an order."""
        request = OrdersCaptureRequest(order_id)

        # Execute the capture
        try:
            response = self.client.execute(request)
            logger.info(f"Payment captured successfully: {response.result}")
            return response.result
        except Exception as e:
            logger.error(f"Error capturing payment: {e}")
            raise

    def create_payout(
        self,
        recipient_email: str,
        amount: float,
        currency: str,
        note: str = "Payout via PayPal",
    ) -> dict:
        """Cria um payout usando a API oficial de Payouts do PayPal.

        Args:
        - recipient_email (str): Email do destinatário.
        - amount (float): Valor do pagamento.
        - currency (str): Moeda do pagamento (ex: 'USD').
        - note (str): Nota opcional para o pagamento.

        Returns:
        - dict: Resposta do PayPal com os detalhes do payout.
        """
        amount = float(amount)
        sender_batch_id = str(uuid.uuid4())

        # Prepara a requisição de payout
        request = PayoutsPostRequest()
        request.request_body(
            {
                "sender_batch_header": {
                    "sender_batch_id": "Payouts_"
                    + sender_batch_id,  # Um ID único por batch
                    "email_subject": "Você recebeu um pagamento",
                },
                "items": [
                    {
                        "recipient_type": "EMAIL",
                        "amount": {"value": f"{amount:.2f}", "currency": currency},
                        "note": note,
                        "receiver": recipient_email,
                        "sender_item_id": "item_1",
                    }
                ],
            }
        )

        # Tenta executar a requisição
        try:
            response = self.client.execute(request)
            if response.status_code not in [200, 201]:
                logger.error(
                    f"Erro na resposta do PayPal: {response.status_code} - {response.result}"
                )
                raise Exception(f"Erro na resposta do PayPal: {response.status_code}")
            logger.info(f"Payout criado com sucesso: {response.result}")
            return {
                "status": "success",
                "batch_id": response.result.batch_header.payout_batch_id,
                "links": response.result.links,
            }

        except Exception as e:
            logger.error(f"Erro ao criar Payout no PayPal: {e}")
            raise
