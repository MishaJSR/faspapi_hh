from datetime import datetime
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Table)

from src.database import Base
from src.repository.repository import SQLAlchemyRepository


class Vacancy(Base):
    __tablename__ = "vacancy"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    salary = Column(String, nullable=False)
    experience = Column(String, nullable=False)
    employer = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class VacancyRepository(SQLAlchemyRepository):
    model = Vacancy
