from loguru import logger


def handle_exceptions(func):
    """
    The `handle_exceptions` function is a decorator that wraps an async function and catches any
    exceptions that occur, logging them with a logger.

    :param func: The `func` parameter is a function that will be wrapped with exception handling
    :return: The function being returned is a wrapper function that handles exceptions.
    """

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:
            logger.exception(exc)

    return wrapper
