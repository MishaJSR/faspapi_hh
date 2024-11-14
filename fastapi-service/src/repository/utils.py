import logging

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session


def connection(method):
    async def wrapper(*args, **kwargs):
        async for session in get_async_session():
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                logging.error(e)

    return wrapper


def async_session_maker_decorator_select(func):
    async def wrapper(self_object, **kwargs):
        session: AsyncSession = kwargs.get("session")
        field_filter = kwargs.get("field_filter")
        order_filter = kwargs.get("order_filter")
        data = kwargs.get("data")
        if not kwargs.get("field_filter"):
            field_filter = {}
        if not data:
            logging.error(f"Expecting kwargs data")
        try:
            if kwargs.get("distinct"):
                query = select(*[getattr(self_object.model, field) for field in data]).distinct()
            else:
                if order_filter:
                    query = select(*[getattr(self_object.model, field) for field in data]) \
                        .order_by(desc(getattr(self_object.model, order_filter)))
                else:
                    query = select(*[getattr(self_object.model, field) for field in data])
        except AttributeError:
            logging.error("Unknown fields in data")
            return
        try:
            for key, value in field_filter.items():
                query = query.filter(getattr(self_object.model, key) == value)
        except AttributeError as e:
            logging.error(f"Unknown fields in field_filter {e}")
            return
        res = await session.execute(query)
        return await func(self_object, data=data, result_query=res)

    return wrapper


class AlchemyDataObject:
    def __init__(self, keys, values):
        for key, value in zip(keys, values):
            setattr(self, key, value)
