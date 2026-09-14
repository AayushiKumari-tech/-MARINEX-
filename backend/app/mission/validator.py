from datetime import timedelta

from .models import Mission


def validate_mission(mission: Mission) -> dict:
    """
    Check whether a marine mission is internally consistent.
    """

    errors = []

    # 1. Check return deadline
    planned_return_time = (
        mission.departure_time
        + timedelta(hours=mission.duration_hours)
    )

    if (
        mission.return_deadline is not None
        and planned_return_time > mission.return_deadline
    ):
        errors.append(
            "Mission duration exceeds the return deadline."
        )

    # 2. Check that latitude and longitude are provided together
    if (
        (mission.start_latitude is None)
        != (mission.start_longitude is None)
    ):
        errors.append(
            "Starting latitude and longitude must be provided together."
        )

    # 3. Return validation result
    if errors:
        return {
            "valid": False,
            "errors": errors
        }

    return {
        "valid": True,
        "errors": []
    }