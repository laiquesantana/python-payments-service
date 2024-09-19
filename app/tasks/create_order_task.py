from celery import shared_task
from paypalpayoutssdk.payouts import PayoutsPostRequest
from app.services.paypal_gateway.paypal_client import PayPalClient

import uuid


def __init__(self, paypal_client: PayPalClient):
    self.paypal_client = paypal_client


@shared_task
def create_payout_task(
    self, recipient_email, amount, currency, note="Payout via PayPal"
):
    """Task Celery para gerar payout usando o PayPal."""
    try:
        amount = float(amount)
        sender_batch_id = str(uuid.uuid4())

        request = PayoutsPostRequest()
        request.request_body(
            {
                "sender_batch_header": {
                    "sender_batch_id": "Payouts_" + sender_batch_id,
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

        response = self.paypal_client.create_payout(request)

        # Verifica a resposta e loga
        if response.status_code in [200, 201]:
            return {
                "status": "success",
                "batch_id": response.result.batch_header.payout_batch_id,
                "links": response.result.links,
            }
        else:
            raise RuntimeError(f"Erro na resposta do PayPal: {response.status_code}")

    except Exception as e:
        raise RuntimeError(f"Erro ao criar Payout no PayPal: {e}") from e
