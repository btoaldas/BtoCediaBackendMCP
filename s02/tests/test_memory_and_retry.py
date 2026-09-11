"""Deterministic boundary tests; fake responses are not provider evidence."""

from copy import deepcopy
import json
from types import SimpleNamespace

import pytest
from google.genai import errors

from conversation import Conversation
import conversation
from gemini_client import GeminiGateway


def response(text="OK", finish="STOP"):
    return SimpleNamespace(text=text, candidates=[SimpleNamespace(finish_reason=finish)],
                           usage_metadata=SimpleNamespace(prompt_token_count=4,
                               candidates_token_count=2, total_token_count=6))


def error(cls, code):
    return cls(code, {"error": {"code": code, "message": "synthetic test error"}})


class Models:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(deepcopy(kwargs))
        item = next(self.outcomes)
        if isinstance(item, Exception):
            raise item
        return item

    def count_tokens(self, **kwargs):
        return SimpleNamespace(total_tokens=16)


def gateway(outcomes):
    models = Models(outcomes)
    waits, logs = [], []
    instance = GeminiGateway(SimpleNamespace(models=models), sleep=waits.append, log=logs.append)
    return instance, models, waits, logs


def test_eight_turns_include_initial_fact_and_alternate_roles():
    g, models, _, _ = gateway([response() for _ in range(8)])
    chat = Conversation(g)
    for i in range(8):
        assert chat.send("initial fact" if i == 0 else f"turn {i}").ok
    assert len(models.calls[-1]["contents"]) == 15
    assert models.calls[-1]["contents"][0]["parts"][0]["text"] == "initial fact"
    assert [x["role"] for x in chat.history] == ["user", "model"] * 8


def test_window_preserves_complete_pairs_and_is_bounded():
    g, models, _, _ = gateway([response() for _ in range(12)])
    chat = Conversation(g, max_turns=10)
    for i in range(12):
        chat.send(str(i))
    assert len(chat.history) == 20
    assert chat.history[0]["parts"][0]["text"] == "2"
    assert all(len(call["contents"]) <= 19 for call in models.calls)


def test_one_turn_window_drops_all_previous_pairs():
    g, models, _, _ = gateway([response(), response()])
    chat = Conversation(g, max_turns=1)
    chat.send("first")
    chat.send("second")
    assert len(models.calls[-1]["contents"]) == 1
    assert len(chat.history) == 2


@pytest.mark.parametrize("value", [0, -1])
def test_invalid_window_rejected(value):
    with pytest.raises(ValueError):
        Conversation(object(), max_turns=value)


@pytest.mark.parametrize("value", ["", "  ", None, 42])
def test_invalid_message_does_not_call_provider(value):
    g, models, _, _ = gateway([])
    chat = Conversation(g)
    with pytest.raises(ValueError):
        chat.send(value)
    assert models.calls == []
    assert chat.history == []


def test_429_retries_same_request_without_duplicate_user():
    g, models, waits, logs = gateway([error(errors.ClientError, 429), response()])
    chat = Conversation(g)
    result = chat.send("one user message")
    assert result.ok and result.attempts == 2
    assert waits == [1]
    assert models.calls[0]["contents"] == models.calls[1]["contents"]
    assert len(chat.history) == 2
    assert "RESOURCE_EXHAUSTED" in logs[0]


def test_429_exhaustion_is_bounded_and_preserves_prior_history():
    g, models, waits, _ = gateway([response()] + [error(errors.ClientError, 429) for _ in range(4)])
    chat = Conversation(g, max_turns=1)
    chat.send("keep this")
    before = deepcopy(chat.history)
    result = chat.send("will fail")
    assert not result.ok and result.error_code == 429
    assert result.attempts == 4 and waits == [1, 2, 4]
    assert len(models.calls) == 5
    assert chat.history == before


@pytest.mark.parametrize("code", [400, 401, 403])
def test_other_client_errors_never_retry(code):
    g, models, waits, _ = gateway([error(errors.ClientError, code)])
    result = Conversation(g).send("bad request")
    assert not result.ok and result.error_code == code
    assert len(models.calls) == 1 and waits == []


def test_server_error_recovery_has_exponential_backoff():
    g, _, waits, _ = gateway([error(errors.ServerError, 503), error(errors.ServerError, 500), response()])
    assert Conversation(g).send("hello").ok
    assert waits == [1, 2]


def test_server_error_exhaustion_does_not_add_failed_turn():
    g, _, waits, _ = gateway([error(errors.ServerError, 503) for _ in range(4)])
    chat = Conversation(g)
    result = chat.send("hello")
    assert not result.ok and result.attempts == 4
    assert chat.history == [] and waits == [1, 2, 4]


def test_truncation_warning_and_usage_are_visible():
    g, _, _, logs = gateway([response("partial", "MAX_TOKENS")])
    result = g.ask("hello")
    assert result.total_tokens == 6
    assert any("total_token_count=6" in line for line in logs)
    assert any("truncada" in line for line in logs)


def test_empty_candidate_does_not_corrupt_history():
    g, _, _, _ = gateway([SimpleNamespace(text=None, candidates=[], usage_metadata=None)])
    chat = Conversation(g)
    result = chat.send("hello")
    assert not result.ok and result.finish_reason == "NO_CANDIDATES"
    assert chat.history == []


def test_explicit_config_and_token_budget():
    g, models, _, logs = gateway([response()])
    g.ask("hello")
    config = models.calls[0]["config"]
    assert config.system_instruction and config.temperature == 0.7
    assert config.max_output_tokens == 200
    assert g.count_tokens([]) == 16
    assert any("CONTEXT tokens=16" in line for line in logs)


def test_rate_limit_demo_detects_provider_429_even_when_retry_recovers(monkeypatch):
    g, models, waits, _ = gateway([error(errors.ClientError, 429), response()])

    def configured_gateway(**kwargs):
        g.log = kwargs["log"]
        return g

    monkeypatch.setattr(conversation, "GeminiGateway", configured_gateway)
    assert conversation.rate_limit_demo() is True
    assert len(models.calls) == 2 and waits == [1]
    assert models.calls[0]["contents"] == models.calls[1]["contents"]


def test_existing_evidence_is_preserved_before_provider_creation(tmp_path, monkeypatch):
    destination = tmp_path / "original.json"
    destination.write_text("original evidence", encoding="utf-8")
    monkeypatch.setattr(conversation, "Conversation", lambda: pytest.fail("provider must not be created"))
    with pytest.raises(FileExistsError):
        conversation.memory_demo(str(destination))
    assert destination.read_text(encoding="utf-8") == "original evidence"


def test_invalid_output_parent_fails_before_provider_creation(tmp_path, monkeypatch):
    monkeypatch.setattr(conversation, "Conversation", lambda: pytest.fail("provider must not be created"))
    with pytest.raises(FileNotFoundError):
        conversation.memory_demo(str(tmp_path / "missing" / "run.json"))


def test_lexical_match_is_not_claimed_as_semantic_recall(tmp_path, monkeypatch, capsys):
    ambiguous = "No recuerdo tu nombre ni tu color. Alex y verde serían una suposición."
    g, _, _, _ = gateway([response() for _ in range(7)] + [response(ambiguous)])
    monkeypatch.setattr(conversation, "GeminiGateway", lambda: g)
    destination = tmp_path / "run.json"
    assert conversation.memory_demo(str(destination)) is True
    data = json.loads(destination.read_text(encoding="utf-8"))
    assert data["run_completed"] and data["lexical_match"]
    assert data["semantic_review_required"] is True
    assert "passed" not in data
    assert "MEMORY_RECALL_PASS" not in capsys.readouterr().out


def test_incomplete_memory_run_is_saved_without_success(tmp_path, monkeypatch):
    g, models, _, _ = gateway([error(errors.ClientError, 403)])
    monkeypatch.setattr(conversation, "GeminiGateway", lambda: g)
    destination = tmp_path / "failed.json"
    assert conversation.memory_demo(str(destination)) is False
    data = json.loads(destination.read_text(encoding="utf-8"))
    assert data["run_completed"] is False and len(data["turns"]) == 1
    assert len(models.calls) == 1
