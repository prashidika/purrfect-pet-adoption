from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

# Load trained model
model = joblib.load("pet_recommender_pipeline.joblib")

app = FastAPI(
    title="Pet Adoption Predictor API",
    description="Predict the likelihood of a pet being adopted",
    version="0.1.0"
)

# Enable CORS so your website can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, set your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request schema


class PetData(BaseModel):
    PetType: str
    Breed: str
    AgeMonths: int
    Color: str = "Unknown"
    Size: str
    WeightKg: float
    Vaccinated: int
    HealthCondition: int
    TimeInShelterDays: int
    AdoptionFee: float
    PreviousOwner: int


@app.get("/")
def root():
    return {"message": "Welcome to the Pet Adoption Predictor API!"}


@app.post("/predict")
def predict(pet: PetData):
    # Convert incoming data to DataFrame
    df = pd.DataFrame([pet.dict()])

    # Convert categorical columns to dummies (same as during training)
    df = pd.get_dummies(df)

    # Ensure all columns from training exist
    model_columns = model.feature_names_in_
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[model_columns]  # reorder columns

    # Predict probability
    proba = model.predict_proba(df)[0][1]  # probability of adoption
    prediction_percent = round(proba * 100, 2)

    return {
        "adoption_likelihood": int(prediction_percent >= 50),  # 0 or 1
        "adoption_probability": prediction_percent
    }
