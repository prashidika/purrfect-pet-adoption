from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

# ------------------- FastAPI setup -------------------
app = FastAPI(
    title="Pet Adoption Predictor API",
    version="0.1.0",
    description="Predict the likelihood of pet adoption based on features."
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Input schema -------------------


class PetData(BaseModel):
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


# ------------------- Load trained model -------------------
model = joblib.load("pet_recommender_pipeline.joblib")

# ------------------- Endpoints -------------------


@app.get("/")
def root():
    return {"message": "Welcome to the Pet Adoption Predictor API!"}


@app.post("/predict")
def predict(pet: PetData):
    # Convert input to DataFrame
    input_df = pd.DataFrame([pet.dict()])

    # Convert categorical columns to match training
    input_df = pd.get_dummies(input_df)

    # Make sure columns match model's training columns
    model_columns = model.feature_names_in_
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0  # add missing column

    input_df = input_df[model_columns]  # reorder columns

    # Prediction
    prediction = model.predict(input_df)[0]

    return {"prediction": int(prediction)}
