# ==========================================================
# TEMPORARY DEVELOPMENT MODE (GEMINI DISABLED)
#
# Reason:
# Gemini free-tier quota was getting exhausted (429 errors).
#
# To re-enable Gemini:
#
# 1. Uncomment:
#    import json
#    from prompts.trend_prompt import build_trend_prompt
#
# 2. Uncomment in __init__():
#    from utils.gemini_client import GeminiClient
#    self.gemini = GeminiClient()
#
# 3. Remove the "TEMPORARY DETERMINISTIC MODE" block
#    at the beginning of run().
#
# 4. That will reactivate the Gemini try/except logic inside run().
#
# Current Mode:
# Trend Agent  -> Deterministic
# Writer Agent -> Gemini
# ==========================================================
"""Trend Agent — researches hashtags, trends, and audience keywords."""

from __future__ import annotations
# import json # uncomment for gamini integration
import re


from typing import ClassVar
# from prompts.trend_prompt import build_trend_prompt # uncomment for gamini integration
from models import TrendAgentInput, TrendAgentOutput

# Short but meaningful tokens kept during topic analysis.
_SHORT_KEYWORDS: frozenset[str] = frozenset({"ai", "ml", "hr", "ux", "ui", "qa"})

# Common words stripped during topic analysis.
_STOP_WORDS: frozenset[str] = frozenset(
    {
        "a",
        "an",
        "and",
        "for",
        "i",
        "in",
        "is",
        "it",
        "just",
        "my",
        "of",
        "on",
        "or",
        "the",
        "this",
        "to",
        "today",
        "was",
        "we",
        "with",
        "launched",
        "built",
        "created",
        "released",
        "announced",
    }
)

# Platform-specific audience personas used to pad keyword lists deterministically.
_PLATFORM_AUDIENCE: dict[str, list[str]] = {
    "linkedin": [
        "hiring managers",
        "recruiters",
        "founders",
        "product managers",
        "software engineers",
    ],
    "twitter": [
        "tech community",
        "indie hackers",
        "developers",
        "startup founders",
        "content creators",
    ],
    "instagram": [
        "creators",
        "small business owners",
        "marketers",
        "entrepreneurs",
        "designers",
    ],
}

# Generic trend templates filled with extracted topic keywords.
_TREND_TEMPLATES: tuple[str, ...] = (
    "Growing interest in {keyword} tools",
    "How {keyword} is reshaping professional workflows",
    "Community conversations around {keyword} innovation",
)


class TrendAgent:
    """Researches social trends, hashtags, and audience keywords for a user topic.

    Structured for Google ADK / Gemini integration:
    - ``NAME`` and ``DESCRIPTION`` identify the agent in an orchestrator.
    - ``INSTRUCTION`` serves as the system prompt when wired to Gemini.
    - ``TrendAgentOutput`` is the structured response schema.

    Current implementation uses deterministic mock logic (no external API calls).
    """

    NAME: ClassVar[str] = "trend_agent"
    DESCRIPTION: ClassVar[str] = (
        "Analyzes a user topic and suggests hashtags, trending topics, "
        "and audience keywords for social media content."
    )
    INSTRUCTION: ClassVar[str] = """You are the Trend Agent for SocialPilot AI.

Analyze the user's topic and target platform, then produce:
1. Exactly 5 relevant hashtags (include the # prefix).
2. Exactly 3 trending topics related to the announcement.
3. Exactly 5 audience keywords describing who would engage with the content.

Return structured JSON matching the TrendAgentOutput schema."""

    # Default Gemini model — used when this agent is connected to the API later.
    DEFAULT_MODEL: ClassVar[str] = "gemini-2.0-flash"

    def __init__(self, model: str | None = None) -> None:
        """Initialize the agent.

        Args:
            model: Optional Gemini model name for future API integration.
        """
        self.model = model or self.DEFAULT_MODEL
        # from utils.gemini_client import GeminiClient # uncomment for gamini integration
        # self.gemini = GeminiClient() # uncomment for gamini integration
       

    def run(self, input_data: TrendAgentInput) -> TrendAgentOutput:

        # ==========================================
        # TEMPORARY DETERMINISTIC MODE
        # Re-enable Gemini later if needed.
        # ==========================================

        topic_keywords = self._extract_topic_keywords(
            input_data.user_topic
        )

        platform = input_data.platform.lower()

        hashtags = self._generate_hashtags(
            topic_keywords,
            platform,
        )

        trends = self._generate_trends(
            topic_keywords,
        )

        audience_keywords = self._generate_audience_keywords(
            topic_keywords,
            platform,
        )

        return TrendAgentOutput(
            hashtags=hashtags,
            trends=trends,
            audience_keywords=audience_keywords,
        )
        # ==========================================
        # GEMINI VERSION (DISABLED FOR NOW)
        # ==========================================

        """Analyze a user topic and return trend research results.

        Args:
            input_data: The user's topic and target platform.

        Returns:
            Hashtags, trending topics, and audience keywords derived from the topic.
        """
       
        try:

            prompt = build_trend_prompt(input_data)
            response = self.gemini.generate(prompt)

            # Strip markdown code block formatting if present
            cleaned = response.strip()
            if cleaned.startswith("```"):
                import re
                match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
                if match:
                    cleaned = match.group(1)
            response = cleaned

            data = json.loads(response)
            required_keys = [
                "hashtags",
                "trends",
                "audience_keywords",
            ]

            for key in required_keys:
                if key not in data:
                    raise ValueError(
                        f"Missing key in Gemini response: {key}"
                    )

            return TrendAgentOutput(
                hashtags=data["hashtags"],
                trends=data["trends"],
                audience_keywords=data["audience_keywords"],
            )

        except Exception as e:
            print(f"Gemini error: {e}")

            # Fall back to existing deterministic methods
            topic_keywords = self._extract_topic_keywords(input_data.user_topic)
            platform = input_data.platform.lower()

            hashtags = self._generate_hashtags(topic_keywords, platform)
            trends = self._generate_trends(topic_keywords)
            audience_keywords = self._generate_audience_keywords(topic_keywords, platform)

            return TrendAgentOutput(
                hashtags=hashtags,
                trends=trends,
                audience_keywords=audience_keywords,
            )

    def _extract_topic_keywords(self, user_topic: str) -> list[str]:
        """Pull distinct, meaningful words from the user's topic sentence."""
        raw_tokens = re.findall(r"[A-Za-z]+", user_topic.lower())
        keywords = [
            token
            for token in raw_tokens
            if token not in _STOP_WORDS
            and (len(token) > 2 or token in _SHORT_KEYWORDS)
        ]

        # Fall back to a generic token so downstream generators always have input.
        if not keywords:
            keywords = ["social", "content"]

        # Preserve order while removing duplicates.
        return list(dict.fromkeys(keywords))

    def _generate_hashtags(self, topic_keywords: list[str], platform: str) -> list[str]:
        """Create 5 deterministic hashtags from topic keywords and platform."""
        hashtags: list[str] = []

        for keyword in topic_keywords:
            if len(hashtags) >= 5:
                break
            hashtags.append(self._to_hashtag(keyword))

        # Pad with platform- and topic-aware defaults to always reach 5.
        platform_tag = self._to_hashtag(platform)
        filler_tags = [
            platform_tag,
            "#BuildInPublic",
            "#TechLaunch",
            "#Innovation",
            "#ProductUpdate",
        ]

        for tag in filler_tags:
            if len(hashtags) >= 5:
                break
            if tag not in hashtags:
                hashtags.append(tag)

        return hashtags[:5]

    def _generate_trends(self, topic_keywords: list[str]) -> list[str]:
        """Create 3 deterministic trending topics from extracted keywords."""
        primary = topic_keywords[0]
        secondary = topic_keywords[1] if len(topic_keywords) > 1 else primary

        trends = [
            _TREND_TEMPLATES[0].format(keyword=primary),
            _TREND_TEMPLATES[1].format(keyword=secondary),
            _TREND_TEMPLATES[2].format(keyword=primary),
        ]

        return trends[:3]

    def _generate_audience_keywords(
        self,
        topic_keywords: list[str],
        platform: str,
    ) -> list[str]:
        """Create 5 deterministic audience keywords from topic and platform."""
        audience: list[str] = []

        # Topic-derived personas (e.g. "resume" -> "job seekers").
        topic_personas = {
            "ai": "AI enthusiasts",
            "resume": "job seekers",
            "analyzer": "career coaches",
            "project": "builders",
            "launch": "early adopters",
            "startup": "founders",
            "product": "product leaders",
        }

        for keyword in topic_keywords:
            persona = topic_personas.get(keyword)
            if persona and persona not in audience:
                audience.append(persona)
            if len(audience) >= 5:
                return audience[:5]

        # Fill remaining slots from platform defaults.
        for persona in _PLATFORM_AUDIENCE.get(platform, _PLATFORM_AUDIENCE["linkedin"]):
            if len(audience) >= 5:
                break
            if persona not in audience:
                audience.append(persona)

        return audience[:5]

    @staticmethod
    def _to_hashtag(keyword: str) -> str:
        """Convert a keyword into a PascalCase hashtag."""
        if keyword in _SHORT_KEYWORDS:
            return "#" + keyword.upper()

        parts = re.findall(r"[A-Za-z0-9]+", keyword)
        if not parts:
            return "#Social"
        return "#" + "".join(part.capitalize() for part in parts)
