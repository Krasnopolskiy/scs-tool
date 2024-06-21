from dataclasses import dataclass
from typing import Any

from loguru import logger
from pydantic import BaseModel, model_validator

from analyzers.mythril.constants import MYTHRIL_REPORT_FILE
from common.schemas import Address, BaseFile


class Issue(BaseModel):
    class Config:
        extra = "ignore"

    description: str

    @model_validator(mode="before")
    def validate(self, value: Any) -> dict:
        description = self["description"]
        filename = self["filename"]
        title = self["title"]
        contract = self["contract"]
        function = self["function"]
        return {"description": f"{title} in {contract}.{function} ({filename}):\n{description}"}


class Report(BaseModel):
    class Config:
        extra = "ignore"

    issues: list[Issue]


@dataclass
class MythrilReportFile(BaseFile[Report]):
    name: str = MYTHRIL_REPORT_FILE

    def get_content(self) -> str:
        return self.content.model_dump_json()

    def write(self, address: Address):
        super().write(address)
        for issue in self.content.issues:
            logger.warning("[{}] {}", address, issue.description)
