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


