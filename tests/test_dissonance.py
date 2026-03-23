from affective_bridge.schemas import ForensicAnalysis


def test_pure_truth_dissonance():
    """Test that identical alibi and silent coordinates yield 0.0 dissonance."""
    truth = ForensicAnalysis(
        alibi="I'm genuinely excited!",
        glitch="None detected.",
        silent_narrative="User is genuinely excited.",
        silent_valence=0.9,
        silent_arousal=0.8,
        alibi_valence=0.9,
        alibi_arousal=0.8
    )
    assert truth.dissonance == 0.0


def test_ultimate_lie_dissonance():
    """Test that maximum coordinate distance yields exactly 1.0 dissonance."""
    the_lie = ForensicAnalysis(
        alibi="Everything is literally perfect!",
        glitch="Hyperbolic language masking deep void.",
        silent_narrative="Complete emotional exhaustion and despair.",
        silent_valence=-1.0,
        silent_arousal=0.0,
        alibi_valence=1.0,
        alibi_arousal=1.0
    )
    assert the_lie.dissonance == 1.0


def test_passive_aggressive_dissonance():
    """Test a realistic mid-range emotional gap."""
    pa = ForensicAnalysis(
        alibi="It's fine, really.",
        glitch="Short sentences, sharp linguistic clipping.",
        silent_narrative="Cold professional resentment.",
        silent_valence=-0.8,
        silent_arousal=0.9,
        alibi_valence=0.2,
        alibi_arousal=0.3
    )
    assert pa.dissonance == 0.522
