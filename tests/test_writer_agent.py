from agents.writer_agent import WriterAgent
from models import WriterAgentInput
from unittest.mock import MagicMock

def test_writer_agent_fallback():
    agent = WriterAgent()
    agent.gemini = MagicMock()
    # Mocking client response to raise exception so it goes to fallback
    agent.gemini.generate.side_effect = Exception("API Error")

    input_data = WriterAgentInput(
        user_topic="Test Topic",
        goal="Lead Generation",
        tone="Professional",
        hashtags=["test"],
        trends=["trend"],
        audience_keywords=["developers"],
        platform="LinkedIn"
    )

    output = agent.run(input_data)
    assert output.post_content is not None
    assert "Test Topic" in output.post_content
    assert output.variations == []
    assert output.call_to_action == "I'd love feedback from developers."

def test_writer_agent_json_parsing():
    agent = WriterAgent()
    agent.gemini = MagicMock()
    # Mocking client response returning JSON
    agent.gemini.generate.return_value = """
    ```json
    {
        "version_a": "This is Version A content.",
        "version_b": "This is Version B content.",
        "version_c": "This is Version C content."
    }
    ```
    """

    input_data = WriterAgentInput(
        user_topic="Test Topic",
        goal="Lead Generation",
        tone="Professional",
        hashtags=["test"],
        trends=["trend"],
        audience_keywords=["developers"],
        platform="LinkedIn"
    )

    output = agent.run(input_data)
    assert output.post_content == "This is Version A content."
    assert output.variations == [
        "This is Version A content.",
        "This is Version B content.",
        "This is Version C content."
    ]
    assert output.call_to_action == "I'd love feedback from developers."

if __name__ == "__main__":
    test_writer_agent_fallback()
    test_writer_agent_json_parsing()
    print("All WriterAgent tests passed successfully!")
