from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """
    Represents one piece of marine evidence used by MARINEX.
    """

    source: str = Field(
        description="Source of the evidence, e.g. INCOIS PFZ or IMD."
    )

    variable: str = Field(
        description="Marine variable represented by the evidence."
    )

    value: float = Field(
        description="Observed or forecast value."
    )

    unit: Optional[str] = Field(
        default=None,
        description="Unit of measurement."
    )

    latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
        description="Latitude where the evidence applies."
    )

    longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
        description="Longitude where the evidence applies."
    )

    timestamp: datetime = Field(
        description="Time associated with the evidence."
    )

    forecast_horizon_hours: Optional[float] = Field(
        default=None,
        ge=0,
        description="Forecast horizon in hours."
    )

    quality: Optional[str] = Field(
        default=None,
        description="Quality indicator for the evidence."
    )

    provenance: Optional[str] = Field(
        default=None,
        description="Information about where the evidence originated."
    )