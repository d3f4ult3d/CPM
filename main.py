import json
import sys

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from schemas import CatchInput, CatchOutput
from services import calculate_catch_probability

app = FastAPI(title="Catch Probability Model API")

@app.post("/predict/catch", response_model=CatchOutput)
def predict_catch(data: CatchInput):
    try:
        return calculate_catch_probability(data)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.get("/health")
def health_check():
    return {"status": "ok"}


def _prompt_number(label: str, cast=float):
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return cast(raw)
        except ValueError:
            print("Enter a valid number.")


def run_raw_input_cli() -> None:
    print("\nCatch Probability Model raw input calculator\n")
    try:
        data = CatchInput(
            ball_speed=_prompt_number("Ball speed"),
            distance=_prompt_number("Distance"),
            reaction_time=_prompt_number("Reaction time"),
            angle=_prompt_number("Angle 0-90"),
            fielder_skill=_prompt_number("Fielder skill 0-1"),
            visibility=_prompt_number("Visibility 0-1"),
        )
        output = CatchOutput(**calculate_catch_probability(data))
    except ValidationError as exc:
        print("\nInput validation error:")
        for error in exc.errors():
            field = ".".join(str(part) for part in error["loc"])
            print(f"- {field}: {error['msg']}")
        return

    print("\nCPM output")
    print(f"Catch probability: {output.catch_probability}")
    print(f"Difficulty index: {output.difficulty_index}")
    print(f"Verdict: {output.verdict}")
    print("\nFull response:")
    print(json.dumps(output.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    if "--api" in sys.argv:
        import uvicorn

        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        run_raw_input_cli()
