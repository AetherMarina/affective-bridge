class AffectiveBridgeError(Exception):
    """
    Base exception for all errors raised by the Affective-Bridge library.

    Catching this exception will catch all custom errors defined in this library.
    """
    pass


class AffectiveBridgeParsingError(AffectiveBridgeError):
    """
    Raised when the output from the LLM cannot be parsed as valid JSON.

    This typically occurs if the LLM fails to adhere to the JSON output format
    or if the response is malformed.
    """
    pass


class AffectiveBridgeValidationError(AffectiveBridgeError):
    """
    Raised when the parsed JSON from the LLM does not match the expected Pydantic schema.

    This error indicates that the LLM's output was valid JSON but was missing
    required fields or contained data of the wrong type.
    """
    pass
