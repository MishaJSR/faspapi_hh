from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class ConstructVacancy(BaseModel):
    url: str
    name: str
    salary: str
    experience: str
    employer: str
    location: str
    is_active: Optional[bool] = True
