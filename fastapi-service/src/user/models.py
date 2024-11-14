import uuid
from datetime import datetime

from parso.python.tree import String
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, BigInteger, UUID, String)
from sqlalchemy.orm import relationship

from database import Base
from repository.repository import SQLAlchemyRepository


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    tg_user_id = Column(String, nullable=False, unique=True)
    is_block_bot: bool = Column(Boolean, default=False, nullable=False)
    is_auth: bool = Column(Boolean, default=False, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)

    subscribers = relationship("Subscriber", back_populates="user")

class UserRepository(SQLAlchemyRepository):
    model = User


user_repository = UserRepository()
