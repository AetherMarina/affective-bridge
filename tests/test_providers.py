import pytest
import respx
from httpx import Response
from affective_bridge.providers.ollama_provider import OllamaProvider
import json


@pytest.mark.asyncio
@respx.mock
async def test_ollama_provider_completion():
    """
    Tests that the Ollama provider correctly extracts the content
    from the nested API response structure.
    """
    # Setup the mock provider
    provider = OllamaProvider(url="http://mock-url")

    # Mock the Ollama API response with the new schema
    mock_content = {
        "alibi": "test alibi",
        "glitch": "test glitch",
        "silent_narrative": "test narrative",
        "silent_valence": -0.5,
        "silent_arousal": 0.6,
        "alibi_valence": 0.1,
        "alibi_arousal": 0.2,
    }
    mock_response_payload = {
        "message": {
            "content": json.dumps(mock_content)
        }
    }
    respx.post("http://mock-url/api/chat").mock(return_value=Response(200, json=mock_response_payload))

    result = await provider.get_completion("Hello", "System Prompt")

    # The result should be the raw JSON string from the 'content' field
    assert result == json.dumps(mock_content)
