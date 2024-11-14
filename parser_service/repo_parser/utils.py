import logging

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