from datetime import date

from pydantic import BaseModel, Field


class Paper(BaseModel):
    source: str
    external_id: str
    title: str
    abstract: str = ""
    authors: list[str] = Field(default_factory=list)
    published: date | None = None
    url: str = ""
    doi: str | None = None
    categories: list[str] = Field(default_factory=list)

    @property
    def searchable_text(self) -> str:
        return f"{self.title}\n\n{self.abstract}".strip()
