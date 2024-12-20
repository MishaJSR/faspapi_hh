from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from repository.repository import SQLAlchemyRepository
from database import Base


class Subscriber(Base):
    __tablename__ = "subscriber"

    id = Column(Integer, primary_key=True)
    sub_tag = Column(String, nullable=False)
    is_no_exp = Column(Boolean, nullable=False)
    is_remote = Column(Boolean, nullable=False)
    user_tg_id = Column(Integer, ForeignKey('user.tg_user_id'))

    user = relationship("User", back_populates="subscribers")


class SubscriberRepository(SQLAlchemyRepository):
    model = Subscriber


sub_repository = SubscriberRepository()
