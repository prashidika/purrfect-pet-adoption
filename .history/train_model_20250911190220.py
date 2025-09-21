import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("pets.csv")

# For simplicity, only numeric columns
X = df[["AgeMonths", "WeightKg", "Vaccinated", "HealthCondition",
        "TimeInShelterDays", "AdoptionFee", "PreviousOwner"]]
y = df["AdoptionLikelihood"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "adoption_model.pkl")
print("Model saved!")
