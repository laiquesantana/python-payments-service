from datetime import datetime
from typing import Any, Optional, Union
from uuid import uuid4

from sqlmodel import select

from app.config.database import db_session, start_or_use
from app.exceptions import SoftDeleteDoesNotSupported

# TODO: change this class to dont use SQLModel


class CRUDBase:
    """Base class for models.

    This class implements the basic CRUD (Create, Read, Update, Delete) operations
    for the models.

    Attributes:
        guid (str): Unique identifier for the model
        __config__ (dict): Configuration for the model
        __editable__ (list): List of editable fields
        __filters__ (dict): List of filters
        __soft_delete__ (bool): If the model supports soft delete. Default is True.

    """

    guid: Union[str, None] = None
    __fields__: Any = None
    __config__: Any = None
    __editable__: list = []
    __filters__: dict = {}
    __soft_delete__: bool = True

    @classmethod
    async def find_all(cls) -> list[Any]:
        """Find all models.

        Returns:
            `list`: List of models found.

        """
        query = select(cls)  # type: ignore
        return await cls.all(query)

    @classmethod
    async def first(cls, query) -> Any:
        """Return the first result of a query.

        Args:
            query (`sqlmodel.select`): Query to execute.

        Returns:
            `sqlmodel.select`: First result of the query.

        """
        async with db_session() as session:
            if cls.__soft_delete__:
                query = query.where(cls.deleted_at.is_(None))  # type: ignore
            results = await session.scalars(query)
            return results.first()

    @classmethod
    async def all(cls, query) -> list[Any]:
        """Return all results of a query.

        Args:
            query (`sqlmodel.select`): Query to execute.

        Returns:
            `sqlmodel.select`: All results of the query.

        """
        async with db_session() as session:
            if cls.__soft_delete__:
                query = query.where(cls.deleted_at.is_(None))  # type: ignore
            query = query.order_by(cls.created_at)
            results = await session.scalars(query)
            return results.fetchall()

    @classmethod
    async def find_by_guid(cls, guid: str) -> Any:
        """Find a model by guid.

        Args:
            guid (`str`): Guid to search.

        Returns:
            `sqlmodel.select`: Model found.

        """
        query = select(cls).where(cls.guid == guid)  # type: ignore
        return await cls.first(query)

    @classmethod
    async def execute(cls, query, transaction=None):
        """Execute a query.

        Args:
            query (`sqlmodel.select`): Query to execute.
            transaction (`sqlmodel.Session`): Transaction to use. Default is None.

        """
        async with start_or_use(transaction) as transaction:
            await transaction.execute(query)

    async def save(self, transaction=None) -> Any:
        """Save model to database.

        Args:
            transaction (`sqlmodel.Session`): Transaction to use. Default is None.

        Returns:
            `Model`: Saved object model.

        """
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
        """Update object model with new values.

        Args:
            new (`dict`): New values to update.
            transaction (`sqlmodel.Session`): Transaction to use. Default is None.

        Returns:
            `Model`: Updated object model.

        """
        for field in self.__editable__:
            if field in new and field in self.__fields__:
                setattr(self, field, new[field])
        await self.save(transaction=transaction)
        return self

    async def soft_delete(self, transaction=None) -> Any:
        """Soft delete object model.

        Args:
            transaction (`sqlmodel.Session`): Transaction to use. Default is None.

        Returns:
            `Model`: Soft deleted object model.

        """
        if not self.__soft_delete__:
            raise SoftDeleteDoesNotSupported(self.__class__.__name__)

        self.deleted_at: Optional[datetime] = datetime.now()
        async with start_or_use(transaction) as transaction:
            transaction.add(self)

        return self
