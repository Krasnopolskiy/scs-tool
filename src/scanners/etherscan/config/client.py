from contextlib import asynccontextmanager
from random import choice

from aiohttp import ClientSession
from pydantic import Field
from pydantic_settings import BaseSettings

from scanners.etherscan.config import constants


class ClientSessionBuilder(BaseSettings):
    cf_clearance: str = ""
    user_agent: str = constants.USER_AGENT
    keys: list[str] = Field(default=list(), alias="ETHERSCAN_API_KEYS")

    @asynccontextmanager
    async def session(self) -> ClientSession:
        """
        The function `session` creates a ClientSession object with specified cookies and headers, yields
        the session, and closes the session when done.
        """
        session = ClientSession(cookies=self.cookies, headers=self.headers)
        try:
            yield session
        finally:
            await session.close()

    @property
    def cookies(self) -> dict[str, str]:
        """
        The function returns a dictionary with a key "cf_clearance" and its corresponding value
        self.cf_clearance.
        :return: a dictionary with a key "cf_clearance" and the value of self.cf_clearance.
        """
        return {"cf_clearance": self.cf_clearance}

    @property
    def headers(self) -> dict[str, str]:
        """
        The function returns a dictionary with a single key-value pair, where the key is "User-Agent"
        and the value is the user_agent attribute of the object.
        :return: a dictionary with a single key-value pair. The key is "User-Agent" and the value is the
        user_agent attribute of the object.
        """
        return {"User-Agent": self.user_agent}

    @property
    def apikey(self) -> str:
        """
        The function `apikey` returns a randomly chosen API key from a list of keys.
        :return: A randomly chosen API key from the list of keys stored in the `self.keys` attribute.
        """
        return choice(self.keys)


session_builder = ClientSessionBuilder()
