import re

import streamlit as st

from agents.models import ChoiceQuestion, FillInTheBlankQuestion
from agents.studybuddy import StudyBuddyAgent
from settings import Settings


@st.cache_resource
def get_agent():
    return StudyBuddyAgent(Settings())


def format_choice_question(question: ChoiceQuestion, index: int):
    st.radio(question.question, question.choices, key=f"question_{index}")


def format_fill_question(question: FillInTheBlankQuestion, index: int):
    st.write(re.sub(r"_{2,}", "`______`", question.question))
    st.text_input("Answer: ", key=f"question_{index}")


with st.sidebar:
    st.title("Study Buddy")
    st.subheader("Generate study questions")
    with st.form("generate_questions", border=False):
        amount = st.number_input(
            "Amount of questions", value=3, min_value=1, max_value=10, key="amount"
        )
        difficulty = st.selectbox(
            "Difficulty", ["easy", "medium", "hard"], key="difficulty"
        )
        format = st.selectbox("Format", ["choice", "fill"], key="format")
        topic = st.text_input("Topic", "math", key="topic")
        st.form_submit_button("Generate questions", key="submit")


if st.session_state.get("submit_quiz"):
    questions = st.session_state.get("questions", [])
    answers = [
        st.session_state.get(f"question_{index}")
        for index, question in enumerate(questions)
    ]
    correct_answers = [
        question.answer == answer for question, answer in zip(questions, answers)
    ]
    st.title(f"You got {sum(correct_answers)} out of {len(questions)} correct")

    for question, answer in zip(questions, answers):
        st.write(f"Question: {question.question}")
        st.write(f"Your answer: {answer}")
        st.write(f"Correct answer: {question.answer}")
        st.write("-" * 100)

elif st.session_state.get("submit"):
    agent = get_agent()
    with st.spinner("Generating questions..."):
        questions = [
            agent.generate_question(
                format=st.session_state.get("format"),
                difficulty=st.session_state.get("difficulty"),
                topic=st.session_state.get("topic"),
            )
            for _ in range(st.session_state.get("amount"))
        ]
        st.session_state["questions"] = questions
    with st.form("quiz", border=False):
        for index, question in enumerate(questions):
            if hasattr(question, "choices"):
                format_choice_question(question, index)
            else:
                format_fill_question(question, index)
        st.form_submit_button("Submit", key="submit_quiz")
