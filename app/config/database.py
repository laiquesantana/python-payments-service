from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.config.config import get_settings

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_pool_overflow,
)


db_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class ORMDictCompare:  # pylint: disable=R0903 # pragma: no cover
    """Class to compare two ORM objects.

    Attributes:
        __config__ (dict): Configuration for the model

    """

    __config__: dict = {}

    def __eq__(self, other):
        self_dict = self.__dict__
        self_dict.pop("_sa_instance_state")

        other_dict = other.__dict__
        other_dict.pop("_sa_instance_state")

        return self_dict == other_dict


@asynccontextmanager
async def start_or_use(transaction=None):  # pragma: no cover
    """Function to start a transaction or use an existing one.

    Args:
        transaction (`sqlmodel.Transaction`): Transaction to use if exists. Default is None.

    yields:
        `sqlmodel.Transaction`: Transaction to use.

    """
    if transaction:
        yield transaction
        return

    async with db_transaction() as transaction:
        yield transaction


@asynccontextmanager
async def db_transaction():  # pragma: no cover
    """Database transaction context manager."""

    session = db_session()
    try:
        session.begin()
        yield session
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
