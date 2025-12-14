from langchain_core.prompts import PromptTemplate

choice_question_template = PromptTemplate.from_template(
    """
    Generate a {difficulty} choice question about {topic}.
    The question should be a multiple choice question with 4 choices.
    The answer should be the correct choice.
    """,
    input_variables=["difficulty", "topic"],
)

fill_question_template = PromptTemplate.from_template(
    """
    Generate a {difficulty} fill in the blank question about {topic}.
    The question should be a fill in the blank question with a single blank.
    The answer should be the correct answer.
    """,
    input_variables=["difficulty", "topic"],
)
