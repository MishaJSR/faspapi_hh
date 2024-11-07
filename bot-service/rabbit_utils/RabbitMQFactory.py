import asyncio
from abc import ABC, abstractmethod
from pydantic import ValidationError
import logging

from rabbit_utils.schemas import FastApiRabbit, FastApiRabbit2


class DefaultDataObject(ABC):
    def __init__(self, data):
        self._data = data

    @abstractmethod
    async def operation(self):
        pass


class CreateCheckUserData(DefaultDataObject):
    _pydantic_model = FastApiRabbit

    def __init__(self, data):
        super().__init__(data)

    async def operation(self):
        logging.info(f"Do operation with {self._data}")
        await asyncio.sleep(0)


class CreateCheckUserDataAnother(DefaultDataObject):
    _pydantic_model = FastApiRabbit

    def __init__(self, data):
        super().__init__(data)

    async def operation(self):
        logging.info("another operation")
        await asyncio.sleep(0)


class NullDataObject(DefaultDataObject):
    def __init__(self):
        super().__init__(None)

    async def operation(self):
        logging.info("Error in validation")
        await asyncio.sleep(0)


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
        return NullDataObject()

