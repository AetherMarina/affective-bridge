import pytest
import math
from affective_bridge.schemas import ForensicAnalysis


def test_dissonance_calculation():
    """
    Tests that the dissonance score is correctly calculated as the normalized
    Euclidean distance between the alibi and silent narrative coordinates.
    """
    data = {
        "psychological_evaluation": "internal reasoning",
        "alibi": "indifference",
        "glitch": "it's fine",
        "silent_narrative": "disappointment",
        "silent_valence": -0.6,
        "silent_arousal": 0.2,
        "alibi_valence": 0.1,
        "alibi_arousal": 0.1,
    }
    analysis = ForensicAnalysis(**data)

    # Manually calculate expected dissonance
    # max_dist = sqrt((1 - -1)^2 + (1 - 0)^2) = sqrt(5)
    raw_dist = math.sqrt((0.1 - -0.6) ** 2 + (0.1 - 0.2) ** 2)
    expected_dissonance = round(raw_dist / math.sqrt(5), 3)

    assert analysis.dissonance == pytest.approx(expected_dissonance)
    assert analysis.alibi == "indifference"


def test_zero_dissonance():
    """
    Tests that dissonance is 0 when the alibi and silent narrative have
    identical affective coordinates.
    """
    data = {
        "psychological_evaluation": "internal reasoning",
        "alibi": "joy",
        "glitch": "n/a",
        "silent_narrative": "joy",
        "silent_valence": 0.8,
        "silent_arousal": 0.7,
        "alibi_valence": 0.8,
        "alibi_arousal": 0.7,
    }
    analysis = ForensicAnalysis(**data)
    assert analysis.dissonance == 0.0


def test_max_dissonance():
    """
    Tests that dissonance is 1.0 when the coordinates are at opposite
    extremes of the affective space.
    """
    data = {
        "psychological_evaluation": "internal reasoning",
        "alibi": "ecstasy",
        "glitch": "n/a",
        "silent_narrative": "depression",
        "silent_valence": -1.0,  # extreme negative
        "silent_arousal": 0.0,   # extreme low
        "alibi_valence": 1.0,    # extreme positive
        "alibi_arousal": 1.0,    # extreme high
    }
    analysis = ForensicAnalysis(**data)
    assert analysis.dissonance == 1.0


@pytest.mark.parametrize("field, value", [
    ("silent_valence", 1.1), ("silent_valence", -1.1),
    ("alibi_valence", 1.1), ("alibi_valence", -1.1),
    ("silent_arousal", 1.1), ("silent_arousal", -0.1),
    ("alibi_arousal", 1.1), ("alibi_arousal", -0.1),
])
def test_forensic_analysis_invalid_fields(field, value):
    """
    Tests that Pydantic's validation raises a ValueError for out-of-bounds
    affective coordinates.
    """
    with pytest.raises(ValueError):
        data = {
            "psychological_evaluation": "internal reasoning",
            "alibi": "x", "glitch": "y", "silent_narrative": "z",
            "silent_valence": 0.0, "silent_arousal": 0.0,
            "alibi_valence": 0.0, "alibi_arousal": 0.0,
        }
        data[field] = value
        ForensicAnalysis(**data)
