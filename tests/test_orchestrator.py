from agents.orchestrator_agent import OrchestratorAgent
from models import OrchestratorInput

agent = OrchestratorAgent()

result = agent.run(
    OrchestratorInput(
        user_topic="I launched an AI Resume Analyzer today"
    )
)

print("\n=== ORCHESTRATOR RESULT ===\n")

print("Hashtags:")
print(result.trend_output.hashtags)

print("\nPost:")
print(result.writer_output.post_content)

print("\nSafety:")
print(result.safety_output.approval_recommendation.value)