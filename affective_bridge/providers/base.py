import logging
import json
from abc import ABC, abstractmethod
from pydantic import ValidationError

from ..schemas import ForensicAnalysis
from ..exceptions import AffectiveBridgeParsingError, AffectiveBridgeValidationError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    This class defines the interface for concrete provider implementations.
    It uses the Strategy Pattern to allow for different LLM backends
    (e.g., local, cloud-based) to be used interchangeably.
    """

    @abstractmethod
    async def get_completion(self, prompt: str, system_prompt: str) -> str:
        """
        Retrieves a raw JSON string completion from the LLM.

        Args:
            prompt: The user-provided text to be analyzed.
            system_prompt: The system prompt guiding the LLM's behavior.

        Returns:
            A string containing the raw, unparsed JSON output from the LLM.
        """
        pass

    async def get_analysis(self, prompt: str, system_prompt: str) -> ForensicAnalysis:
        """
        Gets and validates a forensic analysis from the LLM.

        This method orchestrates the process of getting a completion,
        parsing it as JSON, and validating it against the ForensicAnalysis schema.

        Args:
            prompt: The user-provided text to be analyzed.
            system_prompt: The system prompt guiding the LLM's behavior.

        Returns:
            A ForensicAnalysis object containing the structured psychological data.

        Raises:
            AffectiveBridgeParsingError: If the LLM output is not valid JSON.
            AffectiveBridgeValidationError: If the JSON does not match the ForensicAnalysis schema.
        """
        try:
            raw_json = await self.get_completion(prompt, system_prompt)
            parsed_data = json.loads(raw_json)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM output as JSON: {e}")
            raise AffectiveBridgeParsingError(f"Invalid JSON returned from LLM: {e}") from e
            
        try:
            analysis = ForensicAnalysis(**parsed_data)
            return analysis
        except ValidationError as e:
            logger.error(f"Failed to validate LLM output against schema: {e}")
            raise AffectiveBridgeValidationError(f"LLM output does not match expected schema: {e}") from e
