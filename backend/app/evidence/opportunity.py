from .models import Evidence


def calculate_opportunity_score(evidence: list[Evidence]) -> float:
    """
    Calculate a prototype opportunity score from marine evidence.

    Higher score means stronger opportunity according to
    the prototype rules.
    """

    opportunity_score = 0.0

    for item in evidence:

        # Prototype rule for chlorophyll
        if item.variable == "chlorophyll":
            if item.value >= 1.0:
                opportunity_score += 60
            elif item.value >= 0.7:
                opportunity_score += 45
            elif item.value >= 0.4:
                opportunity_score += 30
            elif item.value >= 0.2:
                opportunity_score += 15

    return min(round(opportunity_score, 2), 100.0)