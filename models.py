from pydantic import BaseModel


class ChoiceQuestion(BaseModel):
    question: str
    choices: list[str]
    answer: str


class FillInTheBlankQuestion(BaseModel):
    question: str
    answer: str
