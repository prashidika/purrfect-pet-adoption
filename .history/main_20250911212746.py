from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load trained model
model = joblib.load("pet_recommender_pipeline.joblib")

app = FastAPI()


class Pet(BaseModel):
    PetType: str
    Breed: str
    AgeMonths: int
    Color: str
    Size: str
    WeightKg: float
    Vaccinated: int
    HealthCondition: int
    TimeInShelterDays: int
    AdoptionFee: float
    PreviousOwner: int


@app.get("/")
def read_root():
    return {"message": "Welcome to the Pet Adoption Predictor API!"}


@app.post("/predict")
def predict_adoption(pet: Pet):
    # Convert input to DataFrame
    pet_df = pd.DataFrame([pet.dict()])

    # Convert categorical columns to dummy variables
    pet_df = pd.get_dummies(pet_df)

    # Ensure same columns as model expects
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in pet_df.columns:
            pet_df[col] = 0
    pet_df = pet_df[model_features]

    # Predict probability
    proba = model.predict_proba(pet_df)[0][1]  # probability of adoption (1)
    return {"adoption_probability": round(float(proba)*100, 2)}
