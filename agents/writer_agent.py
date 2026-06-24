"""Writer Agent — generates professional social media content."""

from __future__ import annotations

from typing import ClassVar

from models import WriterAgentInput, WriterAgentOutput


class WriterAgent:
    """Generates platform-specific social media content.

    Structured for future Google ADK / Gemini integration.

    Current implementation uses deterministic mock logic.
    """

    NAME: ClassVar[str] = "writer_agent"

    DESCRIPTION: ClassVar[str] = (
        "Creates professional social media posts from trend research."
    )

    INSTRUCTION: ClassVar[str] = """You are the Writer Agent for SocialPilot AI.

Your responsibilities:

1. Create engaging social media content.
2. Write a strong opening hook.
3. Highlight the user's achievement or announcement.
4. Include a call-to-action.
5. Use hashtags naturally.

Return content matching the WriterAgentOutput schema.
"""

    DEFAULT_MODEL: ClassVar[str] = "gemini-2.0-flash"

    def __init__(self, model: str | None = None) -> None:
        self.model = model or self.DEFAULT_MODEL

    def run(self, input_data: WriterAgentInput) -> WriterAgentOutput:
        """Generate a social media post.

        Args:
            input_data: Topic, hashtags, trends, and audience keywords.

        Returns:
            WriterAgentOutput
        """

        platform = input_data.platform.lower()

        if platform == "linkedin":
            post = self._generate_linkedin_post(input_data)
        else:
            post = self._generate_generic_post(input_data)

        call_to_action = self._generate_cta(input_data)

        return WriterAgentOutput(
            post_content=post,
            call_to_action=call_to_action,
        )

    def _generate_linkedin_post(
        self,
        input_data: WriterAgentInput,
    ) -> str:
        """Generate a LinkedIn-style professional post."""

        topic = input_data.user_topic

        hashtags = " ".join(input_data.hashtags[:5])

        trend_line = ""
        if input_data.trends:
            trend_line = (
                f"\nThis aligns with growing interest in "
                f"{input_data.trends[0].lower()}."
            )

        post = f"""
🚀 Excited to share an update!

{topic}

Over the past few weeks, I've been working on this project and learning a lot throughout the process.

{trend_line}

Building in public has been an incredible experience, and I'm excited to continue improving and sharing my journey.

{hashtags}
""".strip()

        return post

    def _generate_generic_post(
        self,
        input_data: WriterAgentInput,
    ) -> str:
        """Fallback content for unsupported platforms."""

        hashtags = " ".join(input_data.hashtags[:5])

        return (
            f"🚀 {input_data.user_topic}\n\n"
            f"Excited to share this update with everyone.\n\n"
            f"{hashtags}"
        )

    def _generate_cta(
        self,
        input_data: WriterAgentInput,
    ) -> str:
        """Generate a simple call-to-action."""

        if input_data.audience_keywords:
            audience = input_data.audience_keywords[0]
            return (
                f"I'd love feedback from {audience}. "
                f"What do you think?"
            )

        return (
            "I'd love to hear your thoughts and feedback "
            "in the comments."
        )