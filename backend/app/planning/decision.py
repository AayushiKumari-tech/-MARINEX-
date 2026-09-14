from .candidate_plans import CandidatePlan


def build_decision(
    selected_plan: CandidatePlan,
    ranking_score: float,
    feasibility_result: dict,
) -> dict:
    """
    Build a transparent explanation
    for the selected plan.
    """

    reasons = [
        "The plan passed all currently implemented feasibility checks.",
        (
            f"Opportunity score: "
            f"{selected_plan.opportunity_score}/100."
        ),
        (
            f"Risk score: "
            f"{selected_plan.risk_score}/100."
        ),
        (
            f"Ranking score: "
            f"{ranking_score}/100."
        ),
    ]

    return {
        "recommended_plan": {
            "plan_id": selected_plan.plan_id,
            "plan_name": selected_plan.plan_name,
        },

        "decision": "recommended",

        "reasons": reasons,

        "feasibility": feasibility_result,
    }