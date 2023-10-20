from enum import StrEnum

BASE_URL = "https://etherscan.io"


class Endpoint(StrEnum):
    TRANSACTION = "/address/{transaction_id}"


def reverse(endpoint: Endpoint, **kwargs) -> str:
    """
    The function takes an endpoint and keyword arguments, and returns a URL by formatting the endpoint
    with the provided arguments.

    :param endpoint: The `endpoint` parameter is a string that represents the endpoint of a URL. It may
    contain placeholders that can be replaced with values from the `kwargs` dictionary
    :type endpoint: Endpoint
    :return: a string that is the concatenation of the BASE_URL and the formatted endpoint string.
    """
    try:
        return BASE_URL + endpoint.format(**kwargs)
    except KeyError as exc:
        raise KeyError("Invalid reverse params") from exc
