from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI(title="Pet Adoption Predictor API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    # allows all origins; for production, restrict to your domain
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your trained model
model = joblib.load("pet_recommender_pipeline.joblib")

# Define input schema


class PetData(BaseModel):
    PetType: str
    Breed: str
    AgeMonths: int
    Color: str
    Size: str
    WeightKg: float
    Vaccinated: int  # 1 = Yes, 0 = No
    HealthCondition: int  # 1 = Good, 0 = Bad
    TimeInShelterDays: int
    AdoptionFee: float
    PreviousOwner: int  # 1 = Yes, 0 = No

# Root endpoint


@app.get("/")
def read_root():
    return {"message": "Welcome to the Pet Adoption Predictor API!"}

# Prediction endpoint


@app.post("/predict")
def predict(pet: PetData):
    # Convert input to DataFrame
    df = pd.DataFrame([pet.dict()])

    # Convert categorical columns to dummies (same as training)
    df = pd.get_dummies(df)

    # Align columns with training model
    # This ensures missing dummy columns are added with 0
    model_columns = model.feature_names_in_
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[model_columns]

    # Make prediction
    prediction = model.predict(df)[0]

    return {"adoption_likelihood": int(prediction)}
