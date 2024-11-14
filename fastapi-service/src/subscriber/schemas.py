from typing import Optional

from pydantic import BaseModel, conint


class ConstructSubscriber(BaseModel):
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: int


class SubPaginationModel(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None


class ResponseUpdateSubs(BaseModel):
    id: int


class ResponseAllSubs(BaseModel):
    id: int
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: int

