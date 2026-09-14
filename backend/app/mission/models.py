from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Mission(BaseModel):
    """
    Represents a marine mission requested by the user.
    """

    objective: str = Field(
        description="Main goal of the marine mission, e.g. fishing or navigation."
    )

    departure_time: datetime = Field(
        description="Planned mission departure time."
    )

    duration_hours: float = Field(
        gt=0,
        description="Expected mission duration in hours."
    )

    return_deadline: Optional[datetime] = Field(
        default=None,
        description="Latest acceptable return time."
    )

    start_latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
        description="Starting latitude."
    )

    start_longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
        description="Starting longitude."
    )

    hard_constraints: list[str] = Field(
        default_factory=list,
        description="Conditions that must not be violated."
    )

    soft_preferences: list[str] = Field(
        default_factory=list,
        description="Preferences used when ranking feasible plans."
    )

    vessel_speed_knots: Optional[float] = Field(
        default=None,
        gt=0,
        description="Expected vessel speed in nautical miles per hour."
    )