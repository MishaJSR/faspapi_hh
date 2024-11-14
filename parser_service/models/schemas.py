import uuid
from typing import Optional

import pydantic
import validators
from pydantic import BaseModel, field_validator


class ConstructSubscriber(BaseModel):
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: str


class ResponseAllSubs(BaseModel):
    sub_id: uuid.UUID
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: str

class ConstructUser(BaseModel):
    tg_user_id: str
    is_block_bot: Optional[bool] = False


class ResponseAllUsers(BaseModel):
    user_id: uuid.UUID
    tg_user_id: str
    is_block_bot: bool


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
