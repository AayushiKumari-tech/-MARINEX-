from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from fastapi import FastAPI

from app.mission.models import Mission
from app.mission.validator import validate_mission

from app.evidence.models import Evidence

from app.planning.candidate_plans import CandidatePlan
from app.planning.pipeline import run_mission_pipeline


app = FastAPI(
    title="MARINEX API",
    description="Marine Mission Intelligence & Decision Engine",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "MARINEX API is running",
        "status": "success"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# BASIC MISSION ENDPOINT
# ============================================================

@app.post("/mission")
def create_mission(mission: Mission):

    validation = validate_mission(mission)

    return {
        "message": "Mission received successfully",
        "validation": validation,
        "mission": mission
    }


# ============================================================
# MARINEX MISSION PLANNING
# ============================================================

@app.post("/mission/plan")
def plan_mission(mission: Mission):

    # --------------------------------------------------------
    # PLAN A — High opportunity but higher risk
    # --------------------------------------------------------

    plan_a_evidence = [

        Evidence(
            source="TEST",
            variable="chlorophyll",
            value=1.1,
            unit="mg/m3",
            latitude=12.90,
            longitude=74.90,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        ),

        Evidence(
            source="TEST",
            variable="wave_height",
            value=2.4,
            unit="m",
            latitude=12.90,
            longitude=74.90,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        ),

        Evidence(
            source="TEST",
            variable="wind_speed",
            value=22,
            unit="knots",
            latitude=12.90,
            longitude=74.90,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        )
    ]

    # --------------------------------------------------------
    # PLAN B — Balanced plan
    # --------------------------------------------------------

    plan_b_evidence = [

        Evidence(
            source="TEST",
            variable="chlorophyll",
            value=1.0,
            unit="mg/m3",
            latitude=12.88,
            longitude=74.88,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        ),

        Evidence(
            source="TEST",
            variable="wave_height",
            value=1.2,
            unit="m",
            latitude=12.88,
            longitude=74.88,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        ),

        Evidence(
            source="TEST",
            variable="wind_speed",
            value=16,
            unit="knots",
            latitude=12.88,
            longitude=74.88,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        )
    ]

    # --------------------------------------------------------
    # PLAN C — Low-risk but lower opportunity
    # --------------------------------------------------------

    plan_c_evidence = [

        Evidence(
            source="TEST",
            variable="chlorophyll",
            value=0.55,
            unit="mg/m3",
            latitude=12.86,
            longitude=74.86,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        ),

        Evidence(
            source="TEST",
            variable="wave_height",
            value=0.8,
            unit="m",
            latitude=12.86,
            longitude=74.86,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        ),

        Evidence(
            source="TEST",
            variable="wind_speed",
            value=10,
            unit="knots",
            latitude=12.86,
            longitude=74.86,
            timestamp=datetime(2026, 9, 15, 6, 0),
            provenance="Prototype test dataset"
        )
    ]

    # --------------------------------------------------------
    # Combine evidence by plan
    # --------------------------------------------------------

    evidence_by_plan = {
        "PLAN-A": plan_a_evidence,
        "PLAN-B": plan_b_evidence,
        "PLAN-C": plan_c_evidence,
    }

    # --------------------------------------------------------
    # Candidate plans
    # --------------------------------------------------------

    plans = [

        CandidatePlan(
            plan_id="PLAN-A",
            plan_name="High Opportunity Zone",

            target_latitude=12.90,
            target_longitude=74.90,

            departure_time=datetime(
                2026, 9, 15, 6, 0
            ),

            activity_duration_hours=5,

            estimated_return_time=datetime(
                2026, 9, 15, 17, 0
            ),

            distance_nm=25
        ),

        CandidatePlan(
            plan_id="PLAN-B",
            plan_name="Balanced Safe Zone",

            target_latitude=12.88,
            target_longitude=74.88,

            departure_time=datetime(
                2026, 9, 15, 6, 0
            ),

            activity_duration_hours=5,

            estimated_return_time=datetime(
                2026, 9, 15, 15, 0
            ),

            distance_nm=18
        ),

        CandidatePlan(
            plan_id="PLAN-C",
            plan_name="Nearshore Zone",

            target_latitude=12.86,
            target_longitude=74.86,

            departure_time=datetime(
                2026, 9, 15, 6, 0
            ),

            activity_duration_hours=4,

            estimated_return_time=datetime(
                2026, 9, 15, 14, 0
            ),

            distance_nm=10
        )
    ]

    # --------------------------------------------------------
    # Run MARINEX
    # --------------------------------------------------------

    result = run_mission_pipeline(
        mission=mission,
        evidence_by_plan=evidence_by_plan,
        candidate_plans=plans
    )

    return result