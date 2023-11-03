from dataclasses import dataclass
from typing import Annotated

from pydantic import Field

Address = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{40}$")]
Transaction = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{64}$")]


@dataclass
class ContractFile:
    """
    The ContractFile class represents a contract file with a name and content.
    """
    name: str
    content: str
