import uuid
from datetime import datetime
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, String, UUID)

from database import Base
from repo.repository import SQLAlchemyRepository


class Vacancy(Base):
    __tablename__ = "vacancy"

    id = Column(UUID(as_uuid=True), primary_key=True)
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
