from .models import Mission


def build_constraints(mission: Mission) -> dict:
    """
    Convert a mission into structured hard constraints
    and soft preferences.
    """

    hard_constraints = list(mission.hard_constraints)
    soft_preferences = list(mission.soft_preferences)

    # The return deadline is automatically a hard constraint
    # because the mission must finish before this time.
    if mission.return_deadline is not None:
        hard_constraints.append(
            "Return before the specified deadline."
        )

    return {
        "hard_constraints": hard_constraints,
        "soft_preferences": soft_preferences
    }