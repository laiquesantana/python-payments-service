from fastapi import APIRouter, HTTPException, Request, status, Body
from sqlalchemy.exc import IntegrityError
from app.services import PaymentService
from app.config.structlog import get_struct_logger
from app.services.paypal_gateway.paypal_client import PayPalClient

logger = get_struct_logger(__name__)

router = APIRouter(
    prefix="/v1/payments",
    tags=["Payments"],
    responses={
        404: {
            "description": "Not found. See documentation for more details",
        },
    },
)

payment_service = PaymentService(PayPalClient())


@router.get("/order/{order_id}")
async def get_payment(order_id: str):
    """
    Endpoint to create a new payment.
    """
    try:
        order_data = payment_service.get_order(order_id)

        return {
            "status": "success",
            "message": "Payment captured successfully.",
            "order_id": order_data.id,
            "payer_info": {
                "payer_id": order_data.payer.payer_id,
                "name": {
                    "given_name": order_data.payer.name.given_name,
                    "surname": order_data.payer.name.surname,
                },
                "email_address": order_data.payer.email_address,
                "address": {"country_code": order_data.payer.address.country_code},
            },
            "purchase_units": [
                {
                    "reference_id": unit.reference_id,
                }
                for unit in order_data.purchase_units
            ],
            "links": [
                {"rel": link.rel, "href": link.href, "method": link.method}
                for link in order_data.links
            ],
        }
    except Exception as ex:
        logger.critical("Error while processing payment", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing payment.",
        ) from ex


@router.post("/")
async def create_payment(
    amount: str = Body(title="Amount", description="The amount to be paid."),
    currency: str = Body(title="Currency", description="The currency of the payment."),
    description: str = Body(
        title="Description", description="The description of the payment."
    ),
):
    """
    Endpoint to create a new payment.
    """
    try:
        body = dict(amount=amount, currency=currency, description=description)
        order_data = payment_service.create_payment(body)

        # Log success with detailed information
        logger.info(f"Payment created successfully. Amount: {amount} {currency}")

        return {
            "status": "success",
            "message": "Payment created successfully.",
            "order_id": order_data.id,
            "capture_details": [
                link.href for link in order_data.links
            ],  # Lista as URLs de captura
            "approval_url": next(
                link.href for link in order_data.links if link.rel == "approve"
            ),  # URL de aprovação
        }

    except Exception as ex:
        logger.critical("Error while processing payment", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing payment.",
        ) from ex


@router.post("/payouts")
async def create_payout(
    amount: str = Body(
        title="Amount",
        description="The amount to be paid.",
    ),
    currency: str = Body(
        title="currency",
        description="The currency of the payment.",
    ),
    description: str = Body(
        title="description",
        description="The description of the payment.",
    ),
    recipient_email: str = Body(
        title="recipient_email",
        description="The email of the recipient.",
    ),
):
    """
    Endpoint to create a new payment.

    Args:
    -    amount (str): The amount to be paid.
    -    currency (str): The currency of the payment.
    -    description (str): The description of the payment.
    -    recipient_email (str): The email of the payment recipient.

    Returns:
    -    `JSON`: Payment status and relevant details.

    Raises:
    -    `HTTPException`: If there is an integrity error (status code 422) or any other internal server error (status code 500).
    """
    try:
        body = dict(
            amount=amount,
            currency=currency,
            description=description,
            recipient_email=recipient_email,
        )
        payment = payment_service.create_payout(body)

        # Log de sucesso detalhado
        logger.info(
            f"Pagamento criado com sucesso. Email do destinatário: {recipient_email}, Valor: {amount} {currency}, Status: {payment.get('status')}"
        )

        return {
            "status": "success",
            "message": "Pagamento criado com sucesso.",
            "recipient_email": recipient_email,
            "amount": amount,
            "currency": currency,
            "batch_id": payment.get("batch_id"),
            "details": payment,
        }

    except IntegrityError as ex:
        logger.exception(
            "Integrity error while processing payment", exc_info=True, stack_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Erro de integridade ao processar pagamento.",
        ) from ex
    except Exception as ex:
        logger.critical(
            "Internal server error while processing payment",
            exc_info=True,
            stack_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar pagamento.",
        ) from ex
