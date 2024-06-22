import json
from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from openai import OpenAI

from analyzers.openai.config import CONFIG_PATH, openai_config
from analyzers.openai.schemas import OpenAIMessage, OpenAIReportFile, Report
from common.constants import SOURCE_PATH
from common.schemas import Address

CONFIG = Path(__file__).parent / CONFIG_PATH

client = OpenAI(api_key=openai_config.key)


class Template(str, Enum):
    HONEYPOT = "honeypot.j2"
    PONZI = "ponzi.j2"


def load_template(template: Template, *args, **kwargs) -> str:
    env = Environment(loader=FileSystemLoader(CONFIG.absolute()))
    template = env.get_template(template.value)
    return template.render(*args, **kwargs)


def request_model(target: Path) -> dict:
    result: dict = {}
    contract = target.read_text()
    for template in Template:
        prompt = load_template(template, contract=contract)
        message = OpenAIMessage(content=prompt)
        chat = client.chat.completions.create(
            messages=[message.model_dump()],
            model=openai_config.model,
        )
        report = chat.choices[0].message.content
        report = report.replace("```json", "")
        report = report.replace("```", "")
        result.update(json.loads(report))
    return result


def process_targets(targets: list[Path]) -> dict:
    report: dict = {}
    for target in targets:
        report.update(request_model(target))
    return report


async def analyze(address: Address) -> OpenAIReportFile | None:
    target = SOURCE_PATH / address
    targets = list(target.rglob("*.sol"))
    if not targets:
        logger.info("[{}] Nothing to analyze", address)
        return None
    logger.info("[{}] Running OpenAI analysis", address)
    report = process_targets(targets)
    return OpenAIReportFile(content=Report(**report))
