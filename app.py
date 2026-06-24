from models import TrendAgentInput, WriterAgentInput

from agents.trend_agent import TrendAgent
from agents.writer_agent import WriterAgent
from models import SafetyAgentInput

from agents.safety_agent import SafetyAgent

def main():
    print("=" * 50)
    print("SOCIALPILOT AI MVP")
    print("=" * 50)

    topic = input("\nEnter your project/topic:\n> ")

    trend_agent = TrendAgent()

    trend_result = trend_agent.run(
        TrendAgentInput(
            user_topic=topic,
            platform="linkedin",
        )
    )

    print("\n--- TREND AGENT OUTPUT ---")
    print("Hashtags:")
    for tag in trend_result.hashtags:
        print(f"  {tag}")

    print("\nTrends:")
    for trend in trend_result.trends:
        print(f"  • {trend}")

    writer_agent = WriterAgent()

    writer_result = writer_agent.run(
        WriterAgentInput(
            user_topic=topic,
            hashtags=trend_result.hashtags,
            trends=trend_result.trends,
            audience_keywords=trend_result.audience_keywords,
            platform="linkedin",
        )
    )

    print("\n--- WRITER AGENT OUTPUT ---")
    print(writer_result.post_content)

    print("\nCTA:")
    print(writer_result.call_to_action)
    print("\n--- SAFETY AGENT OUTPUT ---")

    safety_agent = SafetyAgent()

    safety_result = safety_agent.run(
        SafetyAgentInput(
            post_content=writer_result.post_content,
            call_to_action=writer_result.call_to_action,
        )
    )

    print(
        f"Recommendation: "
        f"{safety_result.approval_recommendation.value}"
    )

    if safety_result.safety_report.issues:
        print("\nDetected Issues:")

        for issue in safety_result.safety_report.issues:
            print(
                f"- {issue.issue_type}: "
                f"{issue.description}"
            )
    else:
        print("No safety issues detected.")

    


if __name__ == "__main__":
    main()

