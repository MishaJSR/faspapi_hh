import uuid
from typing import Optional

from pydantic import BaseModel, conint


class ConstructSubscriber(BaseModel):
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: str


class DeleteSubSchema(BaseModel):
    tg_user_id: str

class ResponseDeleteSubSchema(BaseModel):
    user_tg_id: str


class SubPaginationModel(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None


class ResponseUpdateSubs(BaseModel):
    id: uuid.UUID


class ResponseAllSubs(BaseModel):
    id: uuid.UUID
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: str

