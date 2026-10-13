import pytest

from app.services.response_agents import select_response_agent


@pytest.mark.parametrize(("question", "expected"), [
    ("What are the signs of malaria?", "clinical"),
    ("What symptoms should I report to the clinic?", "clinical"),
    ("Explain the findings in the malaria report", "clinical"),
    ("Write a patient handout about malaria prevention", "writing"),
    ("Write about malaria prevention for patients", "writing"),
    ("Draft an email about the outbreak report", "writing"),
    ("Rewrite the malaria guidance in plain language", "writing"),
    ("Summarise pneumonia treatment", "writing"),
    ("Prepare a report on malaria", "report"),
    ("I need a report on malaria prevention", "report"),
    ("Revise the report about malaria", "report"),
    ("Can you write a short clinical report about dehydration?", "report"),
    ("Turn this into a situation report", "report"),
    ("Report on malaria prevention", "report"),
])
def test_routes_requested_output(question, expected):
    assert select_response_agent(question, []).name == expected


@pytest.mark.parametrize(("question", "expected"), [
    ("Make it shorter", "report"),
    ("Add an evidence gaps section", "report"),
    ("Rewrite it in plain language", "report"),
    ("Write a letter about this", "writing"),
    ("What is the treatment for malaria?", "clinical"),
])
def test_revision_inherits_report_but_new_request_overrides_it(question, expected):
    history = [
        {"role": "user", "content": "Prepare a report about malaria"},
        {"role": "assistant", "content": "Write an email instead"},
    ]
    assert select_response_agent(question, history).name == expected


def test_unrelated_question_breaks_report_inheritance():
    history = [
        {"role": "user", "content": "Prepare a report about malaria"},
        {"role": "user", "content": "What are the symptoms of pneumonia?"},
    ]
    assert select_response_agent("Make it shorter", history).name == "writing"
