from dataclasses import dataclass

from loguru import logger
from pydantic import BaseModel

from analyzers.slither.constants import SLITHER_REPORT_FILE
from common.schemas import Address, BaseFile


class Issue(BaseModel):
    class Config:
        extra = "ignore"

    description: str


class Report(BaseModel):
    class Config:
        extra = "ignore"

    issues: list[Issue]


@dataclass
class SlitherReportFile(BaseFile[Report]):
    name: str = SLITHER_REPORT_FILE

    def get_content(self) -> str:
        return self.content.model_dump_json()

    def write(self, address: Address):
        super().write(address)
        for issue in self.content.issues:
            logger.warning("[{}] {}", address, issue.description)
