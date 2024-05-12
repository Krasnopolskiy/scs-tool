from loguru import logger

nothing = object()


def handle_exceptions(default=nothing):
    """
    The `handle_exceptions` decorator in Python catches exceptions in async functions and logs them,
    with an option to return a default value.

    :param default: The `default` parameter in the `handle_exceptions` decorator function is used to
    specify a default value that will be returned if an exception occurs within the decorated function.
    If no `default` value is provided, the decorator will log the exception and return `None`
    :return: The `handle_exceptions` function returns a decorator function that wraps the input function
    with error handling logic. If an exception occurs during the execution of the input function, the
    decorator catches the exception, logs it using a logger, and optionally returns a default value
    specified in the `default` parameter.
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                logger.error(exc)
                if default is not nothing:
                    return default

        return wrapper

    return decorator
