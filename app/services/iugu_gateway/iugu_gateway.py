import requests
from app.config.env_adapter import EnvAdapter
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


class IuguGateway:
    """Gateway para interagir com a API da Iugu."""

    def __init__(self):
        self.base_url = "https://api.iugu.com/v1"
        self.api_token = EnvAdapter.get_iugu_api_token()

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.api_token}",
        }

    def create_charge(self, charge_data: dict):
        """Cria um pedido de pagamento (charge) na Iugu."""
        url = f"{self.base_url}/charge"
        logger.info("Enviando requisição para criar pagamento na Iugu.")
        response = requests.post(
            url, json=charge_data, headers=self._get_headers(), timeout=10
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"Erro na criação de pagamento na Iugu: {e}, Resposta: {response.text}"
            )
            raise
        return response.json()
