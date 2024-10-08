from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, conint


class ConstructSubscriber(BaseModel):
    sub_tag: str
    is_no_exp: bool
    is_remote: bool
    user_tg_id: conint(strict=True, gt=0)
