# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd

# Load the trained model
with open("adoption_model.pkl", "rb") as f:
    model = pickle.load(f)

# Define FastAPI app
app = FastAPI()

# Enable CORS so your frontend (HTML/JS) can call the API
app.add_middleware(
    CORSMiddleware,
    # or ["http://127.0.0.1:5500"] if you want to restrict
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body


class Pet(BaseModel):
    AgeMonths: int
    WeightKg: float
    Vaccinated: int
    HealthCondition: int
    TimeInShelterDays: int
    AdoptionFee: float
    PreviousOwner: int


@app.get("/")
def read_root():
    return {"message": "Pet adoption prediction API is running!"}


@app.post("/predict")
def predict(pet: Pet):
    # Convert to DataFrame
    data = pd.DataFrame([{
        "AgeMonths": pet.AgeMonths,
        "WeightKg": pet.WeightKg,
        "Vaccinated": pet.Vaccinated,
        "HealthCondition": pet.HealthCondition,
        "TimeInShelterDays": pet.TimeInShelterDays,
        "AdoptionFee": pet.AdoptionFee,
        "PreviousOwner": pet.PreviousOwner
    }])

    # Make prediction
    prediction = model.predict(data)[0]

    return {"adoption_likelihood": int(prediction)}
