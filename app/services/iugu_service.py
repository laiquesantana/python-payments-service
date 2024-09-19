from app.services.iugu_gateway.iugu_gateway import IuguGateway
from app.config.structlog import get_struct_logger
from app.schema.schema import PaymentRequest

logger = get_struct_logger(__name__)


class IuguService:
    """Serviço para gerenciar pagamentos e clientes na Iugu."""

    def __init__(self, iugu_gateway: IuguGateway):
        self.iugu_gateway = iugu_gateway

    def create_payment(self, payment_request: PaymentRequest) -> dict:
        """
        Cria um pedido de pagamento na Iugu.

        Args:
            payment_request (PaymentRequest): Objeto contendo todos os dados necessários para criar o pagamento.

        Returns:
            dict: Resposta da Iugu com os detalhes do pagamento criado.
        """
        # Converter o modelo Pydantic em um dicionário
        charge_data = payment_request.dict(exclude_unset=True)

        # Log para depuração
        total_value = sum(
            item.price_cents * item.quantity for item in payment_request.items
        )
        logger.info(
            f"Criando pagamento para {payment_request.email} no valor total de {total_value} centavos."
        )

        # Chamar o gateway para enviar a requisição à Iugu
        return self.iugu_gateway.create_payment(charge_data)
