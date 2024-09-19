from celery import shared_task
from paypalpayoutssdk.payouts import PayoutsPostRequest
from app.services.paypal_gateway.paypal_client import PayPalClient
import uuid
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


def __init__(self, paypal_client: PayPalClient):
    self.paypal_client = paypal_client


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def create_payout_task(
    self,
    recipient_email: str,
    amount: float,
    currency: str,
    note: str = "Payout via PayPal",
):
    """
    Celery task for generating a payout using PayPal.

    Args:
    - recipient_email (str): The email of the payout recipient.
    - amount (float): The amount to be paid.
    - currency (str): The currency of the payout.
    - note (str, optional): A note to include with the payout. Default is 'Payout via PayPal'.

    Returns:
    - dict: The result of the payout request.

    Raises:
    - RuntimeError: If the payout fails after retries.
    """
    try:
        # Ensure the amount is a valid float
        amount = float(amount)
        sender_batch_id = str(uuid.uuid4())

        # Build the payout request
        request = PayoutsPostRequest()
        request.request_body(
            {
                "sender_batch_header": {
                    "sender_batch_id": f"Payouts_{sender_batch_id}",
                    "email_subject": "You have received a payment",
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

        # Send the payout request
        response = self.paypal_client.create_payout(request)

        # Check response and return the result if successful
        if response.status_code in [200, 201]:
            logger.info(f"Payout successfully created for {recipient_email}")
            return {
                "status": "success",
                "batch_id": response.result.batch_header.payout_batch_id,
                "links": response.result.links,
            }
        else:
            logger.error(f"Failed to create payout: {response.status_code}")
            raise RuntimeError(f"PayPal error: {response.status_code}")

    except Exception as e:
        logger.error(f"Error creating payout for {recipient_email}: {e}")
        raise self.retry(exc=e)  # Retry the task if it fails
