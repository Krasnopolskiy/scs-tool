from dataclasses import dataclass
from typing import Any

from loguru import logger
from pydantic import BaseModel, Field, model_validator

from analyzers.semgrep.constants import SEMGREP_REPORT_FILE
from common.schemas import Address, BaseFile


class Issue(BaseModel):
    class Config:
        extra = "ignore"

    description: str

    @model_validator(mode="before")
    def validate(self, value: Any) -> dict:
        description = self["extra"]["message"]
        path = self["path"]
        return {"description": f"({path}):\n{description}"}


class Report(BaseModel):
    class Config:
        extra = "ignore"

    issues: list[Issue] = Field(alias="results")


@dataclass
class SemgrepReportFile(BaseFile[Report]):
    name: str = SEMGREP_REPORT_FILE

    def get_content(self) -> str:
        return self.content.model_dump_json()

    def write(self, address: Address):
        super().write(address)
        for result in self.content.issues:
            logger.warning("[{}] {}", address, result.description)
