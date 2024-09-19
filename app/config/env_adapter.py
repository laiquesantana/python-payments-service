import os


class EnvAdapter:
    @staticmethod
    def get_paypal_client_id() -> str:
        return os.getenv("PAYPAL_CLIENT_ID")

    @staticmethod
    def get_paypal_client_secret() -> str:
        return os.getenv("PAYPAL_CLIENT_SECRET")

    @staticmethod
    def get_paypal_api_url() -> str:
        return os.getenv("PAYPAL_API_URL")

    @staticmethod
    def get_iugu_api_token():
        return os.getenv("IUGU_API_TOKEN")

    @staticmethod
    def get_vindi_api_token():
        return os.getenv("VINDI_API_TOKEN")
