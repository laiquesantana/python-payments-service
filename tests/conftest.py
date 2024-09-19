import asyncio
import contextlib

import pytest
import responses
import sqlalchemy
from sqlalchemy import MetaData

from app.config.database import SQLALCHEMY_DATABASE_URL

ENGINE_METADATA: MetaData | None = None
DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("+asyncpg", "")
ENGINE = sqlalchemy.create_engine(DATABASE_URL, future=True)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def clear_db():
    global ENGINE
    global ENGINE_METADATA

    if not ENGINE_METADATA:
        ENGINE_METADATA = MetaData()
        ENGINE_METADATA.reflect(ENGINE)

    with contextlib.closing(ENGINE.connect()) as con:
        trans = con.begin()
        for table in reversed(ENGINE_METADATA.sorted_tables):
            if table.name == "alembic_version":
                continue
            con.execute(table.delete())
        trans.commit()


@pytest.fixture(autouse=True)
async def _clear_database():
    yield
    clear_db()


@pytest.fixture(autouse=True)
async def _start_and_stop_responses():
    responses.start()
    yield
    responses.stop()
