from datetime import datetime
from typing import Optional

import pydantic
from pydantic import BaseModel, field_validator
import validators


class ConstructVacancy(BaseModel):
    url: str
    name: str
    salary: str
    is_no_exp: bool
    is_remote: bool
    employer: str
    location: str
    is_active: Optional[bool] = True

    @field_validator('url')
    def validate_url(cls, v):
        if not validators.url(v):
            raise pydantic.ValidationError
        return v


class VacPaginationModel(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None


class ResponseAllVac(BaseModel):
    id: int
    name: str
    url: str
    salary: str
    is_no_exp: bool
    is_remote: bool
    employer: str
    location: str
    is_active: Optional[bool] = True


