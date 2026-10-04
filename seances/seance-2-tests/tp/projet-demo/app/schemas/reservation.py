from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator  # type: ignore


class ReservationCreate(BaseModel):
    item_id: int = Field(ge=1)
    date_debut: date
    date_fin: date

    @model_validator(mode="after")
    def check_dates(self) -> "ReservationCreate":
        if self.date_fin <= self.date_debut:
            raise ValueError("date_fin must be greater than date_debut")
        return self


class ReservationRead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    item_id: int
    date_debut: date
    date_fin: date
    statut: Literal["active", "annulee"]