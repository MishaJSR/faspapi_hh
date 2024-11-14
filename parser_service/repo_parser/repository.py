import uuid
from abc import ABC, abstractmethod
from typing import Union

from sqlalchemy import insert, update, delete, and_, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from repo_parser.exceptions import async_sqlalchemy_exceptions


class AbstractRepository(ABC):
    @abstractmethod
    async def add_object(self, **kwargs) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_fields(self, **kwargs) -> Union[list[dict], dict, list]:
        raise NotImplementedError

    @abstractmethod
    async def delete_fields(self, **kwargs) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def update_fields(self, **kwargs) -> Union[list[dict], dict, list]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_one_contain_field(self, **kwargs) -> Union[list[dict], list]:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: None

    @async_sqlalchemy_exceptions
    async def add_object(self, **kwargs) -> int:
        session = kwargs.get("session")
        stmt = insert(self.model).values(**kwargs.get("data"), id=str(uuid.uuid4())).returning(self.model.id)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()

    @async_sqlalchemy_exceptions
    async def get_all_by_fields(self, **kwargs) -> Union[list[dict], dict, list]:
        session: AsyncSession = kwargs.get("session")
        field_filter = kwargs.get("field_filter")
        order_filter = kwargs.get("order_filter")
        offset = kwargs.get("offset")
        limit = kwargs.get("limit")
        data = kwargs.get("data")
        is_one = kwargs.get("is_one")
        selected_fields = [getattr(self.model, field) for field in data]
        if order_filter:
            query = (select(*selected_fields).order_by(desc(getattr(self.model, order_filter))))
        else:
            query = select(*selected_fields)
        if field_filter:
            for key, value in field_filter.items():
                query = query.filter(getattr(self.model, key) == value)
        if limit and offset:
            query = query.limit(limit).offset(offset)
        res = await session.execute(query)
        if is_one:
            result = res.mappings().first()
            return dict(result) if result else []
        else:
            result = res.mappings().all()
            return [dict(el) for el in result] if result else []

    @async_sqlalchemy_exceptions
    async def delete_fields(self, **kwargs) -> list[dict]:
        conditions = [getattr(self.model, key) == value for key, value in kwargs.get("delete_filter").items()]
        session = kwargs.get("session")
        is_one = kwargs.get("is_one")
        stmt = (delete(self.model).where(and_(*conditions))
                .returning(*[getattr(self.model, key) for key, value in kwargs.get("delete_filter").items()]))
        result = await session.execute(stmt)
        await session.commit()
        if is_one:
            result = result.mappings().first()
            return dict(result) if result else []
        else:
            result = result.mappings().all()
            return [dict(el) for el in result] if result else []

    @async_sqlalchemy_exceptions
    async def update_fields(self, **kwargs) -> Union[list[dict], dict, list]:
        conditions = [getattr(self.model, key) == value for key, value in kwargs.get("update_filter").items()]
        session = kwargs.get("session")
        is_one = kwargs.get("is_one")
        stmt = update(self.model).where(and_(*conditions)).values(**kwargs.get("update_data")).returning(self.model.id)
        result = await session.execute(stmt)
        await session.commit()
        if is_one:
            result = result.mappings().first()
            return dict(result) if result else []
        else:
            result = result.mappings().all()
            return [dict(el) for el in result] if result else []


    @async_sqlalchemy_exceptions
    async def get_all_by_one_contain_field(self, **kwargs) -> Union[list[dict], list]:
        session = kwargs.get("session")
        query = select(*[getattr(self.model, field) for field in kwargs.get("data")])
        if kwargs.get("contain_field"):
            for key, value in kwargs.get("contain_field").items():
                query = query.filter(getattr(self.model, key).ilike(f"%{value}%"))
        if kwargs.get("field_filter"):
            for key, value in kwargs.get("field_filter").items():
                query = query.filter(getattr(self.model, key) == value)
        res = await session.execute(query)
        result = res.mappings().all()
        return [dict(el) for el in result] if result else []

