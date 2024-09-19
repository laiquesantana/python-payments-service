from pydantic import BaseModel
from typing import List, Optional


# Definição do modelo de Item
class Item(BaseModel):
    description: str
    quantity: int
    price_cents: int
    id: Optional[str] = None
    _destroy: Optional[bool] = None


# Definição do modelo de endereço do pagador
class Address(BaseModel):
    street: str
    number: str
    district: str
    city: str
    state: str
    zip_code: str
    complement: Optional[str] = None


# Definição do modelo de pagador
class Payer(BaseModel):
    cpf_cnpj: str
    name: str
    phone_prefix: str
    phone: str
    email: str
    address: Address


# Definição do modelo principal
class PaymentRequest(BaseModel):
    method: str
    token: Optional[str] = None
    customer_payment_method_id: Optional[str] = None
    restrict_payment_method: Optional[bool] = False
    customer_id: Optional[str] = None
    invoice_id: Optional[str] = None
    email: Optional[str] = None
    months: Optional[int] = 0
    discount_cents: Optional[int] = 0
    bank_slip_extra_days: Optional[int] = 0
    keep_dunning: Optional[bool] = False
    items: List[Item]
    payer: Payer
    order_id: Optional[str] = None
    soft_descriptor_light: Optional[str] = None
