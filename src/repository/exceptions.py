import logging


class CustomException(AttributeError):
    def __init__(self, message="Custom exception occurred"):
        self.message = message
        super().__init__(self.message)


def async_sqlalchemy_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.warning(e)

    return wrapper
