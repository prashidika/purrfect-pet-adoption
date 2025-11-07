from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

# Load the trained model
model = pickle.load(open("adoption_model.pkl", "rb"))

# Define input schema


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

# API endpoint


@app.post("/predict")
def predict_adoption(data: PetData):
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)[0]
    return {"adoption_likelihood": int(prediction)}
