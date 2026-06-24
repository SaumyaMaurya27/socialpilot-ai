"""Tests for TrendAgent."""

from agents.trend_agent import TrendAgent
from models import TrendAgentInput


def test_trend_agent_run_returns_expected_counts() -> None:
    """TrendAgent.run() returns 5 hashtags, 3 trends, and 5 audience keywords."""
    agent = TrendAgent()
    input_data = TrendAgentInput(user_topic="I launched an AI Resume Analyzer today")

    output = agent.run(input_data)

    assert len(output.hashtags) == 5
    assert len(output.trends) == 3
    assert len(output.audience_keywords) == 5
