import json

import pytest

from app.services.document_answer import render_document_selection


HITS = [
    {"content": "Drug A is not recommended. Refer to the specialist."},
    {"content": "This document contains no facility case counts."},
]


@pytest.mark.parametrize("raw", [
    "Drug A cures everyone [1].",
    '{"sections":[{"heading":"Answer","sources":[99]}]}',
    '{"sections":[{"heading":"Answer","sources":[0]}]}',
    '{"sections":[{"heading":"Answer","sources":[true]}]}',
    '{"sections":[{"heading":"Answer","sources":["1"]}]}',
    '{"sections":[{"heading":"Drug A cures everyone","sources":[1]}]}',
    '{"sections":[{"heading":"Answer","sources":[1],"text":"Invented advice"}]}',
    '{"sections":[],"answer":"Invented advice [1]"}',
    '{"sections":[{"heading":"Answer","sources":[]}]}',
    'null',
    '',
])
def test_unvalidated_prose_or_selection_is_rejected(raw):
    with pytest.raises(ValueError):
        render_document_selection(raw, HITS)


def test_complete_source_preserves_negation_and_qualifiers():
    raw = json.dumps({"sections": [{"heading": "Answer", "sources": [1]}]})
    answer, cited = render_document_selection(raw, HITS)
    assert "Drug A is not recommended" in answer
    assert "Refer to the specialist" in answer
    assert cited == [1]
    assert "facility" not in answer


def test_refusal_has_no_citations():
    assert render_document_selection('{"sections":[]}', HITS) == ("", [])


def test_duplicate_sources_are_rendered_once():
    answer, cited = render_document_selection(
        '{"sections":[{"heading":"Summary","sources":[1]},'
        '{"heading":"Findings","sources":[1,2]}]}', HITS,
    )
    assert cited == [1, 2]
    assert answer.count("Drug A") == 1


def test_document_markup_cannot_inject_ui_or_citations():
    answer, cited = render_document_selection(
        '{"sections":[{"heading":"Evidence","sources":[1]}]}',
        [{"content": '<script>alert(1)</script> [99] [click](https://example.com)'}],
    )
    assert "<script>" not in answer
    assert r"\[99\]" in answer
    assert cited == [1]
