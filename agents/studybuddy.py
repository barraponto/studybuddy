from typing import Literal

from langchain.agents import create_agent

from agents.models import ChoiceQuestion, FillInTheBlankQuestion
from agents.prompts import prompt_by_format
from settings import Settings

system_prompt = """
You are a helpful assistant that generates study questions.
"""


class StudyBuddyAgent:
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate_question(
        self,
        format: Literal["choice", "fill"] = "choice",
        difficulty: Literal["easy", "medium", "hard"] = "easy",
        topic: str = "math",
    ) -> ChoiceQuestion | FillInTheBlankQuestion:
        agent = self.quiz_agent(format)
        prompt = prompt_by_format(format).format(difficulty=difficulty, topic=topic)
        result = agent.invoke({"messages": [("user", prompt)]})
        if result["structured_response"] is None:
            raise ValueError("No response from agent")
        return result["structured_response"]

    def quiz_agent(self, format: Literal["choice", "fill"] = "choice"):
        match format:
            case "choice":
                response_format = ChoiceQuestion
            case "fill":
                response_format = FillInTheBlankQuestion
            case _:
                raise ValueError(f"Invalid format: {format}")

        return create_agent(
            model=self.settings.groq_model,
            system_prompt=system_prompt,
            response_format=response_format,
            tools=[],
        )
