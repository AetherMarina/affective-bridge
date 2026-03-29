import logging
import httpx
from .base import LLMProvider

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class OllamaProvider(LLMProvider):
    """
    A provider for interacting with a local Ollama instance.

    This class handles the specifics of sending a request to the Ollama API
    and extracting the content from the response.
    """
    def __init__(self, model: str = "llama3", url: str = "http://localhost:11434",
                 timeout: float = 30.0, temperature: float = 0.2):
        """
        Initializes the OllamaProvider.

        Args:
            model: The name of the Ollama model to use (e.g., "llama3").
            url: The base URL of the Ollama API endpoint.
            timeout: The timeout in seconds for the HTTP request.
            temperature: The temperature parameter for the Ollama API.
        """
        self.model = model
        self.url = f"{url}/api/chat"
        self.timeout = timeout
        self.temperature = temperature

    async def get_completion(self, prompt: str, system_prompt: str) -> str:
        """
        Retrieves a raw JSON string completion from the Ollama API.

        Args:
            prompt: The user-provided text to be analyzed.
            system_prompt: The system prompt guiding the LLM's behavior.

        Returns:
            A string containing the raw, unparsed JSON output from the LLM.
        
        Raises:
            httpx.HTTPStatusError: If the API returns an unsuccessful status code.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "format": "json",
            "stream": False,
            "options": {"temperature": self.temperature}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()['message']['content']
