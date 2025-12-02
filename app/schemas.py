from pydantic import BaseModel
from typing import Optional


class TermBase(BaseModel):
    keyword: str
    description: str


class TermCreate(TermBase):
    pass


class TermUpdate(BaseModel):
    keyword: Optional[str] = None
    description: Optional[str] = None


class Term(TermBase):
    id: int

    class Config:
        orm_mode = True
