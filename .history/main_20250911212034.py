from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Load your trained model
model = joblib.load("pet_recommender_pipeline.joblib")

app = FastAPI(title="Pet Adoption Predictor API")

# Enable CORS for Live Server (or any frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define expected input for prediction


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


@app.get("/")
def root():
    return {"message": "Welcome to the Pet Adoption Predictor API!"}


@app.post("/predict")
def predict(pet: PetData):
    # Convert input to DataFrame
    df = pd.DataFrame([pet.dict()])

    # One-hot encode categorical columns (must match training)
    df = pd.get_dummies(df)

    # Ensure all columns from training exist
    model_columns = model.feature_names_in_
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[model_columns]

    # Predict adoption likelihood
    prediction = model.predict(df)[0]
    return {"prediction": int(prediction)}
