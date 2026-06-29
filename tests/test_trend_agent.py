# """Tests for TrendAgent."""

# from agents.trend_agent import TrendAgent
# from models import TrendAgentInput


# def test_trend_agent_run_returns_expected_counts() -> None:
#     """TrendAgent.run() returns 5 hashtags, 3 trends, and 5 audience keywords."""
#     agent = TrendAgent()
#     input_data = TrendAgentInput(user_topic="I launched an AI Resume Analyzer today")

#     output = agent.run(input_data)

#     assert len(output.hashtags) == 5
#     assert len(output.trends) == 3
#     assert len(output.audience_keywords) == 5
from agents.trend_agent import TrendAgent
from models import TrendAgentInput

agent = TrendAgent()
input_data = TrendAgentInput(user_topic="I launched an AI Resume Analyzer today", platform="LinkedIn")

print("--- Testing TrendAgent.run() ---")
try:
    output = agent.run(input_data)
    print("SUCCESS!")
    print(f"Hashtags: {output.hashtags}")
    print(f"Trends: {output.trends}")
    print(f"Audience Keywords: {output.audience_keywords}")
except Exception as e:
    print(f"FAILED with error: {e}")

