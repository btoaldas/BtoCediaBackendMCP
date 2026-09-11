"""Transactional sliding-window conversation and a bounded rate-limit experiment."""

from __future__ import annotations

import argparse
import json
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path

from gemini_client import GeminiGateway, MODEL, Reply

MAX_TURNS = 10
PROMPTS = [
    "En este ejemplo ficticio me llamo Alex y mi color favorito es el verde.",
    "¿Qué es un framework de Python?",
    "Dame un ejemplo de dato que no cabe en un int.",
    "¿Qué hace el comando uv init?",
    "Explica en una frase qué es un token.",
    "¿Qué significa que una API sea stateless?",
    "¿Para qué sirve un archivo .env?",
    "¿Cómo me llamo y cuál es mi color favorito?",
]


class Conversation:
    def __init__(self, gateway=None, *, max_turns: int = MAX_TURNS):
        if max_turns < 1:
            raise ValueError("max_turns must be at least one")
        self.gateway = gateway if gateway is not None else GeminiGateway()
        self.max_turns = max_turns
        self.history: list[dict] = []

    def send(self, message: str) -> Reply:
        if not isinstance(message, str) or not message.strip():
            raise ValueError("message must be a nonempty string")
        keep = (self.max_turns - 1) * 2
        previous = self.history[-keep:] if keep else []
        request = previous + [{"role": "user", "parts": [{"text": message}]}]
        result = self.gateway.generate(request)
        if result.ok:
            self.history = request + [{"role": "model", "parts": [{"text": result.text}]}]
        return result


def memory_demo(output: str | None = None) -> bool:
    """Return request completion; semantic recall requires reading the transcript.

    Reserve a new output file before constructing the provider. Exclusive creation
    prevents both accidental replacement and a check/open race. An interrupted
    run can leave an empty reserved file; it is preserved, never silently removed.
    """
    destination = Path(output).open("x", encoding="utf-8") if output else nullcontext(None)
    with destination as stream:
        conversation = Conversation()
        turns = []
        print(f"REAL_PROVIDER model={MODEL} time={datetime.now(timezone.utc).isoformat()}")
        for index, prompt in enumerate(PROMPTS, 1):
            print(f"\nTURNO {index} USER: {prompt}")
            result = conversation.send(prompt)
            print(f"TURNO {index} BOT: {result.text}")
            turns.append({"turn": index, "user": prompt, "model": result.text,
                          "ok": result.ok, "total_tokens": result.total_tokens,
                          "finish_reason": result.finish_reason})
            if not result.ok:
                print("MEMORY_RUN_INCOMPLETE: provider request failed; no success is claimed.")
                break
        last = turns[-1]["model"].lower()
        completed = len(turns) == len(PROMPTS) and all(t["ok"] for t in turns)
        lexical_match = "alex" in last and "verde" in last
        print(f"MEMORY_RUN_COMPLETE={completed} history_entries={len(conversation.history)}")
        print(f"MEMORY_LEXICAL_MATCH={lexical_match} SEMANTIC_REVIEW_REQUIRED=True")
        if stream:
            json.dump({"provider": "Gemini", "model": MODEL,
                "time_utc": datetime.now(timezone.utc).isoformat(),
                "run_completed": completed, "lexical_match": lexical_match,
                "semantic_review_required": True, "turns": turns},
                stream, ensure_ascii=False, indent=2)
        return completed


def rate_limit_demo() -> bool:
    """Follow the guide's twenty sequential count requests with conversation history."""
    observed_429 = False

    def observe_log(message: str) -> None:
        nonlocal observed_429
        if message.startswith("[429 "):
            observed_429 = True
        print(message)

    conversation = Conversation(GeminiGateway(log=observe_log))
    print(f"REAL_PROVIDER_RATE_LIMIT model={MODEL} maximum_logical_requests=20 protocol=guide_count_with_history time={datetime.now(timezone.utc).isoformat()}")
    for number in range(1, 21):
        print(f"REQUEST {number}")
        result = conversation.send(f"Cuenta hasta {number}.")
        print(result.text)
        if observed_429:
            print(f"RATE_LIMIT_OBSERVED=True PROCESS_SURVIVED=True LAST_REQUEST_OK={result.ok}")
            return True
        if not result.ok:
            print("RATE_LIMIT_OBSERVED=False DIFFERENT_ERROR=True")
            return False
    print("RATE_LIMIT_OBSERVED=False: no 429 occurred within the bounded experiment.")
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["memory", "rate-limit"], default="memory")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    if args.mode == "memory":
        raise SystemExit(0 if memory_demo(args.json_output) else 2)
    raise SystemExit(0 if rate_limit_demo() else 2)


if __name__ == "__main__":
    main()
