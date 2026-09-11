"""Explicit Gemini requests with token accounting and bounded retry policy."""

from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass
from typing import Callable

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

MODEL = "gemini-2.5-flash"
CONTEXT_WINDOW_LIMIT = 1_048_576
SYSTEM_INSTRUCTION = (
    "Eres un instructor de programación. Responde en español y máximo tres frases. "
    "No inventes información que no figure en la conversación."
)


@dataclass(frozen=True)
class Reply:
    text: str
    finish_reason: str
    total_tokens: int
    ok: bool
    attempts: int
    error_code: int | None = None


def make_client():
    """Read an existing environment credential without writing or printing it."""
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is required; its value must stay outside Git.")
    return genai.Client(api_key=key, vertexai=False)


class GeminiGateway:
    """Keep provider calls, logging, and retry policy outside conversation state."""

    def __init__(self, client=None, *, sleep: Callable = time.sleep, log: Callable = print,
                 max_retries: int = 3, temperature: float = 0.7,
                 max_output_tokens: int = 200):
        self.client = client if client is not None else make_client()
        self.sleep = sleep
        self.log = log
        self.max_retries = max_retries
        self.config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )

    def count_tokens(self, contents: list[dict]) -> int:
        """Measure the input with the provider before generating a response."""
        counted = self.client.models.count_tokens(model=MODEL, contents=contents)
        total = counted.total_tokens or 0
        self.log(f"CONTEXT tokens={total} ratio={total / CONTEXT_WINDOW_LIMIT:.6%}")
        return total

    def generate(self, contents: list[dict]) -> Reply:
        for retry in range(self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=MODEL, contents=contents, config=self.config
                )
            except errors.ClientError as exc:
                if exc.code == 429 and retry < self.max_retries:
                    wait = 2 ** retry
                    self.log(f"[429 RESOURCE_EXHAUSTED] Reintentando en {wait}s...")
                    self.sleep(wait)
                    continue
                label = "RESOURCE_EXHAUSTED" if exc.code == 429 else "CLIENT_ERROR"
                self.log(f"[{exc.code} {label}] Fin controlado; intentos={retry + 1}.")
                return Reply("Solicitud no completada; historial conservado.", label, 0,
                             False, retry + 1, exc.code)
            except errors.ServerError as exc:
                if retry < self.max_retries:
                    wait = 2 ** retry
                    self.log(f"[{exc.code} SERVER_ERROR] Reintentando en {wait}s...")
                    self.sleep(wait)
                    continue
                self.log(f"[{exc.code} SERVER_ERROR] Fin controlado; intentos={retry + 1}.")
                return Reply("Servicio no disponible; historial conservado.", "SERVER_ERROR",
                             0, False, retry + 1, exc.code)
            candidates = response.candidates or []
            finish = str(candidates[0].finish_reason) if candidates else "NO_CANDIDATES"
            usage = response.usage_metadata
            total = (usage.total_token_count or 0) if usage else 0
            prompt = (usage.prompt_token_count or 0) if usage else 0
            output = (usage.candidates_token_count or 0) if usage else 0
            self.log(f"USAGE prompt={prompt} output={output} total_token_count={total} finish={finish}")
            if "MAX_TOKENS" in finish:
                self.log("[warning] Respuesta truncada por max_output_tokens.")
            text = response.text or ""
            return Reply(text, finish, total, bool(text), retry + 1)
        raise AssertionError("Retry loop must return a result")

    def ask(self, prompt: str) -> Reply:
        return self.generate([{"role": "user", "parts": [{"text": prompt}]}])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["minimal", "forgetting", "temperature"], default="minimal")
    args = parser.parse_args()
    if args.mode == "temperature":
        for value in [0.1, 1.3]:
            print(f"TEMPERATURE={value}")
            print(GeminiGateway(temperature=value).ask("¿Qué opinas de var en JS?").text)
        return
    gateway = GeminiGateway()
    if args.mode == "forgetting":
        for prompt in ["En este ejemplo ficticio me llamo Valeria.", "¿Cómo me llamo?"]:
            print("USER:", prompt)
            print("BOT:", gateway.ask(prompt).text)
    else:
        prompt = "¿Qué es una API?"
        gateway.count_tokens([{"role": "user", "parts": [{"text": prompt}]}])
        print(gateway.ask(prompt).text)


if __name__ == "__main__":
    main()
