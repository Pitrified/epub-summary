"""Prompt and response generation for the summarizer."""

from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from epub_summary.config.chat_openai import ChatOpenAIConfig


class ChapterRevised(BaseModel):
    """Revised chapter of a book.

    The revision should shorten the chapter roughly by half.
    Maintain all the pertinent details to be able to follow the story.
    Remove on the nose narration, and improve the overall quality of the
    prose, as would a book editor.

    Provide a short summary of the chapter as well.
    """

    summary: str = Field(..., description="The summary of the revised chapter.")
    revised_chapter: str = Field(..., description="The revised chapter.")


chapter_revised_template = """You are a book editor. \
You have a chapter to revise. \
You need to shorten the chapter roughly by half. \
Maintain all the pertinent details to be able to follow the story. \
Remove on the nose narration, and improve the overall quality of the prose, as would a book editor. \

Provide a short summary of the chapter as well. \

The original chapter is: {original_chapter}
"""
chapter_revised_prompt = ChatPromptTemplate(
    [SystemMessagePromptTemplate.from_template(chapter_revised_template)]
)


@dataclass
class ChapterReviser:
    """Pick a revised chapter."""

    chat_openai_config: ChatOpenAIConfig

    def __post_init__(self):
        """Initialize the action picker."""
        self.model = ChatOpenAI(**self.chat_openai_config.model_dump())
        self.structured_llm = self.model.with_structured_output(ChapterRevised)
        self.chain = chapter_revised_prompt | self.structured_llm

    def invoke(self, original_chapter: str) -> ChapterRevised:
        """Pick a revised chapter."""
        output = self.chain.invoke({"original_chapter": original_chapter})
        if not isinstance(output, ChapterRevised):
            raise ValueError(f"Unexpected output type: {type(output)}")
        return output
