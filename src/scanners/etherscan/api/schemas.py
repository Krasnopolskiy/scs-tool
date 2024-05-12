from pydantic import BaseModel, Field


class ContractSourceCode(BaseModel):
    data: str = Field(alias="SourceCode")


class ContractSourceResponse(BaseModel):
    class Config:
        extra = "allow"

    contracts: list[ContractSourceCode] = Field(alias="result")
