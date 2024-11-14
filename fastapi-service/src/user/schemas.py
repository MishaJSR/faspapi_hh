from typing import Optional

from pydantic import BaseModel


class ConstructUser(BaseModel):
    tg_user_id: int
    is_block_bot: Optional[bool] = False
    is_auth: Optional[bool] = False

class UserCreateModel(BaseModel):
    id: int
    tg_user_id: int

class UserPaginationModel(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None


class ResponseAllUsers(BaseModel):
    id: int
    tg_user_id: int
    is_block_bot: Optional[bool] = False
    is_auth: Optional[bool] = False


class ResponseDeleteUsers(BaseModel):
    tg_user_id: int





