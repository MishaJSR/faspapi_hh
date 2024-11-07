from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod

from pydantic import ValidationError
import logging

from rabbit_utils.schemas import FastApiRabbit, FastApiRabbit2


class AnyDataObject(ABC):
    @abstractmethod
    def operation(self):
        pass


class CreateCheckUserData(AnyDataObject):
    _pydantic_model = FastApiRabbit

    def __init__(self, data):
        self._data = data

    async def operation(self):
        logging.info(f"Do operation with {self._data}")
        await asyncio.sleep(0.1)



class CreateCheckUserDataAnother(AnyDataObject):
    _data = None
    _pydantic_model = FastApiRabbit

    @classmethod
    def __init__(cls, data):
        cls._data = data

    def operation(self):
        print("error")



class FastRMQDataObject:
    _pydantic_models = {"check_id": (FastApiRabbit, CreateCheckUserData),
                        "another": (FastApiRabbit2, CreateCheckUserDataAnother), }


    @classmethod
    def get_custom_object(cls, data):
        for pyd_model, base_class in cls._pydantic_models.values():
            try:
                pyd_model.model_validate(obj=data)
            except ValidationError:
                pass
            else:
                return base_class(data)
        print(f"No valid data for {data}")
