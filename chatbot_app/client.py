"""API layer: the only module that talks to Groq. Converts errors to friendly ones."""
from __future__ import annotations

import logging

import groq
from groq import Groq

from .config import Settings

log = logging.getLogger(__name__)


class ChatError(Exception):
    """An error whose message is safe to show to the user."""


class ChatClient:
    def __init__(self, settings: Settings):
        self._settings = settings
        # The SDK retries network errors, 429 and 5xx automatically (max_retries).
        self._client = Groq(
            api_key=settings.api_key,
            timeout=settings.timeout,
            max_retries=settings.max_retries,
        )

    def complete(self, messages: list[dict]) -> str:
        s = self._settings
        try:
            response = self._client.chat.completions.create(
                model=s.model,
                messages=messages,
                temperature=s.temperature,
                max_tokens=s.max_tokens,
            )
        except groq.AuthenticationError:
            raise ChatError("Invalid API key. Check GROQ_API_KEY in your .env file.")
        except groq.NotFoundError:
            raise ChatError(
                f"Model '{s.model}' was not found or is retired. "
                "Set a current model with MODEL=... in .env "
                "(see https://console.groq.com/docs/models)."
            )
        except groq.RateLimitError:
            raise ChatError("Rate limit reached. Please wait a moment and try again.")
        except groq.APITimeoutError:
            raise ChatError("The request timed out. Please try again.")
        except groq.APIConnectionError:
            raise ChatError("Could not connect to the API. Check your internet connection.")
        except groq.BadRequestError as exc:
            log.error("Bad request: %s", exc)
            raise ChatError("The API rejected the request. See chatbot.log for details.")
        except groq.APIStatusError as exc:
            log.error("API status error %s: %s", exc.status_code, exc)
            raise ChatError(f"The API returned an error (status {exc.status_code}).")

        text = (response.choices[0].message.content or "").strip()
        if not text:
            raise ChatError("The model returned an empty response. Please try again.")
        return text
