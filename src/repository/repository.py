from abc import ABC, abstractmethod

from sqlalchemy import insert, update, delete, and_, select, func

from src.repository.exceptions import async_sqlalchemy_exceptions
from src.repository.utils import AlchemyDataObject
from src.repository.utils import async_session_maker_decorator_select


class AbstractRepository(ABC):
    @abstractmethod
    async def add_object(self, **kwargs) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_fields(self, **kwargs) -> AlchemyDataObject:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_fields(self, **kwargs) -> list[AlchemyDataObject]:
        raise NotImplementedError

    @abstractmethod
    async def delete_fields(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_fields(self, **kwargs) -> list[AlchemyDataObject]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_contain_fields(self, **kwargs) -> list[AlchemyDataObject]:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: None

    @async_sqlalchemy_exceptions
    async def add_object(self, **kwargs) -> int:
        session = kwargs.get("session")
        stmt = insert(self.model).values(**kwargs.get("data")).returning(self.model.id)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()

    @async_session_maker_decorator_select
    async def get_one_by_fields(self, **kwargs) -> AlchemyDataObject:
        res_value = list(kwargs.get("result_query").fetchone())
        return AlchemyDataObject(kwargs.get("data"), res_value)

    @async_session_maker_decorator_select
    async def get_all_by_fields(self, **kwargs) -> list[AlchemyDataObject]:
        res_values = [el._data for el in kwargs.get("result_query").fetchall()]
        return [AlchemyDataObject(kwargs.get("data"), value) for value in res_values]

    @async_sqlalchemy_exceptions
    async def delete_fields(self, **kwargs):
        conditions = [getattr(self.model, key) == value for key, value in kwargs.get("delete_filter").items()]
        session = kwargs.get("session")
        stmt = delete(self.model).where(and_(*conditions)).returning(self.model.id)
        await session.execute(stmt)
        await session.commit()

    @async_sqlalchemy_exceptions
    async def update_fields(self, **kwargs) -> list[AlchemyDataObject]:
        conditions = [getattr(self.model, key) == value for key, value in kwargs.get("update_filter").items()]
        session = kwargs.get("session")
        stmt = update(self.model).where(and_(*conditions)).values(**kwargs.get("update_data")).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        res_values = [el._data for el in res.fetchall()]
        return [AlchemyDataObject(kwargs.get("update_data"), value) for value in res_values]

    @async_sqlalchemy_exceptions
    async def get_all_contain_fields(self, **kwargs):
        session = kwargs.get("session")
        query = select(*[getattr(self.model, field) for field in kwargs.get("data")])
        for key, value in kwargs.get("field_filter").items():
            query = query.filter(func.lower(getattr(self.model, key)).contains(value))
        res = await session.execute(query)
        res_values = [el._data for el in res.fetchall()]
        return [AlchemyDataObject(kwargs.get("data"), value) for value in res_values]
