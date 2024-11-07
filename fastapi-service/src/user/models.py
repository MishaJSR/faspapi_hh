from datetime import datetime
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, BigInteger)
from sqlalchemy.orm import relationship

from database import Base
from repository.repository import SQLAlchemyRepository


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(BigInteger, nullable=False, unique=True)
    is_block_bot: bool = Column(Boolean, default=False, nullable=False)
    is_auth: bool = Column(Boolean, default=False, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)

    subscribers = relationship("Subscriber", back_populates="user")

class UserRepository(SQLAlchemyRepository):
    model = User


user_repository = UserRepository()
