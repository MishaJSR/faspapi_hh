from datetime import datetime
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Table, BigInteger)
from sqlalchemy.orm import relationship

from src.repository.repository import SQLAlchemyRepository

from src.database import Base


class Subscriber(Base):
    __tablename__ = "subscriber"

    id = Column(Integer, primary_key=True)
    sub_tag = Column(String, nullable=False)
    sub_addition = Column(String, nullable=False)
    user_tg_id = Column(Integer, ForeignKey('user.tg_user_id'))


class SubscriberRepository(SQLAlchemyRepository):
    model = Subscriber
