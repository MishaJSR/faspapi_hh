import logging

from sqlalchemy import select, desc

from repository.exceptions import CustomException


def async_session_maker_decorator_select(func):
    async def wrapper(self_object, **kwargs):
        try:
            session = kwargs.get("session")
            field_filter = kwargs.get("field_filter")
            order_filter = kwargs.get("order_filter")
            data = kwargs.get("data")
            distinct = kwargs.get("distinct")
            if not kwargs.get("field_filter"):
                field_filter = {}
            if not data:
                raise CustomException(message="Expecting kwargs data")
            try:
                if distinct:
                    query = select(*[getattr(self_object.model, field) for field in data]).distinct()
                else:
                    if order_filter:
                        query = select(*[getattr(self_object.model, field) for field in data])\
                            .order_by(desc(getattr(self_object.model, order_filter)))
                    else:
                        query = select(*[getattr(self_object.model, field) for field in data])
            except AttributeError:
                raise CustomException(message="Unknown fields in data")
            try:
                for key, value in field_filter.items():
                    query = query.filter(getattr(self_object.model, key) == value)
            except AttributeError as e:
                logging.info(e)
                raise CustomException(message="Unknown fields in field_filter")
            res = await session.execute(query)
            return await func(self_object, data=data, result_query=res)
        except Exception as e:
            logging.info(e)

    return wrapper


class AlchemyDataObject:
    def __init__(self, keys, values):
        for key, value in zip(keys, values):
            setattr(self, key, value)
