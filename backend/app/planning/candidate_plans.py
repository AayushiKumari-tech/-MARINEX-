from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CandidatePlan(BaseModel):
    """
    Represents one possible operational plan for a marine mission.
    """

    plan_id: str = Field(
        description="Unique identifier for the candidate plan."
    )

    plan_name: str = Field(
        description="Human-readable name of the plan."
    )

    target_latitude: float = Field(
        ge=-90,
        le=90,
        description="Latitude of the target operating area."
    )

    target_longitude: float = Field(
        ge=-180,
        le=180,
        description="Longitude of the target operating area."
    )

    departure_time: datetime = Field(
        description="Planned departure time."
    )

    activity_duration_hours: float = Field(
        gt=0,
        description="Time spent performing the main activity."
    )

    estimated_return_time: datetime = Field(
        description="Estimated time of return."
    )

    opportunity_score: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Estimated marine opportunity score."
    )

    risk_score: float = Field(
        default=0.0,
        ge=0,
        le=100,
        description="Estimated operational risk score."
    )

    distance_nm: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated travel distance in nautical miles."
    )