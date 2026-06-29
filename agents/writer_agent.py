from __future__ import annotations

import json
from typing import ClassVar

from models import WriterAgentInput, WriterAgentOutput
from prompts.writer_prompt import build_writer_prompt
from utils.gemini_client import GeminiClient


class WriterAgent:
    """Generates platform-specific social media content."""

    NAME: ClassVar[str] = "writer_agent"

    DESCRIPTION: ClassVar[str] = (
        "Creates professional social media posts from trend research."
    )

    DEFAULT_MODEL: ClassVar[str] = "gemini-2.0-flash"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or self.DEFAULT_MODEL
        self.gemini = GeminiClient()

    def run(
        self,
        input_data: WriterAgentInput,
    ) -> WriterAgentOutput:

        try:
            prompt = build_writer_prompt(input_data)

            # remove it later after development
            try:
                print("*" * 60)
                print("*" * 60)
                print(prompt)
                print("*" * 60)
                print("*" * 60)
            except Exception:
                pass
            # until here

            generated_content = self.gemini.generate(prompt)
            if not generated_content:
                raise ValueError("Gemini returned empty response.")

            # Parse JSON
            clean_content = generated_content.strip()
            if clean_content.startswith("```json"):
                clean_content = clean_content[7:]
            elif clean_content.startswith("```"):
                clean_content = clean_content[3:]
            if clean_content.endswith("```"):
                clean_content = clean_content[:-3]
            clean_content = clean_content.strip()

            data = json.loads(clean_content)
            version_a = data["version_a"]
            version_b = data["version_b"]
            version_c = data["version_c"]

            variations = [version_a, version_b, version_c]
            post_content = version_a

        except Exception as e:

            print(f"Gemini Error: {e}")
            platform = input_data.platform.lower()

            if platform == "linkedin":
                generated_content = self._generate_linkedin_post(input_data)

            elif platform == "x":
                generated_content = self._generate_x_post(input_data)

            elif platform == "instagram":
                generated_content = self._generate_instagram_post(input_data)

            elif platform == "youtube":
                generated_content = self._generate_youtube_content(input_data)

            else:
                generated_content = self._generate_generic_post(input_data)

            post_content = generated_content
            variations = [
                post_content,
                post_content,
                post_content,
            ]

        return WriterAgentOutput(
            post_content=post_content,
            variations=variations,
            call_to_action=self._generate_cta(input_data),
        )

    def _generate_linkedin_post(
        self,
        input_data: WriterAgentInput,
    ) -> str:

        hashtags = " ".join(input_data.hashtags[:5])

        return f"""
🚀 Excited to share an update!

{input_data.user_topic}

Building in public has been an incredible experience.

{hashtags}
""".strip()

    def _generate_x_post(
        self,
        input_data: WriterAgentInput,
    ) -> str:

        hashtags = " ".join(input_data.hashtags[:3])

        return (
            f"🚀 {input_data.user_topic}\n\n"
            f"AI and automation are changing how we work.\n\n"
            f"{hashtags}"
        )

    def _generate_instagram_post(
        self,
        input_data: WriterAgentInput,
    ) -> str:

        hashtags = " ".join(input_data.hashtags[:5])

        return (
            f"🚀 Big Update!\n\n"
            f"{input_data.user_topic}\n\n"
            f"✨ Learning\n"
            f"🔥 Building\n"
            f"💡 Growing\n\n"
            f"{hashtags}"
        )

    def _generate_youtube_content(
        self,
        input_data: WriterAgentInput,
    ) -> str:

        hashtags = " ".join(input_data.hashtags[:5])

        return f"""
🎬 VIDEO TITLE

{input_data.user_topic}: What You Need To Know

📄 DESCRIPTION

In this video we explore:

• Key insights
• Latest trends
• Practical takeaways

🏷️ HASHTAGS

{hashtags}
""".strip()

    def _generate_generic_post(
        self,
        input_data: WriterAgentInput,
    ) -> str:

        hashtags = " ".join(input_data.hashtags[:5])

        return (
            f"🚀 {input_data.user_topic}\n\n"
            f"Excited to share this update.\n\n"
            f"{hashtags}"
        )

    def _generate_cta(
        self,
        input_data: WriterAgentInput,
    ) -> str:

        if input_data.audience_keywords:
            return (
                f"I'd love feedback from "
                f"{input_data.audience_keywords[0]}."
            )

        return "I'd love to hear your thoughts."