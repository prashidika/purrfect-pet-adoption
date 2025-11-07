from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load model
model = joblib.load("pet_recommender_pipeline.joblib")

# Define FastAPI app
app = FastAPI(title="Pet Adoption Predictor API", version="0.1.0")

# Define input schema using Pydantic


class Pet(BaseModel):
    PetType: str
    Breed: str
    AgeMonths: int
    Color: str
    Size: str
    WeightKg: float
    Vaccinated: str
    HealthCondition: str
    TimeInShelterDays: int
    AdoptionFee: float
    PreviousOwner: str


# Keep a template of training columns for dummies
training_columns = model.feature_names_in_


@app.get("/")
def root():
    return {"message": "Welcome to the Pet Adoption Predictor API!"}


@app.post("/predict")
def predict(pet: Pet):
    # Convert input to DataFrame
    input_df = pd.DataFrame([pet.dict()])

    # Convert categorical columns to dummies (one-hot encoding)
    input_df = pd.get_dummies(input_df)

    # Add missing columns that were present during training
    for col in training_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Ensure columns order matches the training columns
    input_df = input_df[training_columns]

    # Make prediction
    prediction = model.predict(input_df)[0]

    return {"prediction": int(prediction)}
