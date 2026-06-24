"""Scheduler Agent."""

from __future__ import annotations

from typing import ClassVar

from tools.calendar_tool import CalendarTool


class SchedulerAgent:
    """Schedules approved content."""

    NAME: ClassVar[str] = "scheduler_agent"

    DESCRIPTION: ClassVar[str] = (
        "Schedules social media content."
    )

    DEFAULT_MODEL: ClassVar[str] = "gemini-2.0-flash"

    def __init__(self) -> None:
        self.calendar_tool = CalendarTool()

    def run(
        self,
        post_title: str,
    ) -> dict:

        return self.calendar_tool.schedule_post(
            title=post_title
        )