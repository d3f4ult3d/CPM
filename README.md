# Catch Probability Model API

## 📌 Overview
This API predicts the probability of a successful catch based on difficulty factors.

## 🚀 Run Instructions

1. Install dependencies:
   pip install -r requirements.txt

2. Run server:
   uvicorn main:app --reload

3. Open docs:
   http://127.0.0.1:8000/docs

## 📥 Endpoint
POST /predict/catch

## 🧾 Sample Request
{
  "ball_speed": 25,
  "distance": 15,
  "reaction_time": 0.5,
  "angle": 30,
  "fielder_skill": 0.8,
  "visibility": 0.9
}

## 📤 Sample Response
{
  "catch_probability": 0.72,
  "difficulty_index": 38.5,
  "verdict": "Moderate Catch"
}

## 📊 Interpretation
- Higher probability → easier catch
- Difficulty index → complexity of attempt