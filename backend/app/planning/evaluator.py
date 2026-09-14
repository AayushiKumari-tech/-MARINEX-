from datetime import datetime, timezone

from ..mission.models import Mission
from .candidate_plans import CandidatePlan


def make_timezone_aware(dt: datetime) -> datetime:
    """
    Convert a datetime into a timezone-aware UTC datetime.

    If the datetime has no timezone information,
    treat it as UTC for the prototype.
    """

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)


def evaluate_plan(
    mission: Mission,
    plan: CandidatePlan,
) -> dict:
    """
    Evaluate whether a candidate plan satisfies
    the currently implemented mission constraints.
    """

    violations = []

    # --------------------------------------------------
    # Normalize mission and plan times
    # --------------------------------------------------

    mission_departure = make_timezone_aware(
        mission.departure_time
    )

    plan_departure = make_timezone_aware(
        plan.departure_time
    )

    plan_return = make_timezone_aware(
        plan.estimated_return_time
    )

    mission_deadline = None

    if mission.return_deadline is not None:
        mission_deadline = make_timezone_aware(
            mission.return_deadline
        )

    # --------------------------------------------------
    # 1. Return deadline
    # --------------------------------------------------

    if (
        mission_deadline is not None
        and plan_return > mission_deadline
    ):
        violations.append(
            "Estimated return time exceeds the mission return deadline."
        )

    # --------------------------------------------------
    # 2. Departure time
    # --------------------------------------------------

    if plan_departure < mission_departure:
        violations.append(
            "Plan departure time is earlier than the mission departure time."
        )

    # --------------------------------------------------
    # 3. Activity duration
    # --------------------------------------------------

    if plan.activity_duration_hours <= 0:
        violations.append(
            "Activity duration must be greater than zero."
        )

    # --------------------------------------------------
    # 4. Prototype marine risk constraint
    # --------------------------------------------------

    # Prototype threshold only.
    # This is NOT an official INCOIS safety limit.

    if plan.risk_score >= 70:
        violations.append(
            "Prototype marine risk score exceeds the allowed threshold."
        )

    # --------------------------------------------------
    # 5. Determine feasibility
    # --------------------------------------------------

    feasible = len(violations) == 0

    return {
        "plan_id": plan.plan_id,
        "feasible": feasible,
        "violations": violations,
    }