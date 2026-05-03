# 🌉 Affective-Bridge

[![PyPI version](https://img.shields.io/pypi/v/affective-bridge.svg?color=blue)](https://pypi.org/project/affective-bridge/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://github.com/AetherMarina/affective-bridge/actions/workflows/ci.yml/badge.svg)](https://github.com/AetherMarina/affective-bridge/actions/workflows/ci.yml)

**A Privacy-Sovereign Adapter for Forensic Emotional Inference.**

`Affective-Bridge` is a lightweight, high-performance middleware designed to translate unstructured human text into structured, high-dimensional psychological coordinates. 

Built for **Affective Computing**, context-aware systems, and behavioral analytics, it acts as the analytical layer between raw LLM outputs and deterministic application logic.

## Key Features
- **Forensic Subtext Extraction:** Identifies the overt "Alibi", linguistic "Glitches", and the suppressed "Silent Narrative" in user input.
- **Dimensional Affect Mapping:** Calculates Valence (-1.0 to 1.0), Arousal (0.0 to 1.0), and psychological Dissonance.
- **Provider Agnostic:** Strategy-based architecture supporting local inference via Ollama (Zero-Persistence) and easily extensible to cloud providers.
- **Strict Schema Enforcement:** Utilizes Pydantic V2 for guaranteed JSON validation.
- **Async-First:** Built on `asyncio` and `httpx` for low-latency, concurrent processing.

## Architecture
The bridge utilizes Schema-Driven Reasoning (SDR) to bypass the limitations of standard sentiment analysis. Unlike traditional black-box models, Affective-Bridge employs a single-pass, reasoning-first extraction pipeline:
- **Internal Monologue:** The engine performs a brief, binary psychological evaluation to determine the "Null Hypothesis" (congruence) before committing to a dissonance state.
- **Dual-State Mapping:** By explicitly parsing the Alibi (overt claim) and the Glitch (linguistic tell), the library maps latent tension into deterministic metrics.
- **Few-Shot Calibration:** Utilizing specialized emotional archetypes, the engine maintains a consistent mathematical scale for Valence and Arousal, preventing coordinate drift and ensuring stable, repeatable results.

This architecture eliminates the need for complex multi-agent overhead, providing high-fidelity emotional subtext detection with minimal latency.
## 📂 Project Structure

```text
affective-bridge/
├── affective_bridge/
│   ├── __init__.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py          # The Strategy Interface
│   │   └── ollama_provider.py # Local LLM integration
│   ├── exceptions.py        # Custom exceptions
│   ├── prompts.py           # The Forensic System Prompt
│   └── schemas.py           # The Pydantic output models
├── evals/
│   ├── baseline_evaluation_matrix.csv
│   └── example_eval_run.csv
│   └── prompt_calibration_matrix.ipynb
├── tests/
│   ├── test_dissonance.py
│   ├── test_providers.py
│   └── test_schemas.py
├── examples/
│   └── basic_usage.py
├── pyproject.toml           # Project configuration
├── README.md                # Project documentation
└── LICENSE                  # Apache License 2.0
└── requirements-dev.txt     # Python dependencies
```

## Installation

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai/) installed locally.
- A local copy of a model, for example Llama 3:
  ```bash
  ollama pull llama3
  ```
You can install `affective-bridge` directly from PyPI:
```bash
pip install affective-bridge
```

## Quick Start 

### Basic Usage

```python
import asyncio
from affective_bridge.providers.ollama_provider import OllamaProvider
from affective_bridge.prompts import SYSTEM_PROMPT
from affective_bridge.schemas import ForensicAnalysis


async def main():
  # Initialize with local privacy-first provider
  provider = OllamaProvider(model="llama3")

  text = "I'm fine. Everything is going exactly according to plan."

  # Get the structured analysis directly from the provider.
  analysis: ForensicAnalysis = await provider.get_analysis(text, SYSTEM_PROMPT)

  print(f"Alibi: {analysis.alibi}")
  print(f"Silent Narrative: {analysis.silent_narrative}")
  print(f"Dissonance Score: {analysis.dissonance}")  # e.g., 0.82


if __name__ == "__main__":
  asyncio.run(main())
```

## Development Setup
For development, it's recommended to set up an editable install. This allows you to run examples and tests against your local source code.

First, clone the repository and navigate into the project directory:
```bash
git clone https://github.com/AetherMarina/affective-bridge.git
cd affective-bridge
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install the project in editable mode + Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

This command installs all dependencies from `pyproject.toml` and makes the `affective_bridge` package available in your environment.

## Extending the Bridge: Custom Providers

`Affective-Bridge` is designed to be provider-agnostic. You can easily add support for any LLM backend (e.g., Anthropic, Gemini, Groq, or a custom internal API) by creating a new provider class that implements the `LLMProvider` interface.

### The Contract
Your custom provider must inherit from `LLMProvider` and implement the `get_completion` async method. The base class automatically provides the `get_analysis` wrapper, which handles the JSON parsing and Pydantic validation for you. 

The core interface is defined in `affective_bridge/providers/base.py`.

### Example: Creating a Dummy Provider
Here is a minimal example of a provider that returns a hardcoded JSON response to demonstrate the required structure:

**1. Create the file:** `affective_bridge/providers/dummy_provider.py`
```python
import json
from .base import LLMProvider

class DummyProvider(LLMProvider):
    """A simple provider for testing that returns a fixed JSON response."""
    
    async def get_completion(self, prompt: str, system_prompt: str) -> str:
        # In a real provider, you would make an HTTP/API call here.
        # For this example, we return a valid, hardcoded JSON string.
        dummy_response = {
          "psychological_evaluation": "The user claims the project is on track, but the repeated use of passive voice indicates emotional distancing. This linguistic glitch reveals underlying frustration with team performance, creating measurable dissonance.",
          "alibi": "User claims the project is on track.",
          "glitch": "Repeatedly uses passive voice ('milestones were met').",
          "silent_narrative": "Underlying frustration with team performance.",
          "silent_valence": -0.3,
          "silent_arousal": 0.5,
          "alibi_valence": 0.2,
          "alibi_arousal": 0.1
        }
        return json.dumps(dummy_response)
```

2. Use the new provider: You can now import and use DummyProvider just like any other provider.

```python
from affective_bridge.providers.dummy_provider import DummyProvider

provider = DummyProvider()
analysis = await provider.get_analysis("Any text here", "Any prompt here")

print(analysis.silent_narrative)
```

## 🧪 Evaluation & Calibration

Because affective extraction relies on probabilistic models, `Affective-Bridge` ships with a deterministic evaluation suite located in the `evals/` directory.

This suite contains a **Golden Dataset** (`baseline_evaluation_matrix.csv`) consisting of 15 highly complex psychological edge cases (including toxic positivity, passive-aggression, and burden minimization) calibrated against Llama 3 8B. 

If you modify the `SYSTEM_PROMPT` or swap the backend to a different provider (like Claude or GPT-4), you can use the included evaluation scripts to generate an `example_eval_run.csv`. The suite will output a color-coded Pandas heatmap comparing your new run against the baseline, instantly highlighting any regressions in the model's ability to detect psychological dissonance.

## ⚠️ Limitations & Disclaimer

`Affective-Bridge` is an experimental utility that interfaces with probabilistic Large Language Models (LLMs). Users must be aware of the following inherent limitations:

1.  **Non-Deterministic Outputs:** LLMs are not deterministic. While this library enforces a strict output schema, the underlying qualitative analysis (like the "Silent Narrative") is subjective and can contain inaccuracies or hallucinations.
2.  **Not a Clinical or Diagnostic Tool (No Profiling):** The dimensional mapping is an abstraction based on the Circumplex Model of Affect, intended solely for research, creative, and experimental applications. It is not a valid psychological metric. This tool must never be used for mental health diagnostics, employee monitoring, or automated decision-making. Furthermore, using this library to profile individuals or infer real-world traits, intentions, or mental states is strictly discouraged and may violate applicable data protection and AI regulations.
3.  **Use at Your Own Risk:** This open-source library is provided "as is," without warranty of any kind. Developers are responsible for implementing their own safety fallbacks and ethical reviews when using this data to drive application logic.

## ⚖️ Authorship Disclaimer
**Affective-Bridge** is an independent, personal project developed by Marina Kaličanin. 
It is not an official product of, nor is it endorsed by, any past or current employers. 
The architecture, logic, and implementation were created outside of professional work hours using personal resources.

## License
This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for the full text.