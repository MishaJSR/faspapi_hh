import logging


class AttributeException(AttributeError):
    def __init__(self, message="Error in sending kwargs"):
        self.message = message
        super().__init__(self.message)


def async_sqlalchemy_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            raise AttributeException()

    return wrapper
