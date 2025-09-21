import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load dataset
data = pd.read_csv("pets.csv")

# Features & target
features = ["AgeMonths", "WeightKg", "Vaccinated", "HealthCondition",
            "TimeInShelterDays", "AdoptionFee", "PreviousOwner"]
X = data[features]
y = data["Adopted"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("adoption_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as adoption_model.pkl")
