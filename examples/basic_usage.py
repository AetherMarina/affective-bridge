import asyncio

from affective_bridge.providers.ollama_provider import OllamaProvider
from affective_bridge.prompts import SYSTEM_PROMPT
from affective_bridge.schemas import ForensicAnalysis
from affective_bridge.exceptions import AffectiveBridgeParsingError, AffectiveBridgeValidationError


async def main():
    print("Initializing Affective-Bridge with local Ollama provider...")
    provider = OllamaProvider(model="llama3")

    # Simulate a user input masking their true feelings
    test_input = "I'm perfectly fine. It's just a job, I can easily find another one."
    print(f"\nUser Input: '{test_input}'")
    print("Extracting forensic emotional subtext...\n")

    try:
        # 1. Get the structured analysis directly from the provider
        analysis: ForensicAnalysis = await provider.get_analysis(test_input, SYSTEM_PROMPT)

        # 2. Output the structured psychological data
        print("--- Analysis Results ---")
        print(f"Internal reasoning: {analysis.psychological_evaluation}")
        print(f"\nAlibi (Claimed Emotion):    {analysis.alibi}")
        print(f"  - Alibi Coords (V/A):     ({analysis.alibi_valence}, {analysis.alibi_arousal})")
        print(f"\nGlitch (Linguistic Tell):   {analysis.glitch}")
        print(f"\nSilent Narrative (Truth):   {analysis.silent_narrative}")
        print(f"  - Silent Coords (V/A):    ({analysis.silent_valence}, {analysis.silent_arousal})")
        print(f"\nPsychological Dissonance:   {analysis.dissonance}")

    except AffectiveBridgeParsingError as e:
        print(f"\n[ERROR] Failed to parse the LLM's output. It may not be valid JSON.")
        print(f"Details: {e}")
    except AffectiveBridgeValidationError as e:
        print(f"\n[ERROR] The LLM's output did not match the required schema.")
        print(f"Details: {e}")


if __name__ == "__main__":
    asyncio.run(main())
