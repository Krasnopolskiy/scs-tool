from dataclasses import dataclass

from loguru import logger
from pydantic import BaseModel

from analyzers.openai.constants import OPENAI_REPORT_FILE
from common.schemas import Address, BaseFile


class OpenAIMessage(BaseModel):
    content: str
    role: str = "user"


class Issue(BaseModel):
    description: str


class Report(BaseModel):
    issues: list[Issue]


@dataclass
class OpenAIReportFile(BaseFile[Report]):
    name: str = OPENAI_REPORT_FILE

    def get_content(self) -> str:
        return self.content.model_dump_json()

    def write(self, address: Address):
        super().write(address)
        for result in self.content.issues:
            logger.warning("[{}] {}", address, result.description)
