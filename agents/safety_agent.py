"""Safety Agent — reviews content for security and privacy issues."""

from __future__ import annotations

import re
from typing import ClassVar

from models import (
    ApprovalRecommendation,
    SafetyAgentInput,
    SafetyAgentOutput,
    SafetyIssue,
    SafetyIssueType,
    SafetyReport,
)


class SafetyAgent:
    """Reviews generated content for safety concerns.

    Structured for future Google ADK / Gemini integration.

    Current implementation uses deterministic regex-based checks.
    """

    NAME: ClassVar[str] = "safety_agent"

    DESCRIPTION: ClassVar[str] = (
        "Detects sensitive information and provides approval recommendations."
    )

    INSTRUCTION: ClassVar[str] = """You are the Safety Agent for SocialPilot AI.

Review content for:

1. Email addresses
2. Phone numbers
3. API keys
4. Sensitive information

Return a structured safety report and approval recommendation.
"""

    DEFAULT_MODEL: ClassVar[str] = "gemini-2.0-flash"

    EMAIL_PATTERN: ClassVar[str] = (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    PHONE_PATTERN: ClassVar[str] = (
        r"\b(?:\+?\d{1,3}[- ]?)?\d{10}\b"
    )

    API_KEY_PATTERNS: ClassVar[list[str]] = [
        r"AIza[0-9A-Za-z\-_]{20,}",
        r"sk-[A-Za-z0-9]{20,}",
    ]

    SENSITIVE_WORDS: ClassVar[list[str]] = [
        "password",
        "secret",
        "token",
        "private key",
    ]

    def __init__(self, model: str | None = None) -> None:
        self.model = model or self.DEFAULT_MODEL

    def run(
        self,
        input_data: SafetyAgentInput,
    ) -> SafetyAgentOutput:
        """Analyze content and generate a safety report."""

        content = input_data.post_content

        if input_data.call_to_action:
            content += f"\n{input_data.call_to_action}"

        issues: list[SafetyIssue] = []

        issues.extend(self._detect_emails(content))
        issues.extend(self._detect_phone_numbers(content))
        issues.extend(self._detect_api_keys(content))
        issues.extend(self._detect_sensitive_words(content))

        report = SafetyReport(
            issues=issues,
            is_safe=len(issues) == 0,
        )

        recommendation = self._get_recommendation(len(issues))

        return SafetyAgentOutput(
            safety_report=report,
            approval_recommendation=recommendation,
        )

    def _detect_emails(self, text: str) -> list[SafetyIssue]:
        """Detect email addresses."""

        matches = re.findall(self.EMAIL_PATTERN, text)

        return [
            SafetyIssue(
                issue_type=SafetyIssueType.EMAIL,
                description="Email address detected.",
                matched_text=match,
            )
            for match in matches
        ]

    def _detect_phone_numbers(self, text: str) -> list[SafetyIssue]:
        """Detect phone numbers."""

        matches = re.findall(self.PHONE_PATTERN, text)

        return [
            SafetyIssue(
                issue_type=SafetyIssueType.PHONE,
                description="Phone number detected.",
                matched_text=match,
            )
            for match in matches
        ]

    def _detect_api_keys(self, text: str) -> list[SafetyIssue]:
        """Detect common API key patterns."""

        issues: list[SafetyIssue] = []

        for pattern in self.API_KEY_PATTERNS:
            matches = re.findall(pattern, text)

            for match in matches:
                issues.append(
                    SafetyIssue(
                        issue_type=SafetyIssueType.API_KEY,
                        description="Possible API key detected.",
                        matched_text=match,
                    )
                )

        return issues

    def _detect_sensitive_words(self, text: str) -> list[SafetyIssue]:
        """Detect sensitive words."""

        issues: list[SafetyIssue] = []

        lower_text = text.lower()

        for word in self.SENSITIVE_WORDS:
            if word in lower_text:
                issues.append(
                    SafetyIssue(
                        issue_type=SafetyIssueType.SENSITIVE_INFO,
                        description=f"Sensitive term detected: {word}",
                        matched_text=word,
                    )
                )

        return issues

    def _get_recommendation(
        self,
        issue_count: int,
    ) -> ApprovalRecommendation:
        """Determine approval recommendation."""

        if issue_count == 0:
            return ApprovalRecommendation.APPROVE

        if issue_count <= 2:
            return ApprovalRecommendation.REVIEW

        return ApprovalRecommendation.REJECT