from pydantic import BaseModel, ConfigDict, Field


class CatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    ball_speed: float = Field(..., gt=0, allow_inf_nan=False)
    distance: float = Field(..., gt=0, allow_inf_nan=False)
    reaction_time: float = Field(..., ge=0, allow_inf_nan=False)
    angle: float = Field(..., ge=0, le=90, allow_inf_nan=False)
    fielder_skill: float = Field(..., ge=0, le=1, allow_inf_nan=False)
    visibility: float = Field(..., ge=0, le=1, allow_inf_nan=False)


class CatchOutput(BaseModel):
    catch_probability: float = Field(..., ge=0, le=1, allow_inf_nan=False)
    difficulty_index: float = Field(..., ge=0, le=100, allow_inf_nan=False)
    verdict: str
