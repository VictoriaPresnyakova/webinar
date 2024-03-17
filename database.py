import os
from contextlib import asynccontextmanager
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum


from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    TIMESTAMP,
    String, BigInteger
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

engine = create_async_engine(
    os.environ["DB_URL"],
    #echo=True,
    future=True,
)

Base = declarative_base()


class StatusEnum(Enum):
    ALIVE = 'ALIVE'
    DEAD = 'DEAD'
    FINISHED = 'FINISHED'


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False)
    status = Column(PgEnum(StatusEnum, name='status_enum', create_type=False), nullable=False, default=StatusEnum.ALIVE)
    status_updated_at = Column(TIMESTAMP, nullable=False)
    msg_num = Column(Integer, nullable=False)
    msg_to_send_at = Column(TIMESTAMP, nullable=False)


def async_session_generator():
    return sessionmaker(engine, class_=AsyncSession)


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
