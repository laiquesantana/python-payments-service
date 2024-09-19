from datetime import datetime
from typing import Any, Optional, Union
from uuid import uuid4
from sqlmodel import select
from app.config.database import db_session, start_or_use


class PaymentRepository:
    """Classe CRUD para o modelo de Payment."""

    guid: Union[str, None] = None
    __fields__: Any = None
    __editable__: list = [
        "email",
        "amount_cents",
        "currency",
        "payment_method",
        "status",
    ]
    __soft_delete__: bool = True

    @classmethod
    async def find_all(cls) -> list[Any]:
        """Busca todos os pagamentos."""
        query = select(cls)  # type: ignore
        return await cls.all(query)

    @classmethod
    async def first(cls, query) -> Any:
        """Retorna o primeiro resultado da query."""
        async with db_session() as session:
            if cls.__soft_delete__:
                query = query.where(cls.deleted_at.is_(None))  # type: ignore
            results = await session.scalars(query)
            return results.first()

    @classmethod
    async def all(cls, query) -> list[Any]:
        """Retorna todos os resultados da query."""
        async with db_session() as session:
            if cls.__soft_delete__:
                query = query.where(cls.deleted_at.is_(None))  # type: ignore
            query = query.order_by(cls.created_at)
            results = await session.scalars(query)
            return results.fetchall()

    @classmethod
    async def find_by_order_id(cls, order_id: str) -> Any:
        """Busca um pagamento pelo order_id."""
        query = select(cls).where(cls.order_id == order_id)  # type: ignore
        return await cls.first(query)

    async def save(self, transaction=None) -> Any:
        """Salva o pagamento no banco de dados."""
        current_timestamp = datetime.now()

        if hasattr(self, "created_at") and self.guid is None:
            self.created_at: Optional[datetime] = current_timestamp

        if hasattr(self, "updated_at"):
            self.updated_at: Optional[datetime] = current_timestamp

        if hasattr(self, "guid") and self.guid is None:
            self.guid = str(uuid4())

        async with start_or_use(transaction) as transaction:
            transaction.add(self)

        return self

    async def update(self, new, transaction=None) -> Any:
        """Atualiza os dados do pagamento."""
        for field in self.__editable__:
            if field in new and field in self.__fields__:
                setattr(self, field, new[field])
        await self.save(transaction=transaction)
        return self

    async def soft_delete(self, transaction=None) -> Any:
        """Aplica soft delete no pagamento."""
        if not self.__soft_delete__:
            raise Exception("Soft delete não suportado para esse modelo.")

        self.deleted_at: Optional[datetime] = datetime.now()
        async with start_or_use(transaction) as transaction:
            transaction.add(self)

        return self
