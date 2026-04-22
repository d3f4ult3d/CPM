import math

from schemas import CatchInput
from utils import clamp


def sigmoid(x):
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    z = math.exp(x)
    return z / (1 + z)


def _normalize_input(data) -> CatchInput:
    if isinstance(data, CatchInput):
        return data
    if isinstance(data, dict):
        return CatchInput(**data)
    raise TypeError("data must be a CatchInput instance or a dictionary")


def calculate_catch_probability(data: CatchInput):
    data = _normalize_input(data)

    # Derived variables
    time_available = data.distance / data.ball_speed
    movement_efficiency = max(0, time_available - data.reaction_time)

    # Difficulty components
    distance_factor = clamp(data.distance / 25, 0, 1)
    angle_factor = clamp(data.angle / 90, 0, 1)
    reaction_factor = clamp(data.reaction_time / 1.5, 0, 1)
    visibility_factor = clamp(1 - data.visibility, 0, 1)

    # Weighted difficulty score
    difficulty_score = (
        0.25 * distance_factor +
        0.20 * angle_factor +
        0.25 * reaction_factor +
        0.15 * visibility_factor
    )

    adjusted_score = clamp(
        difficulty_score * (1 - 0.5 * data.fielder_skill),
        0,
        1,
    )

    # Convert to probability using sigmoid
    catch_probability = clamp(sigmoid((0.5 - adjusted_score) * 5), 0, 1)

    # Difficulty index
    difficulty_index = clamp(adjusted_score * 100, 0, 100)

    # Verdict
    if catch_probability > 0.75:
        verdict = "Easy Catch"
    elif catch_probability > 0.4:
        verdict = "Moderate Catch"
    else:
        verdict = "Difficult Catch"

    return {
        "catch_probability": round(catch_probability, 3),
        "difficulty_index": round(difficulty_index, 2),
        "verdict": verdict
    }
