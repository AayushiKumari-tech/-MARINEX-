from ..mission.models import Mission
from ..evidence.models import Evidence
from ..evidence.scoring import calculate_risk_score
from ..evidence.opportunity import calculate_opportunity_score

from .candidate_plans import CandidatePlan
from .evaluator import evaluate_plan
from .ranking import rank_plans
from .decision import build_decision


def run_mission_pipeline(
    mission: Mission,
    evidence: list[Evidence],
    candidate_plans: list[CandidatePlan],
) -> dict:
    """
    Run the complete MARINEX decision pipeline.

    Flow:
    Mission
        ↓
    Evidence scoring
        ↓
    Candidate plan evaluation
        ↓
    Feasibility filtering
        ↓
    Ranking
        ↓
    Final recommendation
    """

    # --------------------------------------------------
    # 1. Calculate evidence-based scores
    # --------------------------------------------------

    risk_score = calculate_risk_score(evidence)

    opportunity_score = calculate_opportunity_score(evidence)

    # --------------------------------------------------
    # 2. Apply evidence scores to candidate plans
    # --------------------------------------------------

    scored_plans = []

    for plan in candidate_plans:

        updated_plan = plan.model_copy(
            update={
                "risk_score": risk_score,
                "opportunity_score": opportunity_score,
            }
        )

        scored_plans.append(updated_plan)

    # --------------------------------------------------
    # 3. Evaluate feasibility
    # --------------------------------------------------

    evaluations = []

    feasible_plans = []

    for plan in scored_plans:

        evaluation = evaluate_plan(
            mission,
            plan
        )

        evaluations.append(evaluation)

        if evaluation["feasible"]:
            feasible_plans.append(plan)

    # --------------------------------------------------
    # 4. Check whether any feasible plan exists
    # --------------------------------------------------

    if not feasible_plans:

        return {
            "status": "no_feasible_plan",
            "risk_score": risk_score,
            "opportunity_score": opportunity_score,
            "evaluations": evaluations,
            "recommendation": None,
        }

    # --------------------------------------------------
    # 5. Rank feasible plans
    # --------------------------------------------------

    ranked_plans = rank_plans(
        feasible_plans
    )

    # --------------------------------------------------
    # 6. Select best plan
    # --------------------------------------------------

    best_plan_id = ranked_plans[0]["plan_id"]

    selected_plan = next(
        plan
        for plan in feasible_plans
        if plan.plan_id == best_plan_id
    )

    selected_score = ranked_plans[0]["ranking_score"]

    selected_evaluation = next(
        evaluation
        for evaluation in evaluations
        if evaluation["plan_id"] == best_plan_id
    )

    # --------------------------------------------------
    # 7. Build final decision explanation
    # --------------------------------------------------

    decision = build_decision(
        selected_plan,
        selected_score,
        selected_evaluation,
    )

    # --------------------------------------------------
    # 8. Return complete MARINEX result
    # --------------------------------------------------

    return {
        "status": "success",

        "scores": {
            "risk": risk_score,
            "opportunity": opportunity_score,
        },

        "evaluations": evaluations,

        "ranked_plans": ranked_plans,

        "recommendation": decision,
    }