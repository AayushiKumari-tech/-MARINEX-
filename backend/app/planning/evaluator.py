from datetime import datetime

from ..mission.models import Mission
from .candidate_plans import CandidatePlan


def evaluate_plan(mission: Mission, plan: CandidatePlan) -> dict:
    """
    Evaluate whether a candidate plan satisfies the mission constraints.
    """

    violations = []

    # 1. Check return deadline
    if (
        mission.return_deadline is not None
        and plan.estimated_return_time > mission.return_deadline
    ):
        violations.append(
            "Estimated return time exceeds the mission return deadline."
        )

    # 2. Check departure time
    if plan.departure_time < mission.departure_time:
        violations.append(
            "Plan departure time is earlier than the mission departure time."
        )

    # 3. Check activity duration
    if plan.activity_duration_hours <= 0:
        violations.append(
            "Activity duration must be greater than zero."
        )

    # 4. Determine feasibility
    feasible = len(violations) == 0

    return {
        "plan_id": plan.plan_id,
        "feasible": feasible,
        "violations": violations
    }