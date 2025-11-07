from fastapi import FastAPI
from pydantic import BaseModel
import pickle

# Load model
with open("adoption_model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()


class Pet(BaseModel):
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


@app.post("/predict")
def predict(pet: Pet):
    # Convert to DataFrame for model
    import pandas as pd
    df = pd.DataFrame([pet.dict()])
    prediction = model.predict(df)[0]
    return {"adoption_likelihood": int(prediction)}
