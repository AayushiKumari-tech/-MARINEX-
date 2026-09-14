from ..evidence.trace import build_evidence_trace
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
    evidence_by_plan: dict[str, list[Evidence]],
    candidate_plans: list[CandidatePlan],
) -> dict:
    """
    Run the MARINEX mission decision pipeline.

    Each candidate plan receives its own marine evidence.

    Flow:

    Mission
        ↓
    Plan-specific evidence
        ↓
    Risk + opportunity scoring
        ↓
    Feasibility evaluation
        ↓
    Ranking
        ↓
    Recommendation
    """

    scored_plans = []
    evaluations = []
    plan_scores = []

    # --------------------------------------------------
    # 1. Score each candidate plan using its own evidence
    # --------------------------------------------------

    for plan in candidate_plans:

        plan_evidence = evidence_by_plan.get(
            plan.plan_id,
            []
        )

        risk_score = calculate_risk_score(
            plan_evidence
        )

        opportunity_score = calculate_opportunity_score(
            plan_evidence
        )

        # Update the plan with evidence-derived scores
        updated_plan = plan.model_copy(
            update={
                "risk_score": risk_score,
                "opportunity_score": opportunity_score,
            }
        )

        scored_plans.append(updated_plan)

        plan_scores.append(
            {
                "plan_id": plan.plan_id,
                "risk_score": risk_score,
                "opportunity_score": opportunity_score,
            }
        )

    # --------------------------------------------------
    # 2. Evaluate feasibility
    # --------------------------------------------------

    feasible_plans = []

    for plan in scored_plans:

        evaluation = evaluate_plan(
            mission,
            plan
        )

        evaluations.append(
            evaluation
        )

        if evaluation["feasible"]:
            feasible_plans.append(
                plan
            )

    # --------------------------------------------------
    # 3. No feasible plan
    # --------------------------------------------------

    if not feasible_plans:

        return {
            "status": "no_feasible_plan",
            "plan_scores": plan_scores,
            "evaluations": evaluations,
            "ranked_plans": [],
            "recommendation": None,
        }

    # --------------------------------------------------
    # 4. Rank feasible plans
    # --------------------------------------------------

    ranked_plans = rank_plans(
        feasible_plans
    )

    # --------------------------------------------------
    # 5. Select best plan
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
    # 6. Build explanation
    # --------------------------------------------------

    decision = build_decision(
        selected_plan,
        selected_score,
        selected_evaluation,
    )
    evidence_trace = build_evidence_trace(
        mission=mission,
        selected_plan=selected_plan,
        evidence=evidence_by_plan.get(
            selected_plan.plan_id,
            []
        ),
        feasibility=selected_evaluation,
        ranking_score=selected_score,
    )

    # --------------------------------------------------
    # 7. Final MARINEX response
    # --------------------------------------------------

    return {
        "status": "success",

        "plan_scores": plan_scores,

        "evaluations": evaluations,

        "ranked_plans": ranked_plans,

        "recommendation": decision,

        "evidence_trace": evidence_trace,
    }