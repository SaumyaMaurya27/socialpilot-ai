from utils.gemini_client import GeminiClient

client = GeminiClient()

response = client.generate(
    "Say hello in one sentence."
)

print(response)