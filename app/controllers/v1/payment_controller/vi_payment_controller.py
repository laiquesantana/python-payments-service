from fastapi import APIRouter, HTTPException, Body
from app.services import VindiService
from app.services.vi_gateway.vi_gateway import VindiGateway
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)

router = APIRouter(prefix="/v1/vindi", tags=["Vindi Payments"])

vindi_service = VindiService(VindiGateway())


@router.post("/customer")
async def create_vindi_customer(
    name: str = Body(...), email: str = Body(...), cpf_cnpj: str = Body(...)
):
    """Endpoint para criar um novo cliente na Vindi."""
    try:
        customer = vindi_service.create_customer(name, email, cpf_cnpj)
        return {
            "status": "success",
            "customer_id": customer.get("id"),
            "details": customer,
        }
    except Exception as e:
        logger.error(f"Erro ao criar cliente na Vindi: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/payment")
async def create_vindi_payment(
    customer_id: int = Body(...),
    amount: float = Body(...),
):
    """Endpoint para criar um pagamento para um cliente existente na Vindi."""
    try:
        payment = vindi_service.create_payment(customer_id, amount)
        return {
            "status": "success",
            "payment_id": payment.get("id"),
            "details": payment,
        }
    except Exception as e:
        logger.error(f"Erro ao processar pagamento na Vindi: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
