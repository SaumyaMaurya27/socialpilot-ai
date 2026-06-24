"""Mock Calendar Tool."""

from datetime import datetime, timedelta


class CalendarTool:
    """Mock Google Calendar tool."""

    def schedule_post(
        self,
        title: str,
        days_from_now: int = 1,
    ) -> dict:

        scheduled_time = datetime.now() + timedelta(
            days=days_from_now
        )

        return {
            "success": True,
            "event_title": title,
            "scheduled_time": scheduled_time.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "message": "Mock calendar event created successfully.",
        }