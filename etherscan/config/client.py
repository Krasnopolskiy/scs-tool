from contextlib import asynccontextmanager

from aiohttp import ClientSession
from pydantic_settings import SettingsConfigDict, BaseSettings


class ClientSessionBuilder(BaseSettings):
    """
    The `ClientSessionBuilder` class represents client settings for a web application, including model
    configuration, user agent, and session management.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    cf_clearance: str
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    )

    @asynccontextmanager
    async def session(self):
        """
        The function creates a session using the `ClientSession` class from the `aiohttp` library, and
        yields the session for use in a coroutine, ensuring that the session is closed after the
        coroutine is finished.
        """
        session = ClientSession(cookies=self.cookies, headers=self.headers)
        try:
            yield session
        finally:
            await session.close()

    @property
    def cookies(self):
        """
        The function returns a dictionary with a key "cf_clearance" and its corresponding value
        self.cf_clearance.
        :return: a dictionary with a key "cf_clearance" and the value of self.cf_clearance.
        """
        return {"cf_clearance": self.cf_clearance}

    @property
    def headers(self):
        """
        The function returns a dictionary with a single key-value pair, where the key is "User-Agent"
        and the value is the user_agent attribute of the object.
        :return: a dictionary with a single key-value pair. The key is "User-Agent" and the value is the
        user_agent attribute of the object.
        """
        return {"User-Agent": self.user_agent}
