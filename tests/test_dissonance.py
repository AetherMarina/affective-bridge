from affective_bridge.schemas import ForensicAnalysis


def test_pure_truth_dissonance():
    """Test that identical alibi and silent coordinates yield 0.0 dissonance."""
    truth = ForensicAnalysis(
        psychological_evaluation="The statement is factual, direct, and congruent with the claimed emotion. No linguistic tells of masking are present.",
        alibi="invigorated excitement",
        glitch=None,
        silent_narrative="invigorated excitement",
        silent_valence=0.9,
        silent_arousal=0.8,
        alibi_valence=0.9,
        alibi_arousal=0.8
    )
    assert truth.dissonance == 0.0


def test_ultimate_lie_dissonance():
    """Test that maximum coordinate distance yields exactly 1.0 dissonance."""
    the_lie = ForensicAnalysis(
        psychological_evaluation="The absolute qualifiers ('literally perfect') contradict the objective reality of the situation, pointing to high-arousal overcompensation masking total burnout.",
        alibi="absolute perfection and boundless energy",
        glitch="Everything is literally perfect",
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
        psychological_evaluation="The overt claim of being 'fine' conflicts with the objective weight of the situation. The phrasing suggests defensive minimization and martyrdom.",
        alibi="unbothered compliance",
        glitch="It's fine, really.",
        silent_narrative="Cold professional resentment.",
        silent_valence=-0.8,
        silent_arousal=0.9,
        alibi_valence=0.2,
        alibi_arousal=0.3
    )
    assert pa.dissonance == 0.522
