import requests
from app.config.env_adapter import EnvAdapter
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


class VindiGateway:
    """Gateway para interagir com a API da Vindi."""

    def __init__(self):
        self.base_url = "https://app.vindi.com.br/api/v1"
        self.api_key = (
            EnvAdapter.get_vindi_api_key()
        )  # Certifique-se de que a chave esteja no .env

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.api_key}",
        }

    def create_customer(self, customer_data: dict):
        """Cria um cliente na Vindi."""
        url = f"{self.base_url}/customers"
        logger.info(f"Enviando requisição para criar cliente na Vindi.")
        response = requests.post(url, json=customer_data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def create_payment(self, payment_data: dict):
        """Cria uma cobrança na Vindi."""
        url = f"{self.base_url}/charges"
        logger.info(f"Enviando requisição para criar pagamento na Vindi.")
        response = requests.post(url, json=payment_data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
