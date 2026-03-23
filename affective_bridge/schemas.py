import math

from pydantic import BaseModel, Field, computed_field


class ForensicAnalysis(BaseModel):
    """
    Structured container for affective coordinates.
    The order follows the Forensic-First reasoning logic:
    Surface Performance -> Evidence -> Shadow Truth -> Mapping.
    """

    # 1. The Surface Performance
    alibi: str = Field(description="The overt, literal emotion the user is claiming to feel.")

    # 2. The Evidence
    glitch: str = Field(description="Linguistic anomalies, defensive phrasing, or 'out-of-key' words.")

    # 3. The Shadow Truth
    silent_narrative: str = Field(description="The deduced underlying psychological truth being suppressed.")

    # 4. The Authentic Mapping (Mapped first to anchor the truth)
    silent_valence: float = Field(ge=-1.0, le=1.0, description="Pleasure/Displeasure of the shadow emotion.")
    silent_arousal: float = Field(ge=0.0, le=1.0, description="Activation/Energy of the shadow emotion.")

    # 5. The Performative Mapping
    alibi_valence: float = Field(ge=-1.0, le=1.0, description="Pleasure/Displeasure of the claimed alibi.")
    alibi_arousal: float = Field(ge=0.0, le=1.0, description="Activation/Energy of the claimed alibi.")

    @computed_field
    @property
    def dissonance(self) -> float:
        """
        Calculates the Euclidean distance between the Alibi and the Silent Narrative.
        Normalized to a 0.0 - 1.0 scale using the maximum possible distance (sqrt(5)).
        """
        # The coordinate space spans 2 units on Valence and 1 unit on Arousal.
        # Max distance = sqrt((1 - -1)^2 + (1 - 0)^2) = sqrt(5)
        max_possible_dist = math.sqrt(5)

        # Calculate Euclidean distance: sqrt((x2-x1)^2 + (y2-y1)^2)
        raw_dist = math.sqrt(
            (self.alibi_valence - self.silent_valence) ** 2 +
            (self.alibi_arousal - self.silent_arousal) ** 2
        )

        # Normalize to 0-1 scale and round for clean API output
        return round(raw_dist / max_possible_dist, 3)
