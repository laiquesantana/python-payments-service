from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from app.schema.schema import PaymentRequest
from app.services.iugu_service import IuguService
from app.services.iugu_gateway.iugu_gateway import IuguGateway

# Criação do router FastAPI
router = APIRouter(
    prefix="/v1/payments",
    tags=["Payments"],
    responses={404: {"description": "Not found"}},
)

payment_service = IuguService(IuguGateway())


@router.post("/charge")
async def create_charge(payment_data: PaymentRequest):
    try:
        print(payment_data.dict())

        payment_service.create_payment(payment_data.dict())
        return {
            "status": "success",
            "message": "Payment request processed successfully",
            "details": payment_data.dict(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
