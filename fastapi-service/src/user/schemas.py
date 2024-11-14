import uuid
from typing import Optional

from pydantic import BaseModel


class ConstructUser(BaseModel):
    tg_user_id: str
    is_block_bot: Optional[bool] = False
    is_auth: Optional[bool] = False

class UserCreateModel(BaseModel):
    id: uuid.UUID
    tg_user_id: str

class UserPaginationModel(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None


class ResponseAllUsers(BaseModel):
    id: uuid.UUID
    tg_user_id: str
    is_block_bot: Optional[bool] = False
    is_auth: Optional[bool] = False


class ResponseDeleteUsers(BaseModel):
    tg_user_id: str





