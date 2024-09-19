from app.services.vi_gateway.vi_gateway import VindiGateway
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


class VindiService:
    """Serviço para gerenciar pagamentos e clientes na Vindi."""

    def __init__(self, vindi_gateway: VindiGateway):
        self.vindi_gateway = vindi_gateway

    def create_customer(self, name: str, email: str, cpf_cnpj: str) -> dict:
        """Cria um cliente na Vindi."""
        customer_data = {
            "name": name,
            "email": email,
            "registry_code": cpf_cnpj,
        }
        logger.info(f"Criando cliente: {name}")
        return self.vindi_gateway.create_customer(customer_data)

    def create_payment(
        self, customer_id: int, amount: float, payment_method_code: str = "credit_card"
    ) -> dict:
        """Cria um pagamento na Vindi."""
        payment_data = {
            "customer_id": customer_id,
            "payment_method_code": payment_method_code,
            "amount": amount,
        }
        logger.info(f"Criando pagamento de {amount} BRL para o cliente {customer_id}")
        return self.vindi_gateway.create_payment(payment_data)
