from enum import Enum

from scanners.etherscan.config import constants


class Endpoint(str, Enum):
    TRANSACTION_LIST = "/txsInternal?ps={size}&p={offset}"
    TRANSACTION = "/tx/{transaction}"
    ADDRESS = "/address/{address}"
    SOURCE_CODE = "/api?module=contract&action=getsourcecode&address={address}&apikey={key}"


def reverse(endpoint: Endpoint, **kwargs) -> str:
    """
    The `reverse` function takes an endpoint and keyword arguments, and returns a URL by combining the
    base URL and the formatted endpoint.

    :param endpoint: The `endpoint` parameter is a string that represents the endpoint of a URL. It is a
    placeholder that can contain variables enclosed in curly braces `{}`. These variables will be
    replaced with values provided in the `kwargs` dictionary
    :type endpoint: Endpoint
    :return: a string that is the concatenation of the `constants.BASE_URL` and the formatted `endpoint`
    using the provided `kwargs`.
    """
    base = constants.BASE_API_URL if "api" in endpoint else constants.BASE_URL
    try:
        return base + endpoint.format(**kwargs)
    except KeyError as exc:
        raise KeyError("Invalid reverse params") from exc
