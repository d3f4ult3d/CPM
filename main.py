from fastapi import FastAPI, HTTPException
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
