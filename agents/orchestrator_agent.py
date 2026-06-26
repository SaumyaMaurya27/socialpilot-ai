"""Orchestrator Agent — coordinates all agents."""

from __future__ import annotations

from typing import ClassVar

from models import (
    OrchestratorInput,
    OrchestratorOutput,
    TrendAgentInput,
    WriterAgentInput,
    SafetyAgentInput,
    ApprovalRecommendation,
)

from agents.trend_agent import TrendAgent
from agents.writer_agent import WriterAgent
from agents.safety_agent import SafetyAgent
from agents.scheduler_agent import SchedulerAgent


class OrchestratorAgent:
    """Coordinates all SocialPilot agents."""

    NAME: ClassVar[str] = "orchestrator_agent"

    DESCRIPTION: ClassVar[str] = (
        "Coordinates Trend, Writer, Safety, and Scheduler agents."
    )

    INSTRUCTION: ClassVar[str] = """
You are the Orchestrator Agent.

Responsibilities:

1. Receive user request
2. Execute Trend Agent
3. Execute Writer Agent
4. Execute Safety Agent
5. Execute Scheduler Agent (if approved)
6. Return combined result
"""

    DEFAULT_MODEL: ClassVar[str] = "gemini-2.0-flash"

    def __init__(self) -> None:
        self.trend_agent = TrendAgent()
        self.writer_agent = WriterAgent()
        self.safety_agent = SafetyAgent()
        self.scheduler_agent = SchedulerAgent()

    def run(
        self,
        input_data: OrchestratorInput,
    ) -> OrchestratorOutput:

        # Trend Agent
        trend_output = self.trend_agent.run(
            TrendAgentInput(
                user_topic=input_data.user_topic,
                platform=input_data.platform,
            )
        )

        # Writer Agent
        writer_output = self.writer_agent.run(
            WriterAgentInput(
                user_topic=input_data.user_topic,
                goal=input_data.goal,
                tone=input_data.tone,
                hashtags=trend_output.hashtags,
                trends=trend_output.trends,
                audience_keywords=trend_output.audience_keywords,
                platform=input_data.platform,
            )
        )

        # Safety Agent
        safety_output = self.safety_agent.run(
            SafetyAgentInput(
                post_content=writer_output.post_content,
                call_to_action=writer_output.call_to_action,
            )
        )

        # Scheduler Agent
        schedule_output = None

        if (
            safety_output.approval_recommendation
            == ApprovalRecommendation.APPROVE
        ):
            schedule_output = self.scheduler_agent.run(
                post_title=input_data.user_topic
            )

        return OrchestratorOutput(
            trend_output=trend_output,
            writer_output=writer_output,
            safety_output=safety_output,
            schedule_output=schedule_output,
        )