from typing import List

from langchain.memory import summary
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    name: str = Field(description="The person's full name")
    summary: str = Field(description="A long summary of the person")
    facts: List[str] = Field(description="A list of two interesting facts about the person")

    def to_dict(self):
        return {
            "name": self.name,
            "summary": self.summary,
            "facts": self.facts,
        }

summary_parser=PydanticOutputParser(pydantic_object=Summary)
