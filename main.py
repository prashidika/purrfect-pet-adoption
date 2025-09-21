from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from pydantic import BaseModel

app = FastAPI()

# Load trained model
model = joblib.load("pet_recommender_pipeline.joblib")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request data model


class PetData(BaseModel):
    PetType: str
    Breed: str
    AgeMonths: int
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
def predict(pet: PetData):
    df = pd.DataFrame([pet.dict()])
    df = pd.get_dummies(df)

    # Align columns with model
    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0
    df = df[model.feature_names_in_]

    # Predict adoption likelihood
    prediction = model.predict(df)[0]  # 0 = Low, 1 = High

    return {
        "adoption_likelihood": int(prediction)  # JS can read 0 or 1
    }
