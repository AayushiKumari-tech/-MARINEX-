from .candidate_plans import CandidatePlan


def calculate_plan_score(plan: CandidatePlan) -> float:
    """
    Calculate a ranking score for a feasible candidate plan.

    Higher opportunity is better.
    Lower risk is better.
    """

    opportunity_component = plan.opportunity_score * 0.7
    risk_component = (100 - plan.risk_score) * 0.3

    score = opportunity_component + risk_component

    return round(score, 2)


def rank_plans(plans: list[CandidatePlan]) -> list[dict]:
    """
    Rank candidate plans from best to worst.
    """

    ranked_plans = []

    for plan in plans:
        score = calculate_plan_score(plan)

        ranked_plans.append(
            {
                "plan_id": plan.plan_id,
                "plan_name": plan.plan_name,
                "ranking_score": score,
                "opportunity_score": plan.opportunity_score,
                "risk_score": plan.risk_score,
            }
        )

    ranked_plans.sort(
        key=lambda item: item["ranking_score"],
        reverse=True
    )

    return ranked_plans