from ..mission.models import Mission
from ..planning.candidate_plans import CandidatePlan


def build_evidence_trace(
    mission: Mission,
    selected_plan: CandidatePlan,
    evidence: list,
    feasibility: dict,
    ranking_score: float,
) -> dict:
    """
    Build a transparent evidence-to-decision trace.

    This explains how MARINEX arrived at its recommendation.
    """

    evidence_items = []

    for item in evidence:
        evidence_items.append(
            {
                "source": item.source,
                "variable": item.variable,
                "value": item.value,
                "unit": item.unit,
                "latitude": item.latitude,
                "longitude": item.longitude,
                "timestamp": item.timestamp,
                "provenance": item.provenance,
            }
        )

    return {
        "mission": {
            "objective": mission.objective,
            "departure_time": mission.departure_time,
            "return_deadline": mission.return_deadline,
            "duration_hours": mission.duration_hours,
        },

        "selected_plan": {
            "plan_id": selected_plan.plan_id,
            "plan_name": selected_plan.plan_name,
            "target_latitude": selected_plan.target_latitude,
            "target_longitude": selected_plan.target_longitude,
        },

        "evidence": evidence_items,

        "feasibility": {
            "feasible": feasibility["feasible"],
            "violations": feasibility["violations"],
        },

        "ranking": {
            "ranking_score": ranking_score,
            "opportunity_score": selected_plan.opportunity_score,
            "risk_score": selected_plan.risk_score,
        },

        "decision_logic": [
            "Marine evidence was collected for the candidate plan.",
            "Evidence was converted into opportunity and risk scores.",
            "The candidate plan was evaluated against implemented mission constraints.",
            "Feasible plans were ranked.",
            "The highest-ranked feasible plan was selected.",
        ],
    }