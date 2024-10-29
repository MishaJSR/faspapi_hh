from pydantic import BaseModel, conint


class ConstructSubscriber(BaseModel):
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: int


class ResponseAllSubs(BaseModel):
    sub_id: int
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: int

