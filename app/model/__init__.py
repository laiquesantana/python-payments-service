from .payment import Payment
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import database

DBSession = database.DBSession
DeclarativeBase = declarative_base()
__all__ = ("Payment",)
