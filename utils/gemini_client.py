from __future__ import annotations

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:
    """Simple Gemini API client."""

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file."
            )

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """Generate text using Gemini."""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text