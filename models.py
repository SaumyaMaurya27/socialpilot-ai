from __future__ import annotations

from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field


class ApprovalRecommendation(str, Enum):
    APPROVE = "approve"
    REVIEW = "review"
    REJECT = "reject"


class SafetyIssueType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    API_KEY = "api_key"
    SENSITIVE_INFO = "sensitive_info"


class SafetyIssue(BaseModel):
    issue_type: SafetyIssueType
    description: str
    matched_text: Optional[str] = None


class SafetyReport(BaseModel):
    issues: list[SafetyIssue] = Field(default_factory=list)
    is_safe: bool = True


class TrendAgentInput(BaseModel):
    user_topic: str = Field(
        ...,
        description="The user's topic or announcement.",
    )
    platform: str = Field(
        default="linkedin",
        description="Target social platform for trend research.",
    )


class TrendAgentOutput(BaseModel):
    hashtags: list[str] = Field(
        default_factory=list,
        description="Suggested hashtags for the post.",
    )
    trends: list[str] = Field(
        default_factory=list,
        description="Relevant trending topics.",
    )
    audience_keywords: list[str] = Field(
        default_factory=list,
        description="Keywords that resonate with the target audience.",
    )


class WriterAgentInput(BaseModel):
    user_topic: str = Field(
        ...,
        description="The original user topic or announcement.",
    )
    hashtags: list[str] = Field(
        default_factory=list,
        description="Hashtags from the Trend Agent.",
    )
    trends: list[str] = Field(
        default_factory=list,
        description="Trending topics from the Trend Agent.",
    )
    audience_keywords: list[str] = Field(
        default_factory=list,
        description="Audience keywords from the Trend Agent.",
    )
    platform: str = Field(
        default="linkedin",
        description="Target platform for the generated post.",
    )


class WriterAgentOutput(BaseModel):
    post_content: str = Field(
        ...,
        description="The generated social media post body.",
    )
    call_to_action: str = Field(
        ...,
        description="Suggested call-to-action for the post.",
    )


class SafetyAgentInput(BaseModel):
    post_content: str = Field(
        ...,
        description="Post content to review for safety issues.",
    )
    call_to_action: Optional[str] = Field(
        default=None,
        description="Optional call-to-action text to include in the review.",
    )


class SafetyAgentOutput(BaseModel):
    safety_report: SafetyReport = Field(
        ...,
        description="Detailed report of detected safety issues.",
    )
    approval_recommendation: ApprovalRecommendation = Field(
        ...,
        description="Whether the content should be approved, reviewed, or rejected.",
    )


class OrchestratorInput(BaseModel):
    user_topic: str
    platform: str = "linkedin"


class OrchestratorOutput(BaseModel):
    trend_output: TrendAgentOutput
    writer_output: WriterAgentOutput
    safety_output: SafetyAgentOutput
    schedule_output: Optional[dict] = None

