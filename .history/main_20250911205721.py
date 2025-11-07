from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load the trained model
model = joblib.load("pet_recommender_pipeline.joblib")


@app.get("/")
def root():
    return {"message": "Welcome to the Pet Adoption Predictor API!"}


@app.post("/predict")
def predict(pet: dict):
    # Convert input to DataFrame
    df = pd.DataFrame([pet])
    df = pd.get_dummies(df)

    # Align columns with training data
    model_columns = model.feature_names_in_
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[model_columns]

    prediction = model.predict(df)[0]
    return {"prediction": int(prediction)}
