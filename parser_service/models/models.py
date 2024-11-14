import uuid
from datetime import datetime
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, BigInteger, ForeignKey, String, UUID)
from sqlalchemy.orm import relationship

from database import Base
from repository.repository import SQLAlchemyRepository


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    tg_user_id = Column(String, nullable=False, unique=True)
    is_block_bot: bool = Column(Boolean, default=False, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)

    subscribers = relationship("Subscriber", back_populates="user")


class UserRepository(SQLAlchemyRepository):
    model = User


class Subscriber(Base):
    __tablename__ = "subscriber"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    sub_tag = Column(String, nullable=False)
    is_no_exp = Column(Boolean, nullable=False)
    is_remote = Column(Boolean, nullable=False)
    user_tg_id = Column(String, ForeignKey('user.tg_user_id'))

    user = relationship("User", back_populates="subscribers")


class SubscriberRepository(SQLAlchemyRepository):
    model = Subscriber


class Vacancy(Base):
    __tablename__ = "vacancy"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    salary = Column(String, nullable=False)
    is_no_exp = Column(Boolean, nullable=False)
    is_remote = Column(Boolean, nullable=False)
    employer = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class VacancyRepository(SQLAlchemyRepository):
    model = Vacancy


vac_repository = VacancyRepository()
sub_repository = SubscriberRepository()
user_repository = UserRepository()
