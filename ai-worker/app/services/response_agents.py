"""Request-scoped response agents; routing requires no additional model call."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ResponseAgent:
    name: str
    instructions: str
    context_limit: int


CLINICAL_AGENT = ResponseAgent(
    name="clinical",
    instructions=(
        "Select document passages that directly answer the clinical question. "
        "Use the Answer heading. Do not select a passage solely because it mentions the topic."
    ),
    context_limit=3,
)
WRITING_AGENT = ResponseAgent(
    name="writing",
    instructions=(
        "Select and organize document passages for the requested draft. Use the Draft heading. "
        "Prefer passages suited to the requested audience and language when available. "
        "Strict document mode preserves the source wording; do not paraphrase or translate it. "
        "Do not include user-provided facts or patient details absent from the retrieved context."
    ),
    context_limit=6,
)
REPORT_AGENT = ResponseAgent(
    name="report",
    instructions=(
        "Organize document passages into a report using Summary, Findings, and Recommendations. "
        "Select only sections supported by the retrieved context; do not fill evidence gaps. "
        "Never present guideline recommendations as observed facility outcomes. "
        "If the request needs counts, dates, trends, or patient details absent from the documents, "
        "return an empty selection rather than inventing them."
    ),
    context_limit=6,
)

_ACTION = re.compile(
    r"\b(write|draft|compose|prepare|create|generate|produce|make|build|"
    r"format|turn|convert|give me|provide|need|want|rewrite|revise|edit)\b", re.I
)
_ARTIFACT = re.compile(
    r"\b(?P<report>report|briefing|situation report|sitrep)\b|"
    r"\b(?P<writing>email|letter|message|handout|leaflet|article|"
    r"summary|script|announcement|notice|patient information)\b", re.I
)
_REWRITE = re.compile(r"\b(rewrite|rephrase|edit|proofread|summari[sz]e|translate)\b", re.I)
_WRITE = re.compile(r"\b(write|draft|compose)\b", re.I)
_REVISION = re.compile(
    r"^\s*(?:(?:please|can you|could you)\s+)*(?:"
    r"make\s+(?:it|this|that|the\s+(?:draft|report|text|summary))\b|"
    r"(?:shorten|expand|simplify|revise|rewrite|rephrase|edit|proofread|translate)\b|"
    r"add\b|remove\b)", re.I
)


def _explicit_agent(question: str) -> ResponseAgent | None:
    action = _ACTION.search(question)
    # The first requested artifact wins: an email about a report is an email.
    artifact = _ARTIFACT.search(question, action.end() if action else 0)
    if artifact and (
        (action and artifact.start() - action.end() <= 80)
        or not question[:artifact.start()].strip()
    ):
        return REPORT_AGENT if artifact.group("report") else WRITING_AGENT
    return None


def select_response_agent(question: str, recent_messages: list[dict]) -> ResponseAgent:
    explicit = _explicit_agent(question)
    if explicit:
        return explicit
    # Only revisions inherit the previous user's requested output type. A new
    # clinical question must not remain stuck in a previous report workflow.
    if _REVISION.search(question):
        for message in reversed(recent_messages[-6:]):
            if str(message.get("role", "")).lower() != "user":
                continue
            previous = str(message.get("content") or "")
            agent = _explicit_agent(previous)
            if agent:
                return agent
            if _REWRITE.search(previous):
                return WRITING_AGENT
            if not _REVISION.search(previous):
                break
        return WRITING_AGENT
    if _REWRITE.search(question) or _WRITE.search(question):
        return WRITING_AGENT
    return CLINICAL_AGENT


def is_revision_request(question: str) -> bool:
    return bool(_REVISION.search(question))
