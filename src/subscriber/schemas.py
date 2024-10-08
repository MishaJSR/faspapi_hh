from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, conint


class ConstructSubscriber(BaseModel):
    sub_tag: str
    sub_addition: Optional[str] = ""
    user_tg_id: conint(strict=True, gt=0)
