from .models import Evidence


def calculate_risk_score(evidence: list[Evidence]) -> float:
    """
    Calculate a prototype risk score from marine evidence.

    Higher risk score means greater operational risk.
    """

    risk_score = 0.0

    for item in evidence:

        # Prototype rule for significant wave height
        if item.variable == "wave_height":
            if item.value >= 3.0:
                risk_score += 50
            elif item.value >= 2.0:
                risk_score += 30
            elif item.value >= 1.5:
                risk_score += 15

        # Prototype rule for wind speed
        elif item.variable == "wind_speed":
            if item.value >= 30:
                risk_score += 40
            elif item.value >= 20:
                risk_score += 25
            elif item.value >= 15:
                risk_score += 10

    return min(round(risk_score, 2), 100.0)