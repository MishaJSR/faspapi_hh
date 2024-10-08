from datetime import datetime
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, String, BigInteger)

from src.database import Base
from src.repository.repository import SQLAlchemyRepository


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(BigInteger, nullable=False, unique=True)
    user_tag = Column(String, nullable=False)
    is_block_bot: bool = Column(Boolean, default=False, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)


class UserRepository(SQLAlchemyRepository):
    model = User
