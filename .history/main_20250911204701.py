from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load trained model
model = joblib.load("pet_recommender_pipeline.joblib")


@app.post("/predict")
def predict_pet_adoption(input_data: dict):
    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)

    # Align columns with training features
    trained_columns = model.feature_names_in_
    for col in trained_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[trained_columns]

    prediction = model.predict(df)[0]
    return {"AdoptionLikelihood": int(prediction)}
